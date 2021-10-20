from pathlib import Path

from git import Repo
from loguru import logger
from slugify import slugify

from pyadr.const import REVIEW_REQUESTS
from pyadr.content_utils import adr_status_from_file
from pyadr.core import AdrCore
from pyadr.exceptions import PyadrStatusIncompatibleWithReviewRequestError
from pyadr.git.config import GitAdrConfig
from pyadr.git.const import PROPOSAL_REQUEST
from pyadr.git.exceptions import (
    PyadrGitAdrNotStagedError,
    PyadrGitAdrNotStagedOrCommittedError,
    PyadrGitPreMergeChecksFailedError,
)
from pyadr.git.utils import (
    create_feature_branch_and_checkout,
    get_verified_repo_client,
    verify_branch_does_not_exist,
    verify_index_empty,
    verify_main_branch_exists,
)


class GitAdrCore(AdrCore):
    def __init__(self):
        self.config = GitAdrConfig()
        self._repo = None

    ###########################################
    # PROPERTIES
    ###########################################
    @property
    def commit_message_default_prefix(self) -> str:
        if self.config["git"].getboolean("adr-only-repo"):
            return "feat(adr):"
        else:
            return "docs(adr):"

    @property
    def repo(self) -> Repo:
        if not self._repo:
            self._repo = get_verified_repo_client(Path.cwd())
        return self._repo

    ###########################################
    # CONFIGURE ADR
    ###########################################
    def configure(self, setting: str, value: str) -> None:
        self.config.configure(setting, value)
        logger.info(f"Configured '{setting}' to '{value}'.")

    def unset_config_setting(self, setting: str) -> None:
        self.config.unset(setting)
        logger.info(f"AdrConfig setting '{setting}' unset.")

    ###########################################
    # GIT INIT ADR
    ###########################################
    def git_init_adr_repo(self, force: bool = False) -> None:
        verify_index_empty(self.repo)

        init_branch_name = "adr-init-repo"
        verify_branch_does_not_exist(self.repo, init_branch_name)

        created_files = self.init_adr_repo(force=force)

        if "main" not in self.repo.heads:
            logger.info("Git repo empty. Will commit files to 'main'.")
        else:
            create_feature_branch_and_checkout(self.repo, init_branch_name)

        self.repo.index.add([str(p) for p in created_files])

        message = f"{self.commit_message_default_prefix} initialise adr repository"
        self.repo.index.commit(message)

        logger.info(
            f"Files committed to branch '{self.repo.head.ref.name}' "
            f"with commit message '{message}'."
        )
        logger.info("ADR Git repo initialised.")

    ###########################################
    # GIT NEW ADR
    ###########################################
    def git_new_adr(self, title: str, pre_checks: bool = True) -> None:
        if pre_checks:
            verify_main_branch_exists(self.repo, branch="main")

        logger.info("Switching to 'main'...")
        self.repo.heads.main.checkout()
        logger.log("VERBOSE", "... done.")

        if pre_checks:
            self.verify_adr_dir_exists()

        verify_index_empty(self.repo)

        def build_adr_branch_name(request_type: str, title: str) -> str:
            return "-".join(["adr", request_type, slugify(title)])

        adr_branch_name = build_adr_branch_name(PROPOSAL_REQUEST, title)
        verify_branch_does_not_exist(self.repo, adr_branch_name)

        new_adr_path = self.new_adr(title, pre_checks=False)

        create_feature_branch_and_checkout(self.repo, adr_branch_name)

        logger.info(f"Staging '{new_adr_path}'...")
        self.repo.index.add([str(new_adr_path)])
        logger.log("VERBOSE", "... done.")

        logger.info("New ADR added to Git repo.")

    ###########################################
    # ACCEPT / REJECT
    ###########################################
    def git_accept_or_reject(
        self, file: str, status: str, toc: bool = False, commit: bool = False
    ) -> None:
        self._verify_adr_staged_or_committed(Path(file))

        processed_adr = self.accept_or_reject(file, status, toc)

        if commit:
            self._commit_adr(processed_adr)

    def _commit_adr(self, adr_path):
        logger.info(f"Committing ADR '{adr_path}'...")
        commit_message = self._commit_message_for_adr(adr_path)
        self.repo.index.commit(commit_message)
        logger.success(f"Committed ADR '{adr_path}' with message '{commit_message}'.")

    def _commit_message_for_adr(self, adr_path: Path) -> str:
        self._verify_adr_filename(adr_path)

        adr_status = adr_status_from_file(adr_path)
        return (
            f"{self._commit_message_prefix_for_status(adr_status)} "
            f"[{adr_status}] "
            f"{adr_path.stem}"
        )

    def _commit_message_prefix_for_status(self, status: str) -> str:
        if status == "proposed":
            return "chore(adr):"
        else:
            return self.commit_message_default_prefix

    def _verify_adr_staged_or_committed(
        self, path: Path, print_error_message: bool = True
    ) -> None:
        if not (self._file_staged(path) or self._file_committed(path)):
            if print_error_message:
                logger.error(f"ADR '{path}' should be staged or committed first.")
            raise PyadrGitAdrNotStagedOrCommittedError(path)

    def _verify_adr_staged(self, path: Path, print_error_message: bool = True) -> None:
        if not (self._file_staged(path) or self._file_committed(path)):
            if print_error_message:
                logger.error(f"ADR '{path}' should be staged first.")
            raise PyadrGitAdrNotStagedError(path)

    def _file_staged(self, path):
        return str(path) in [d.a_path for d in self.repo.index.diff("HEAD")]

    def _file_committed(self, path):
        return str(path) in list(self.repo.head.commit.stats.files.keys())

    def _apply_accept_or_reject_to_proposed_adr(
        self, proposed_adr: Path, status: str
    ) -> Path:
        processed_adr = super()._apply_accept_or_reject_to_proposed_adr(
            proposed_adr, status
        )

        self.repo.index.add([str(processed_adr)])

        return processed_adr

    def _apply_filepath_update(self, path: Path, renamed_path: Path) -> None:
        try:
            self._verify_adr_staged_or_committed(path, print_error_message=False)
        except PyadrGitAdrNotStagedOrCommittedError:
            logger.debug("not staged or committed")
            super()._apply_filepath_update(path, renamed_path)
            self.repo.index.add([str(renamed_path)])
        else:
            logger.debug("staged or committed")
            self.repo.git.mv(str(path), str(renamed_path))

    ###########################################
    # COMMIT ADR
    ###########################################
    def commit_adr(self, file: str) -> None:
        adr_path = Path(file)
        self._verify_adr_staged(adr_path)
        self._commit_adr(adr_path)

    ###########################################
    # GENERATE TOC
    ###########################################
    def generate_toc(self, pre_checks: bool = True) -> Path:
        toc_path = super().generate_toc()
        self.repo.index.add([str(toc_path)])
        return toc_path

    ###########################################
    # HELPER FUNCTIONS
    ###########################################
    def print_commit_message(self, file: str) -> None:
        logger.info(self._commit_message_for_adr(Path(file)))

    def print_branch_title(self, file: str) -> None:
        logger.info(self._branch_title_from_file(Path(file)))

    def _branch_title_from_file(self, adr_path: Path) -> str:
        self._verify_adr_filename(adr_path)

        adr_status = adr_status_from_file(adr_path)
        if adr_status not in REVIEW_REQUESTS.keys():
            logger.error(
                "Can only create review request branches for ADR statuses: "
                f"{list(REVIEW_REQUESTS.keys())}."
            )
            raise PyadrStatusIncompatibleWithReviewRequestError(
                f"ADR: '{adr_path}'; status: '{adr_status}'."
            )

        return "-".join([REVIEW_REQUESTS[adr_status], adr_path.stem.split("-", 1)[1]])

    ###########################################
    # GIT PRE MERGE CHECKS
    ###########################################
    def git_pre_merge_checks(self) -> None:
        at_least_one_check_failed = self._check_adr_repo(check_no_proposed=True)

        if at_least_one_check_failed:
            raise PyadrGitPreMergeChecksFailedError
        else:
            logger.info("All checks passed.")

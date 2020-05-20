from pathlib import Path

from git import Repo
from loguru import logger
from slugify import slugify

from pyadr.const import REVIEW_REQUESTS
from pyadr.content_utils import adr_status_from_file
from pyadr.core import AdrCore
from pyadr.exceptions import PyadrStatusIncompatibleWithReviewRequestError
from pyadr.git.const import GIT_ADR_DEFAULT_SETTINGS, PROPOSAL_REQUEST
from pyadr.git.exceptions import (
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
        super().__init__(GIT_ADR_DEFAULT_SETTINGS)
        self._repo = None

    ###########################################
    # PROPERTIES
    ###########################################
    @property
    def commit_message_prefix(self) -> str:
        if self.config.getboolean("adr-only-repo"):
            return "feat(adr):"
        else:
            return "docs(adr):"

    @property
    def repo(self) -> Repo:
        if not self._repo:
            self._repo = get_verified_repo_client(Path.cwd())
        return self._repo

    ###########################################
    # GIT INIT ADR
    ###########################################
    def git_init_adr_repo(self, force: bool = False) -> None:
        verify_index_empty(self.repo)

        init_branch_name = "adr-init-repo"
        verify_branch_does_not_exist(self.repo, init_branch_name)

        created_files = self.init_adr_repo(force=force)

        if "master" not in self.repo.heads:
            logger.info("Git repo empty. Will commit files to 'master'.")
        else:
            create_feature_branch_and_checkout(self.repo, init_branch_name)

        self.repo.index.add([str(p) for p in created_files])

        message = f"{self.commit_message_prefix} initialise adr repository"
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
            verify_main_branch_exists(self.repo, branch="master")

        logger.info("Switching to 'master'...")
        self.repo.heads.master.checkout()
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
        self, status: str, toc: bool = False, commit: bool = False,
    ) -> None:
        processed_adr = self.accept_or_reject(status, toc)

        if commit:
            self.repo.index.commit(
                self._commit_message_from_filepath(processed_adr, status)
            )

    def _commit_message_from_filepath(self, adr_path: Path, status: str) -> str:
        return f"{self.commit_message_prefix} [{status}] {adr_path.stem}"

    def _commit_message_from_file(self, adr_path: Path) -> str:
        self._verify_adr_filename_correct(adr_path)

        return (
            f"{self.commit_message_prefix} "
            f"[{adr_status_from_file(adr_path)}] "
            f"{adr_path.stem}"
        )

    def _verify_proposed_adr(self):
        proposed_adr = super()._verify_proposed_adr()
        self._verify_file_staged_or_committed(proposed_adr)
        return proposed_adr

    def _verify_file_staged_or_committed(
        self, path: Path, print_error_message: bool = True
    ) -> None:
        file_staged = str(path) in [d.a_path for d in self.repo.index.diff("HEAD")]
        file_committed = str(path) in list(self.repo.head.commit.stats.files.keys())
        if not (file_staged or file_committed):
            if print_error_message:
                logger.error(f"File {path} should be staged or committed first.")
            raise PyadrGitAdrNotStagedOrCommittedError(path)

    def _apply_filepath_update(self, path: Path, renamed_path: Path) -> None:
        logger.debug("_apply_filepath_update")
        try:
            self._verify_file_staged_or_committed(path, print_error_message=False)
        except PyadrGitAdrNotStagedOrCommittedError:
            logger.debug("not staged or committed")
            super()._apply_filepath_update(path, renamed_path)
            self.repo.index.add([str(renamed_path)])
        else:
            logger.debug("staged or committed")
            self.repo.git.mv(str(path), str(renamed_path))

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
        logger.info(self._commit_message_from_file(Path(file)))

    def print_branch_title(self, file: str) -> None:
        logger.info(self._branch_title_from_file(Path(file)))

    def _branch_title_from_file(self, adr_path: Path) -> str:
        self._verify_adr_filename_correct(adr_path)

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

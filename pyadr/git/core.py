from pathlib import Path

from git import Repo
from loguru import logger
from slugify import slugify

from pyadr.core import AdrCore
from pyadr.git.const import GIT_ADR_DEFAULT_SETTINGS
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
    def commit_msg_prefix(self) -> str:
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

        message = f"{self.commit_msg_prefix} initialise adr repository"
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
            self.verify_adr_dir_exists()
            verify_main_branch_exists(self.repo, branch="master")

        verify_index_empty(self.repo)

        adr_branch_name = f"adr-{slugify(title)}"
        verify_branch_does_not_exist(self.repo, adr_branch_name)

        new_adr_path = self.new_adr(title, pre_checks=False)

        create_feature_branch_and_checkout(self.repo, adr_branch_name)

        self.repo.index.add([str(new_adr_path)])

        logger.info(f"File '{new_adr_path}' staged.")

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
                f"{self.commit_msg_prefix} [{status}] {processed_adr.stem}"
            )

    def _verify_proposed_adr(self):
        proposed_adr = super()._verify_proposed_adr()
        self._verify_file_staged_or_committed(proposed_adr)
        return proposed_adr

    def _verify_file_staged_or_committed(self, path: Path) -> None:
        file_staged = str(path) in [
            d.a_path
            for d in list(
                self.repo.index.diff(self.repo.head.commit).iter_change_type("D")
            )
        ]
        file_committed = str(path) in list(self.repo.head.commit.stats.files.keys())
        if not (file_staged or file_committed):
            logger.error(f"File {path} should be staged or committed first.")
            raise PyadrGitAdrNotStagedOrCommittedError(path)

    def _apply_filepath_update(self, path: Path, renamed_path: Path) -> None:
        self.repo.git.mv(str(path), str(renamed_path))

    ###########################################
    # GENERATE TOC
    ###########################################
    def generate_toc(self, pre_checks: bool = True) -> Path:
        toc_path = super().generate_toc()
        self.repo.index.add([str(toc_path)])
        return toc_path

    ###########################################
    # GIT PRE MERGE CHECKS
    ###########################################
    def git_pre_merge_checks(self) -> None:
        at_least_one_check_failed = self._check_adr_repo(check_no_proposed=True)

        if at_least_one_check_failed:
            raise PyadrGitPreMergeChecksFailedError
        else:
            logger.info("All checks passed.")

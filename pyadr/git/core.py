from pathlib import Path

from loguru import logger

from pyadr.content_utils import adr_title_slug
from pyadr.core import AdrCore
from pyadr.git.const import GIT_ADR_DEFAULT_SETTINGS
from pyadr.git.utils import (
    create_feature_branch_and_checkout,
    get_verified_repo,
    verify_branch_does_not_exist,
    verify_index_empty,
    verify_main_branch_exists,
)


class GitAdrCore(AdrCore):
    def __init__(self):
        super().__init__(GIT_ADR_DEFAULT_SETTINGS)

    ###########################################
    # PROPERTIES
    ###########################################
    @property
    def commit_msg_prefix(self) -> str:
        if self.config.getboolean("adr-only-repo"):
            return "feat(adr):"
        else:
            return "docs(adr):"

    ###########################################
    # GIT INIT ADR
    ###########################################
    def git_init_adr_repo(self, force: bool = False) -> None:
        repo = get_verified_repo(Path.cwd())

        verify_index_empty(repo)

        init_branch_name = "adr-init-repo"
        verify_branch_does_not_exist(repo, init_branch_name)

        created_files = self.init_adr_repo(force=force)

        if "master" not in repo.heads:
            logger.info("Git repo empty. Will commit files to 'master'.")
        else:
            create_feature_branch_and_checkout(repo, init_branch_name)

        repo.index.add([str(p) for p in created_files])

        message = f"{self.commit_msg_prefix} initialise adr repository"
        repo.index.commit(message)

        logger.info(
            f"Files committed to branch '{repo.head.ref.name}' "
            f"with commit message '{message}'."
        )
        logger.info("ADR Git repo initialised.")

    ###########################################
    # GIT NEW ADR
    ###########################################
    def git_new_adr(self, title: str, pre_checks: bool = True) -> None:
        repo = get_verified_repo(Path.cwd())

        if pre_checks:
            self.verify_adr_dir_exists()
            verify_main_branch_exists(repo, branch="master")

        verify_index_empty(repo)

        adr_branch_name = f"adr-{adr_title_slug(title)}"
        verify_branch_does_not_exist(repo, adr_branch_name)

        new_adr_path = self.new_adr(title, pre_checks=False)

        create_feature_branch_and_checkout(repo, adr_branch_name)

        repo.index.add([str(new_adr_path)])

        logger.info(f"File '{new_adr_path}' staged.")

        logger.info("New ADR added to Git repo.")

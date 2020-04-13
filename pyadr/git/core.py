from pathlib import Path

from loguru import logger

from pyadr.content_utils import adr_title_slug
from pyadr.core import init_adr_repo, new_adr
from pyadr.git.utils import (
    create_feature_branch_and_checkout,
    get_verified_repo,
    verify_branch_does_not_exist,
    verify_index_empty,
    verify_main_branch_exists,
)
from pyadr.utils import verify_adr_dir_exists


###########################################
# GIT INIT ADR
###########################################
def git_init_adr_repo(repo_workdir: Path, force: bool = False) -> None:
    repo = get_verified_repo(repo_workdir)

    verify_index_empty(repo)

    init_branch_name = "adr-init-repo"
    verify_branch_does_not_exist(repo, init_branch_name)

    created_files = init_adr_repo(force=force)

    if "master" not in repo.heads:
        logger.info("Git repo empty. Will commit files to 'master'.")
    else:
        create_feature_branch_and_checkout(repo, init_branch_name)

    repo.index.add([str(p) for p in created_files])

    message = "feat(adr): initialise adr repository"
    repo.index.commit(message)

    logger.info(
        f"Files committed to branch '{repo.head.ref.name}' "
        f"with commit message '{message}'."
    )
    logger.info("ADR Git repo initialised.")


###########################################
# GIT NEW ADR
###########################################
def git_new_adr(repo_workdir: Path, title: str, pre_checks: bool = True) -> None:
    repo = get_verified_repo(repo_workdir)

    if pre_checks:
        verify_adr_dir_exists()
        verify_main_branch_exists(repo, branch="master")

    verify_index_empty(repo)

    adr_branch_name = f"adr-{adr_title_slug(title)}"
    verify_branch_does_not_exist(repo, adr_branch_name)

    new_adr_path = new_adr(title, pre_checks=False)

    create_feature_branch_and_checkout(repo, adr_branch_name)

    repo.index.add([str(new_adr_path)])

    logger.info(f"File '{new_adr_path}' staged.")

    logger.info("New ADR added to Git repo.")

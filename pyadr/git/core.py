from pathlib import Path

from git import BadName, InvalidGitRepositoryError, Repo
from loguru import logger

from pyadr.core import init_adr_repo
from pyadr.exceptions import (
    PyadrGitBranchAlreadyExistsError,
    PyadrGitIndexNotEmptyError,
    PyadrInvalidGitRepositoryError,
)


def git_init_adr_repo(repo_workdir: Path, force: bool = False) -> None:
    repo = get_verified_repo(repo_workdir)

    verify_index_empty(repo)

    init_branch_name = "adr-init-repo"
    verify_branch_does_not_exist(repo, init_branch_name)

    created_files = init_adr_repo(force=force)

    if "master" not in repo.heads:
        logger.info("Git repo empty. Will commit files to 'master'.")
    else:
        logger.info(f"Switching to 'master'.")
        repo.heads.master.checkout()

        logger.info(f"Creating branch '{init_branch_name}'...")
        repo.create_head(init_branch_name)
        repo.heads[init_branch_name].checkout()
        logger.info(f"... done.")

    repo.index.add([str(p) for p in created_files])

    message = "feat(adr): initialise adr repository"
    repo.index.commit(message)

    logger.info(
        f"Files committed to branch '{repo.head.ref.name}' "
        f"with commit message '{message}'."
    )
    logger.info("ADR Git repo initialised.")


def get_verified_repo(repo_workdir: Path) -> Repo:
    try:
        repo = Repo(repo_workdir)
    except InvalidGitRepositoryError as e:
        logger.error(
            f"No Git repository found in directory '{repo_workdir}/'. "
            f"Please initialise a Git repository before running command."
        )
        raise PyadrInvalidGitRepositoryError(e)
    return repo


def verify_index_empty(repo: Repo) -> None:
    logger.info("Verifying Git index is empty...")
    try:
        count_staged_files = len(repo.index.diff("HEAD"))
    except BadName:
        # HEAD does not exist => the repo is empty, so must verify index is too
        count_staged_files = len(list(repo.index.iter_blobs()))

    if count_staged_files > 0:
        logger.error("... files staged in Git index. Clean before running command.")
        raise PyadrGitIndexNotEmptyError()

    logger.info("... done.")


def verify_branch_does_not_exist(repo: Repo, branch: str) -> None:
    logger.info(f"Verifying branch '{branch}' does not exist... ")
    if "master" not in repo.heads or branch not in repo.heads:
        logger.info("... does not exist.")
    else:
        logger.error(
            f"... branch '{branch}' already exists. Clean before running command."
        )
        raise PyadrGitBranchAlreadyExistsError(branch)

from pathlib import Path
from typing import List

from git import Commit, InvalidGitRepositoryError, Repo  # type: ignore[attr-defined]
from gitdb.exc import BadName
from loguru import logger

from pyadr.git.exceptions import (
    PyadrGitBranchAlreadyExistsError,
    PyadrGitIndexNotEmptyError,
    PyadrGitMainBranchDoesNotExistError,
    PyadrInvalidGitRepositoryError,
)


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

    logger.log("VERBOSE", "... done.")


def verify_branch_does_not_exist(repo: Repo, branch: str) -> None:
    logger.info(f"Verifying branch '{branch}' does not exist...")
    if "main" not in repo.heads or branch not in repo.heads:
        logger.log("VERBOSE", "... done.")
    else:
        logger.error(
            f"... branch '{branch}' already exists. Clean before running command."
        )
        raise PyadrGitBranchAlreadyExistsError(branch)


def verify_main_branch_exists(repo: Repo, branch: str = "main") -> None:
    logger.info(f"Verifying branch '{branch}' exists... ")
    if branch in repo.heads:
        logger.log("VERBOSE", "... done.")
    else:
        message = (
            "... branch '{branch}' does not exist. {supplement}"
            "Correct before running command."
        )
        if branch == "main":
            supplement = ""
        else:
            supplement = "Your repo is empty or it was deleted. "
        logger.error(message.format(branch=branch, supplement=supplement))
        raise PyadrGitMainBranchDoesNotExistError(branch)


def get_verified_repo_client(repo_workdir: Path) -> Repo:
    try:
        repo = Repo(repo_workdir)
    except InvalidGitRepositoryError as e:
        logger.error(
            f"No Git repository found in directory '{repo_workdir}/'. "
            f"Please initialise a Git repository before running command."
        )
        raise PyadrInvalidGitRepositoryError(e)
    return repo


def create_feature_branch_and_checkout(repo: Repo, branch_name: str) -> None:
    logger.info("Switching to 'main'...")
    repo.heads.main.checkout()
    logger.log("VERBOSE", "... done.")

    logger.info(f"Creating branch '{branch_name}' and switching to it...")
    repo.create_head(branch_name)
    repo.heads[branch_name].checkout()
    logger.log("VERBOSE", "... done.")


def files_committed_in_commit(commit: Commit) -> List:
    return list(commit.stats.files.keys())

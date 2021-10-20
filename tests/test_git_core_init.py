from git import Repo
from hamcrest import assert_that, calling, not_, raises

from pyadr.git.exceptions import (
    PyadrGitBranchAlreadyExistsError,
    PyadrGitMainBranchDoesNotExistError,
)
from pyadr.git.utils import verify_branch_does_not_exist, verify_main_branch_exists


def test_verify_branch_does_not_exist_empty_repo(tmp_path):
    # Given
    repo = Repo.init(tmp_path)
    # When
    # Then
    assert_that(
        calling(verify_branch_does_not_exist).with_args(repo, "main"),
        not_(raises(PyadrGitBranchAlreadyExistsError)),
    )
    assert_that(
        calling(verify_branch_does_not_exist).with_args(repo, "my-branch"),
        not_(raises(PyadrGitBranchAlreadyExistsError)),
    )


def test_verify_branch_does_not_exist_repo_fails_with_main(tmp_repo):
    # Given
    # When
    # Then
    assert_that(
        calling(verify_branch_does_not_exist).with_args(tmp_repo, "main"),
        raises(PyadrGitBranchAlreadyExistsError),
    )
    assert_that(
        calling(verify_branch_does_not_exist).with_args(tmp_repo, "my-branch"),
        not_(raises(PyadrGitBranchAlreadyExistsError)),
    )


def test_verify_branch_does_not_exist_empty_fails(tmp_repo):
    # Given
    tmp_repo.create_head("my-branch")
    # tmp_repo.heads["my-branch"].checkout()

    # When
    # Then
    assert_that(
        calling(verify_branch_does_not_exist).with_args(tmp_repo, "my-branch"),
        raises(PyadrGitBranchAlreadyExistsError),
    )


def test_verify_main_branch_exists_empty_repo(tmp_path):
    # Given
    repo = Repo.init(tmp_path)
    # When
    # Then
    assert_that(
        calling(verify_main_branch_exists).with_args(repo, "main"),
        raises(PyadrGitMainBranchDoesNotExistError),
    )


def test_verify_main_branch_exists_other_main_than_main_fail(tmp_repo):
    # Given
    # When
    # Then
    assert_that(
        calling(verify_main_branch_exists).with_args(tmp_repo, "main"),
        not_(raises(PyadrGitBranchAlreadyExistsError)),
    )
    assert_that(
        calling(verify_main_branch_exists).with_args(tmp_repo, "non-existing-branch"),
        raises(PyadrGitMainBranchDoesNotExistError),
    )


def test_verify_main_branch_exists_other_main_than_main_pass(tmp_repo):
    # Given
    tmp_repo.create_head("other-main-branch")

    # When
    # Then
    assert_that(
        calling(verify_main_branch_exists).with_args(tmp_repo, "other-main-branch"),
        not_(raises(PyadrGitMainBranchDoesNotExistError)),
    )

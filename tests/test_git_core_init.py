from git import Repo
from hamcrest import assert_that, calling, not_, raises

from pyadr.exceptions import PyadrGitBranchAlreadyExistsError
from pyadr.git.core import verify_branch_does_not_exist


def test_verify_branch_does_not_exist_empty_repo(tmp_path):
    # Given
    repo = Repo.init(tmp_path)
    # When
    # Then
    assert_that(
        calling(verify_branch_does_not_exist).with_args(repo, "master"),
        not_(raises(PyadrGitBranchAlreadyExistsError)),
    )
    assert_that(
        calling(verify_branch_does_not_exist).with_args(repo, "my-branch"),
        not_(raises(PyadrGitBranchAlreadyExistsError)),
    )


def test_verify_branch_does_not_exist_repo_fails_with_master(tmp_repo):
    # Given
    # When
    # Then
    assert_that(
        calling(verify_branch_does_not_exist).with_args(tmp_repo, "master"),
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

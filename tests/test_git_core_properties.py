from hamcrest import assert_that, equal_to


def test_commit_msg_prefix_for_adr_only_repo(git_adr_core):
    # Given
    git_adr_core.config["adr-only-repo"] = "true"

    # When
    # Then
    assert_that(git_adr_core.commit_msg_prefix, equal_to("feat(adr):"))


def test_commit_msg_prefix_for_project_repo(git_adr_core):
    # Given
    git_adr_core.config["adr-only-repo"] = "false"

    # When
    # Then
    assert_that(git_adr_core.commit_msg_prefix, equal_to("docs(adr):"))

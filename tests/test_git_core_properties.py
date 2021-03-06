from hamcrest import assert_that, equal_to


def test_commit_msg_default_prefix_for_adr_only_repo(git_adr_core):
    # Given
    git_adr_core.config["git"]["adr-only-repo"] = "true"

    # When
    # Then
    assert_that(git_adr_core.commit_message_default_prefix, equal_to("feat(adr):"))


def test_commit_msg_default_prefix_for_project_repo(git_adr_core):
    # Given
    git_adr_core.config["git"]["adr-only-repo"] = "false"

    # When
    # Then
    assert_that(git_adr_core.commit_message_default_prefix, equal_to("docs(adr):"))

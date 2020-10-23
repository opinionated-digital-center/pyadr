from hamcrest import assert_that, equal_to, not_


def test_adr_commit_msg_prefix_for_status_proposed(git_adr_core):
    # Given
    # When
    # Then
    assert_that(
        git_adr_core._commit_message_prefix_for_status("proposed"),
        equal_to("chore(adr):"),
    )


def test_adr_commit_msg_prefix_for_status_other_than_proposed(git_adr_core):
    # Given
    # When
    # Then
    assert_that(
        git_adr_core._commit_message_prefix_for_status(""),
        not_(equal_to("chore(adr):")),
    )

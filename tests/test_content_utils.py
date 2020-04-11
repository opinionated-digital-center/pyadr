from datetime import datetime
from io import StringIO

import pytest
from hamcrest import assert_that, contains_string, equal_to, none, not_

from pyadr import content_utils
from pyadr.content_utils import (
    adr_title_slug_from_content_stream,
    retrieve_title_status_and_date_from_madr_content_stream,
)


@pytest.fixture()
def sample_adr_content():
    yield """<!-- comment -->
# [short title of solved problem and solution]

* Status: any_status
* Date: any_date

## Context and Problem Statement

[..]
"""


def test_update_adr_content_date(sample_adr_content):
    # Given

    # When
    today = datetime.today().strftime("%Y-%m-%d")
    result_text = content_utils.update_adr_content_title_status(
        sample_adr_content, status="another_status"
    )

    # Then
    assert_that(result_text, not_(contains_string("\n* Date: any_date\n")))
    assert_that(result_text, contains_string(f"\n* Date: {today}\n"))


def test_update_adr_content_title(sample_adr_content):
    # Given

    # When
    result_text = content_utils.update_adr_content_title_status(
        sample_adr_content, "My New Title"
    )

    # Then
    assert_that(
        result_text,
        not_(contains_string("\n# [short title of solved problem and solution]\n")),
    )
    assert_that(result_text, contains_string("\n# My New Title\n"))


def test_update_adr_content_status(sample_adr_content):
    # Given

    # When
    result_text = content_utils.update_adr_content_title_status(
        sample_adr_content, status="another_status"
    )

    # Then
    assert_that(result_text, not_(contains_string("\n* Status: any_status\n")))
    assert_that(result_text, contains_string("\n* Status: another_status\n"))


def test_get_adr_title_slug_from_content_stream():
    # Given
    adr_content = """#  My ADR Updated Title

* Status: any_status
* Date: any_date

## Context and Problem Statement

[..]
"""
    # When
    title_slug = adr_title_slug_from_content_stream(StringIO(adr_content))

    # Then
    assert_that(title_slug, equal_to("my-adr-updated-title"))


def test_retrieve_title_status_and_date_from_madr_content():
    # Given
    adr_content = """<!-- comment -->
#  My ADR Updated Title

* Status: any_status status phrase
* Date: any_date

## Context and Problem Statement

[..]
"""
    # When
    (
        title,
        (status, status_phrase),
        date,
    ) = retrieve_title_status_and_date_from_madr_content_stream(StringIO(adr_content))

    # Then
    assert_that(title, equal_to("My ADR Updated Title"))
    assert_that(status, equal_to("any_status"))
    assert_that(status_phrase, equal_to("status phrase"))
    assert_that(date, equal_to("any_date"))


def test_retrieve_title_status_and_date_from_madr_content_when_no_status_phrase(
    sample_adr_content,
):
    # Given

    # When
    (
        title,
        (status, status_phrase),
        date,
    ) = retrieve_title_status_and_date_from_madr_content_stream(
        StringIO(sample_adr_content)
    )

    # Then
    assert_that(title, equal_to("[short title of solved problem and solution]"))
    assert_that(status, equal_to("any_status"))
    assert_that(status_phrase, none())
    assert_that(date, equal_to("any_date"))

from datetime import datetime
from io import StringIO

import pytest
from hamcrest import assert_that, contains_string, equal_to, none, not_

from pyadr import text_utils
from pyadr.const import STATUS_ACCEPTED, STATUS_REJECTED
from pyadr.text_utils import (
    find_title_status_and_date_in_madr_content,
    get_adr_title_slug_from_stream,
)


@pytest.fixture()
def source_adr_text():
    yield """# [short title of solved problem and solution]

* Status: any_status
* Date: any_date

## Context and Problem Statement

[..]
"""


def test_date_changed_when_change_adr_str_content_to_status(source_adr_text):
    # Given

    # When
    today = datetime.today().strftime("%Y-%m-%d")
    result_text = text_utils.change_adr_text_to_status(
        source_adr_text, "another_status"
    )

    # Then
    assert_that(result_text, not_(contains_string("\n* Date: any_date\n")))
    assert_that(result_text, contains_string(f"\n* Date: {today}\n"))


def test_status_changed_when_change_adr_str_content_to_status(source_adr_text):
    # Given

    # When
    result_text = text_utils.change_adr_text_to_status(
        source_adr_text, "another_status"
    )

    # Then
    assert_that(result_text, not_(contains_string("\n* Status: any_status\n")))
    assert_that(result_text, contains_string("\n* Status: another_status\n"))


def test_status_changed_when_change_adr_str_content_to_accepted(source_adr_text):
    # Given

    # When
    result_text = text_utils.change_adr_text_to_accepted(source_adr_text)

    # Then
    assert_that(result_text, not_(contains_string("\n* Status: any_status\n")))
    assert_that(result_text, contains_string(f"\n* Status: {STATUS_ACCEPTED}\n"))


def test_status_changed_when_change_adr_str_content_to_rejected(source_adr_text):
    # Given

    # When
    result_text = text_utils.change_adr_text_to_rejected(source_adr_text)

    # Then
    assert_that(result_text, not_(contains_string("\n* Status: any_status\n")))
    assert_that(result_text, contains_string(f"\n* Status: {STATUS_REJECTED}\n"))


def test_get_adr_title_slug_from_stream():
    # Given
    adr_content = """#  My ADR Updated Title

* Status: any_status
* Date: any_date

## Context and Problem Statement

[..]
"""
    stream = StringIO(adr_content)

    # When
    title_slug = get_adr_title_slug_from_stream(stream)

    # Then
    assert_that(title_slug, equal_to("my-adr-updated-title"))


def test_find_title_status_and_date_in_madr_content():
    # Given
    adr_content = """<!-- comment -->
#  My ADR Updated Title

* Status: any_status status phrase
* Date: any_date

## Context and Problem Statement

[..]
"""
    stream = StringIO(adr_content)

    # When
    title, (status, status_phrase), date = find_title_status_and_date_in_madr_content(
        stream
    )

    # Then
    assert_that(title, equal_to("My ADR Updated Title"))
    assert_that(status, equal_to("any_status"))
    assert_that(status_phrase, equal_to("status phrase"))
    assert_that(date, equal_to("any_date"))


def test_find_title_status_and_date_in_madr_content_when_no_status_phrase():
    # Given
    adr_content = """<!-- comment -->
#  My ADR Updated Title

* Status:   any_status
* Date:   any_date

## Context and Problem Statement

[..]
"""
    stream = StringIO(adr_content)

    # When
    title, (status, status_phrase), date = find_title_status_and_date_in_madr_content(
        stream
    )

    # Then
    assert_that(title, equal_to("My ADR Updated Title"))
    assert_that(status, equal_to("any_status"))
    assert_that(status_phrase, none())
    assert_that(date, equal_to("any_date"))

from datetime import datetime

import pytest
from hamcrest import assert_that, calling, contains_string, equal_to, none, not_, raises

from pyadr import content_utils
from pyadr.content_utils import (
    adr_title_slug_from_file,
    build_toc_content_from_adrs_by_status,
    retrieve_title_status_and_date_from_madr,
)
from pyadr.exceptions import (
    PyadrAdrDateNotFoundError,
    PyadrAdrStatusNotFoundError,
    PyadrAdrTitleNotFoundError,
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


@pytest.fixture()
def sample_adr_path(adr_tmp_path, sample_adr_content):
    sample_adr_path = adr_tmp_path / "sample_adr"
    with sample_adr_path.open("w") as f:
        f.write(sample_adr_content)
    yield sample_adr_path


def test_update_adr_content_date(sample_adr_content):
    # Given

    # When
    today = datetime.today().strftime("%Y-%m-%d")
    result_text = content_utils.update_adr_content_status(
        sample_adr_content, "another_status"
    )

    # Then
    assert_that(result_text, not_(contains_string("\n* Date: any_date\n")))
    assert_that(result_text, contains_string(f"\n* Date: {today}\n"))


def test_update_adr_content_title(sample_adr_content):
    # Given

    # When
    result_text = content_utils.update_adr_content_title(
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
    result_text = content_utils.update_adr_content_status(
        sample_adr_content, "another_status"
    )

    # Then
    assert_that(result_text, not_(contains_string("\n* Status: any_status\n")))
    assert_that(result_text, contains_string("\n* Status: another_status\n"))


def test_get_adr_title_slug_from_content_stream(adr_tmp_path):
    # Given
    adr_content = """#  My ADR Updated Title

* Status: any_status
* Date: any_date

## Context and Problem Statement

[..]
"""
    adr_path = adr_tmp_path / "sample_adr"
    with adr_path.open("w") as f:
        f.write(adr_content)

    # When
    title_slug = adr_title_slug_from_file(adr_path)

    # Then
    assert_that(title_slug, equal_to("my-adr-updated-title"))


def test_retrieve_title_status_and_date_from_madr(adr_tmp_path):
    # Given
    adr_content = """<!-- comment -->
#  My ADR Updated Title

* Status: any_status status phrase
* Date: any_date

## Context and Problem Statement

[..]
"""
    adr_path = adr_tmp_path / "sample_adr"
    with adr_path.open("w") as f:
        f.write(adr_content)

    # When
    (title, (status, status_phrase), date,) = retrieve_title_status_and_date_from_madr(
        adr_path
    )

    # Then
    assert_that(title, equal_to("My ADR Updated Title"))
    assert_that(status, equal_to("any_status"))
    assert_that(status_phrase, equal_to("status phrase"))
    assert_that(date, equal_to("any_date"))


def test_retrieve_title_status_and_date_from_madr_when_no_status_phrase(
    sample_adr_path,
):
    # Given

    # When
    (title, (status, status_phrase), date,) = retrieve_title_status_and_date_from_madr(
        sample_adr_path
    )

    # Then
    assert_that(title, equal_to("[short title of solved problem and solution]"))
    assert_that(status, equal_to("any_status"))
    assert_that(status_phrase, none())
    assert_that(date, equal_to("any_date"))


def test_retrieve_title_status_and_date_from_madr_throws_error_when_no_title(
    adr_tmp_path,
):
    # Given
    adr_content = """
* Status: any_status status phrase
* Date: any_date

## Context and Problem Statement

[..]
"""
    adr_path = adr_tmp_path / "sample_adr"
    with adr_path.open("w") as f:
        f.write(adr_content)

    # When
    # Then
    assert_that(
        calling(retrieve_title_status_and_date_from_madr).with_args(adr_path),
        raises(PyadrAdrTitleNotFoundError),
    )


def test_retrieve_title_status_and_date_from_madr_throws_error_when_no_status(
    adr_tmp_path,
):
    # Given
    adr_content = """
#  My ADR Updated Title

* Date: any_date

## Context and Problem Statement

[..]
"""
    adr_path = adr_tmp_path / "sample_adr"
    with adr_path.open("w") as f:
        f.write(adr_content)

    # When
    # Then
    assert_that(
        calling(retrieve_title_status_and_date_from_madr).with_args(adr_path),
        raises(PyadrAdrStatusNotFoundError),
    )


def test_retrieve_title_status_and_date_from_madr_throws_error_when_no_date(
    adr_tmp_path,
):
    # Given
    adr_content = """
#  My ADR Updated Title

* Status: any_status status phrase

## Context and Problem Statement

[..]
"""
    adr_path = adr_tmp_path / "sample_adr"
    with adr_path.open("w") as f:
        f.write(adr_content)

    # When
    # Then
    assert_that(
        calling(retrieve_title_status_and_date_from_madr).with_args(adr_path),
        raises(PyadrAdrDateNotFoundError),
    )


def test_build_toc_content_from_adrs_by_status():
    # Given
    adrs_by_status = {
        "accepted": {
            "status-title": "Accepted Records",
            "adrs": ["* [ADR Title](adr.md)\n", "* [ADR Title](adr.md)\n"],
        },
        "rejected": {
            "status-title": "Rejected Records",
            "adrs": ["* [ADR Title](adr.md)\n"],
        },
        "superseded": {
            "status-title": "Superseded Records",
            "adrs": ["* [ADR Title](adr.md)\n"],
        },
        "deprecated": {
            "status-title": "Deprecated Records",
            "adrs": ["* [ADR Title](adr.md)\n"],
        },
        "non-standard": {
            "status-title": "Records with non-standard statuses",
            "adrs-by-status": {
                "foo": {
                    "status-title": "Status `foo`",
                    "adrs": ["* [ADR Title](adr.md)\n"],
                },
                "bar": {
                    "status-title": "Status `bar`",
                    "adrs": ["* [ADR Title](adr.md)\n"],
                },
            },
        },
    }

    # When
    toc_content = build_toc_content_from_adrs_by_status(adrs_by_status)

    # Then
    expected = [
        "<!-- This file has been generated by `pyadr`. Manual changes will be erased "
        "at next generation. -->\n",
        "# Architecture Decision Records\n",
        "\n",
        "## Accepted Records\n",
        "\n",
        "* [ADR Title](adr.md)\n",
        "* [ADR Title](adr.md)\n",
        "\n",
        "## Rejected Records\n",
        "\n",
        "* [ADR Title](adr.md)\n",
        "\n",
        "## Superseded Records\n",
        "\n",
        "* [ADR Title](adr.md)\n",
        "\n",
        "## Deprecated Records\n",
        "\n",
        "* [ADR Title](adr.md)\n",
        "\n",
        "## Records with non-standard statuses\n",
        "\n",
        "### Status `foo`\n",
        "\n",
        "* [ADR Title](adr.md)\n",
        "\n",
        "### Status `bar`\n",
        "\n",
        "* [ADR Title](adr.md)\n",
    ]
    assert_that(toc_content, equal_to(expected))


def test_build_toc_content_from_adrs_by_status_no_adr():
    # Given
    adrs_by_status = {
        "accepted": {"status-title": "Accepted Records", "adrs": []},
        "rejected": {"status-title": "Rejected Records", "adrs": []},
        "superseded": {"status-title": "Superseded Records", "adrs": []},
        "deprecated": {"status-title": "Deprecated Records", "adrs": []},
        "non-standard": {
            "status-title": "Records with non-standard statuses",
            "adrs-by-status": {},
        },
    }

    # When
    toc_content = build_toc_content_from_adrs_by_status(adrs_by_status)

    # Then
    expected = [
        "<!-- This file has been generated by `pyadr`. Manual changes will be erased "
        "at next generation. -->\n",
        "# Architecture Decision Records\n",
        "\n",
        "## Accepted Records\n",
        "\n",
        "* None\n",
        "\n",
        "## Rejected Records\n",
        "\n",
        "* None\n",
        "\n",
        "## Superseded Records\n",
        "\n",
        "* None\n",
        "\n",
        "## Deprecated Records\n",
        "\n",
        "* None\n",
        "\n",
        "## Records with non-standard statuses\n",
        "\n",
        "* None\n",
    ]
    assert_that(toc_content, equal_to(expected))

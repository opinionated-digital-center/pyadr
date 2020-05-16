from hamcrest import assert_that, calling, equal_to, raises

from pyadr.core import AdrCore
from pyadr.exceptions import PyadrNoNumberedAdrError
from pyadr.file_utils import calculate_next_adr_id


def test_add_id_and_update_title_on_proposed_adr_file_name(adr_tmp_path):
    # Given
    adr_file = adr_tmp_path / "XXXX-adr-title.md"
    with adr_file.open("w") as f:
        f.write(
            """# My ADR Updated Title

* Status: any_status
* Date: any_date

## Context and Problem Statement

[..]
"""
        )

    # When
    result_file = AdrCore()._update_adr_filename(adr_file, "0002")

    # Then
    expected_file = adr_tmp_path / "0002-my-adr-updated-title.md"
    assert_that(result_file, equal_to(expected_file))


def test_determine_next_id(adr_tmp_path):
    # Given
    (adr_tmp_path / "0001-a-reviewed-adr.md").touch()
    (adr_tmp_path / "0002-a-reviewed-adr.md").touch()
    (adr_tmp_path / "XXXX-a-proposed-adr.md").touch()

    # When
    next_id = calculate_next_adr_id(adr_tmp_path)

    # Then
    assert_that(next_id, equal_to("0003"))


def test_determine_next_id_fail_when_no_previous_adr(adr_tmp_path):
    # Given
    (adr_tmp_path / "XXXX-a-proposed-adr.md").touch()

    # When

    # Then
    assert_that(
        calling(calculate_next_adr_id).with_args(adr_tmp_path),
        raises(PyadrNoNumberedAdrError),
    )

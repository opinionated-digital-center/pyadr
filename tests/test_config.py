from hamcrest import assert_that, equal_to

from pyadr.config import config
from pyadr.const import DEFAULT_ADR_PATH
from pyadr.core import configure, unset_config_item


def test_config_write(tmp_path):
    # Given
    adr_ini_path = tmp_path / ".adr"

    # When
    config["records_dir"] = "doc/adr"
    config.parser.write()

    # Then
    with adr_ini_path.open() as f:
        content = f.read()

    expected = """[adr]
records_dir = doc/adr

"""
    assert_that(content, equal_to(expected))


def test_config_defaults():
    # Given
    # When
    # Then
    assert_that(config["records_dir"], equal_to(str(DEFAULT_ADR_PATH)))


def test_config_configure():
    # Given
    # When
    configure("records_dir", "another")
    # Then
    assert_that(config["records_dir"], equal_to("another"))


def test_config_unset():
    # Given
    config["records_dir"] = "another"

    # When
    unset_config_item("records_dir")
    # Then
    assert_that(config["records_dir"], equal_to(str(DEFAULT_ADR_PATH)))

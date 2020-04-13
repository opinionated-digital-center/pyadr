from hamcrest import assert_that, calling, contains_string, equal_to, not_, raises

from pyadr.config import Config, config
from pyadr.const import DEFAULT_ADR_PATH
from pyadr.core import configure, unset_config_item
from pyadr.exceptions import (
    PyadrConfigFileSettingsNotSupported,
    PyadrConfigSettingNotSupported,
)


def test_config_set(tmp_path):
    # Given
    adr_ini_path = tmp_path / ".adr"

    # When
    config["records-dir"] = "doc/adr"

    # Then
    with adr_ini_path.open() as f:
        content = f.read()

    expected = """[adr]
records-dir = doc/adr

"""
    assert_that(content, equal_to(expected))


def test_config_defaults():
    # Given
    # When
    # Then
    assert_that(config["records-dir"], equal_to(str(DEFAULT_ADR_PATH)))


def test_config_configure():
    # Given
    # When
    configure("records-dir", "another")
    # Then
    assert_that(config["records-dir"], equal_to("another"))


def test_config_unset(tmp_path):
    # Given
    config["records-dir"] = "another"

    # When
    unset_config_item("records-dir")
    # Then
    assert_that(config["records-dir"], equal_to(str(DEFAULT_ADR_PATH)))

    adr_ini_path = tmp_path / ".adr"
    assert_that(adr_ini_path.exists(), equal_to(True))
    with adr_ini_path.open() as f:
        assert_that(f.read(), not_(contains_string("records-dir = ")))


def test_config_unset_fail_on_unknown_setting(tmp_path):
    # Given
    # config["unsupported_option"] = "value"

    # Then
    assert_that(
        calling(config.__delitem__).with_args("unsupported_option"),
        raises(PyadrConfigSettingNotSupported),
    )


def test_config_fail_on_unknown_setting():
    # Given
    # When
    # Then
    assert_that(
        calling(config.__setitem__).with_args("unsupported_option", "value"),
        raises(PyadrConfigSettingNotSupported),
    )


def test_config_fail_on_unknown_setting_in_config_file(tmp_path):
    # Given
    adr_ini_path = tmp_path / ".adr"
    with adr_ini_path.open("w") as f:
        f.write("[adr]\nunsupported_option = value\n\n")
    # When
    # Then
    assert_that(calling(Config), raises(PyadrConfigFileSettingsNotSupported))

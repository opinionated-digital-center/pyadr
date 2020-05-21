from hamcrest import assert_that, calling, contains_string, equal_to, not_, raises

from pyadr.config import AdrConfig
from pyadr.const import DEFAULT_ADR_PATH
from pyadr.exceptions import (
    PyadrConfigFileSettingsNotSupported,
    PyadrConfigSettingNotSupported,
)


def test_config_set(adr_core, tmp_path):
    # Given
    adr_ini_path = tmp_path / ".adr"

    # When
    adr_core.config["adr"]["records-dir"] = "doc/adr"

    # Then
    with adr_ini_path.open() as f:
        content = f.read()

    expected = """[adr]
records-dir = doc/adr

"""
    assert_that(content, equal_to(expected))


def test_config_defaults(adr_core):
    # Given
    # When
    # Then
    assert_that(adr_core.config["adr"]["records-dir"], equal_to(str(DEFAULT_ADR_PATH)))


def test_config_configure(adr_core):
    # Given
    # When
    adr_core.configure("records-dir", "another")
    # Then
    assert_that(adr_core.config["adr"]["records-dir"], equal_to("another"))


def test_config_unset(adr_core, tmp_path):
    # Given
    adr_core.config["adr"]["records-dir"] = "another"

    # When
    adr_core.unset_config_setting("records-dir")
    # Then
    assert_that(adr_core.config["adr"]["records-dir"], equal_to(str(DEFAULT_ADR_PATH)))

    adr_ini_path = tmp_path / ".adr"
    assert_that(adr_ini_path.exists(), equal_to(True))
    with adr_ini_path.open() as f:
        assert_that(f.read(), not_(contains_string("records-dir = ")))


def test_config_does_not_touch_other_config_file_sections(adr_core, tmp_path):
    # Given
    adr_ini_path = tmp_path / ".adr"
    content = """[adr]
unsupported_option = value

[other_section]
option = value

"""
    with adr_ini_path.open("w") as f:
        f.write(content)

    # When
    adr_core.config.persist()
    # Then
    with adr_ini_path.open() as f:
        result = f.read()

    expected = """[adr]

[other_section]
option = value

"""
    assert_that(result, equal_to(expected))


def test_config_unset_fail_on_unknown_setting(adr_core, tmp_path):
    # Given
    # config["unsupported_option"] = "value"

    # Then
    assert_that(
        calling(adr_core.config["adr"].__delitem__).with_args("unsupported_option"),
        raises(PyadrConfigSettingNotSupported),
    )


def test_config_fail_on_unknown_setting(adr_core):
    # Given
    # When
    # Then
    assert_that(
        calling(adr_core.config["adr"].__setitem__).with_args(
            "unsupported_option", "value"
        ),
        raises(PyadrConfigSettingNotSupported),
    )


def test_config_fail_on_unknown_setting_in_config_file(tmp_path):
    # Given
    adr_ini_path = tmp_path / ".adr"
    with adr_ini_path.open("w") as f:
        f.write("[adr]\nunsupported_option = value\n\n")
    # When
    # Then
    assert_that(
        calling(AdrConfig), raises(PyadrConfigFileSettingsNotSupported),
    )

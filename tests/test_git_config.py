from hamcrest import assert_that, calling, contains_string, equal_to, not_, raises

from pyadr.const import DEFAULT_ADR_PATH
from pyadr.exceptions import (
    PyadrConfigFileSettingsNotSupported,
    PyadrConfigSettingNotSupported,
)
from pyadr.git.config import GitAdrConfig


def test_git_config_set_adr_setting(git_adr_core, tmp_path):
    # Given
    adr_ini_path = tmp_path / ".adr"

    # When
    git_adr_core.config["adr"]["records-dir"] = "doc/adr"

    # Then
    with adr_ini_path.open() as f:
        content = f.read()

    expected = """[adr]
records-dir = doc/adr

[git]

"""
    assert_that(content, equal_to(expected))


def test_git_config_set_git_setting(git_adr_core, tmp_path):
    # Given
    adr_ini_path = tmp_path / ".adr"

    # When
    git_adr_core.config["git"]["adr-only-repo"] = "true"

    # Then
    with adr_ini_path.open() as f:
        content = f.read()

    expected = """[adr]

[git]
adr-only-repo = true

"""
    assert_that(content, equal_to(expected))


def test_git_config_git_setting_not_erased_when_update_adr_setting_with_pyadr(
    adr_core, git_adr_core, tmp_path
):
    # Given
    adr_ini_path = tmp_path / ".adr"
    git_adr_core.config["git"]["adr-only-repo"] = "true"

    # When
    git_adr_core.config["adr"]["records-dir"] = "doc/adr"

    # Then
    with adr_ini_path.open() as f:
        content = f.read()

    expected = """[adr]
records-dir = doc/adr

[git]
adr-only-repo = true

"""
    assert_that(content, equal_to(expected))


def test_git_config_adr_setting_defaults(git_adr_core):
    # Given
    # When
    # Then
    assert_that(
        git_adr_core.config["adr"]["records-dir"], equal_to(str(DEFAULT_ADR_PATH))
    )


def test_git_config_git_setting_defaults(git_adr_core):
    # Given
    # When
    # Then
    assert_that(git_adr_core.config["git"]["adr-only-repo"], equal_to("false"))


def test_git_config_configure_adr_setting(git_adr_core):
    # Given
    # When
    git_adr_core.configure("records-dir", "another")
    # Then
    assert_that(git_adr_core.config["adr"]["records-dir"], equal_to("another"))


def test_git_config_configure_git_setting(git_adr_core):
    # Given
    # When
    git_adr_core.configure("adr-only-repo", "true")
    # Then
    assert_that(git_adr_core.config["git"]["adr-only-repo"], equal_to("true"))


def test_git_config_unset_adr_setting(git_adr_core, tmp_path):
    # Given
    git_adr_core.config["adr"]["records-dir"] = "another"

    # When
    git_adr_core.unset_config_setting("records-dir")
    # Then
    assert_that(
        git_adr_core.config["adr"]["records-dir"], equal_to(str(DEFAULT_ADR_PATH))
    )

    adr_ini_path = tmp_path / ".adr"
    assert_that(adr_ini_path.exists(), equal_to(True))
    with adr_ini_path.open() as f:
        assert_that(f.read(), not_(contains_string("records-dir = ")))


def test_git_config_unset_git_setting(git_adr_core, tmp_path):
    # Given
    git_adr_core.config["git"]["adr-only-repo"] = "true"

    # When
    git_adr_core.unset_config_setting("adr-only-repo")
    # Then
    assert_that(git_adr_core.config["git"]["adr-only-repo"], equal_to("false"))

    adr_ini_path = tmp_path / ".adr"
    assert_that(adr_ini_path.exists(), equal_to(True))
    with adr_ini_path.open() as f:
        assert_that(f.read(), not_(contains_string("adr-only-repo = ")))


def test_git_config_unset_fail_on_unknown_setting(git_adr_core, tmp_path):
    # Given
    # config["unsupported_option"] = "value"

    # Then
    assert_that(
        calling(git_adr_core.config["adr"].__delitem__).with_args("unsupported_option"),
        raises(PyadrConfigSettingNotSupported),
    )
    assert_that(
        calling(git_adr_core.config["git"].__delitem__).with_args("unsupported_option"),
        raises(PyadrConfigSettingNotSupported),
    )


def test_git_config_fail_on_unknown_setting(git_adr_core):
    # Given
    # When
    # Then
    assert_that(
        calling(git_adr_core.config["adr"].__setitem__).with_args(
            "unsupported_option", "value"
        ),
        raises(PyadrConfigSettingNotSupported),
    )
    assert_that(
        calling(git_adr_core.config["git"].__setitem__).with_args(
            "unsupported_option", "value"
        ),
        raises(PyadrConfigSettingNotSupported),
    )


def test_git_config_fail_on_unknown_adr_setting_in_config_file(tmp_path):
    # Given
    adr_ini_path = tmp_path / ".adr"
    with adr_ini_path.open("w") as f:
        f.write("[adr]\nunsupported_option = value\n\n")
    # When
    # Then
    assert_that(
        calling(GitAdrConfig), raises(PyadrConfigFileSettingsNotSupported),
    )


def test_git_config_fail_on_unknown_git_setting_in_config_file(tmp_path):
    # Given
    adr_ini_path = tmp_path / ".adr"
    with adr_ini_path.open("w") as f:
        f.write("[git]\nunsupported_option = value\n\n")
    # When
    # Then
    assert_that(
        calling(GitAdrConfig), raises(PyadrConfigFileSettingsNotSupported),
    )

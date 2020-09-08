from configparser import ConfigParser
from copy import deepcopy
from typing import Dict

from pyadr.const import ADR_DEFAULT_SETTINGS, DEFAULT_CONFIG_FILE_PATH
from pyadr.exceptions import (
    PyadrConfigFileSettingsNotSupported,
    PyadrConfigSettingNotSupported,
)


class AdrConfig(ConfigParser):
    config_file_path = DEFAULT_CONFIG_FILE_PATH

    def __init__(self, defaults=None):
        if defaults:
            super().__init__(defaults=defaults)
        else:
            sorted_default_settings = {}
            for key in sorted(ADR_DEFAULT_SETTINGS.keys()):
                sorted_default_settings[key] = ADR_DEFAULT_SETTINGS[key]
            super().__init__(defaults=sorted_default_settings)

            self.section_defaults = {"adr": ADR_DEFAULT_SETTINGS}

            self.add_section("adr")

            if self.config_file_path.exists():
                self.read(self.config_file_path)

            self.check_filled_settings_supported()

    def set(self, section: str, setting: str, value: str = None) -> None:
        if section != self.default_section:  # type: ignore
            self.check_section_supports_setting(section, setting)
        super().set(section, setting, value)
        if section != self.default_section:  # type: ignore
            self.persist()

    def has_option(self, section: str, setting: str) -> bool:
        self.check_section_supports_setting(section, setting)
        return super().has_option(section, setting)

    def remove_option(self, section: str, setting: str) -> bool:
        self.check_section_supports_setting(section, setting)
        existed = super().remove_option(section, setting)
        if existed and section != self.default_section:  # type: ignore
            self.persist()
        return existed

    def configure(self, setting: str, value: str) -> None:
        setting_supported = False
        for section in self._sections.keys():  # type: ignore
            if self.section_supports_setting(section, setting):
                self[section][setting] = value
                setting_supported = True
        if not setting_supported:
            raise PyadrConfigSettingNotSupported(
                f"'{self.optionxform(setting)}' not in {list(self.defaults().keys())}"
            )

    def unset(self, setting: str) -> None:
        setting_supported = False
        for section in self._sections.keys():  # type: ignore
            if self.section_supports_setting(section, setting):
                del self[section][setting]
                setting_supported = True
        if not setting_supported:
            raise PyadrConfigSettingNotSupported(
                f"'{self.optionxform(setting)}' not in {list(self.defaults().keys())}"
            )

    def raw(self) -> Dict[str, str]:
        raw_config = {}
        for setting in self.defaults().keys():
            for section in self._sections.keys():  # type: ignore
                if self.section_supports_setting(section, setting):
                    raw_config[setting] = self[section][setting]
        return raw_config

    # def print_config_setting(self, setting: str) -> None:
    #     logger.info(f"{setting} = {self.config['adr'][setting]}")

    def persist(self) -> None:
        defaults = deepcopy(self.defaults())
        self[self.default_section] = {}  # type: ignore

        if self.config_file_path.exists():
            tmp_config = ConfigParser()
            tmp_config.read(self.config_file_path)
            tmp_config["adr"] = self["adr"]
            with self.config_file_path.open("w") as f:
                tmp_config.write(f)
        else:
            with self.config_file_path.open("w") as f:
                self.write(f)

        self[self.default_section] = defaults  # type: ignore

    def check_filled_settings_supported(self) -> None:
        messages = []
        for section in self._sections.keys():  # type: ignore
            try:
                self.check_section_supports_filled_settings(section)
            except PyadrConfigFileSettingsNotSupported as e:
                messages.append(str(e))
        if messages:
            raise PyadrConfigFileSettingsNotSupported(", ".join(messages))

    def check_section_supports_filled_settings(self, section: str) -> None:
        unsupported_settings = [
            self.optionxform(setting)
            for setting in self._sections[section].keys()  # type: ignore
            if not self.section_supports_setting(section, setting)
        ]
        if unsupported_settings:
            raise PyadrConfigFileSettingsNotSupported(
                f"{unsupported_settings} not in "
                f"{list(self.section_defaults[section].keys())}"
            )

    def check_section_supports_setting(self, section: str, setting: str) -> None:
        if not self.section_supports_setting(section, setting):
            raise PyadrConfigSettingNotSupported(
                f"'{self.optionxform(setting)}' not in "
                f"{list(self.section_defaults[section].keys())}"
            )

    def section_supports_setting(self, section: str, setting: str) -> bool:
        if section in self.section_defaults.keys():
            return self.optionxform(setting) in self.section_defaults[section].keys()
        else:
            return True

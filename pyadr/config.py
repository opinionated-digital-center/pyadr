from configparser import ConfigParser
from copy import deepcopy
from typing import Dict

from pyadr.const import DEFAULT_CONFIG_FILE_PATH
from pyadr.exceptions import (
    PyadrConfigFileSettingsNotSupported,
    PyadrConfigSettingNotSupported,
)


class Config(ConfigParser):
    config_file_path = DEFAULT_CONFIG_FILE_PATH

    def __init__(self, defaults: Dict[str, str]):
        super().__init__(defaults=defaults)

        self.add_section("adr")

        if self.config_file_path.exists():
            self.read(self.config_file_path)

        self.check_settings_support_post_read()

    def set(self, section: str, setting: str, value: str) -> None:
        if section != self.default_section:  # type: ignore
            self.check_setting_supported(setting)
        super().set(section, setting, value)
        if section != self.default_section:  # type: ignore
            self.persist()

    def has_option(self, section: str, setting: str) -> bool:
        self.check_setting_supported(setting)
        return super().has_option(section, setting)

    def remove_option(self, section: str, setting: str) -> bool:
        self.check_setting_supported(setting)
        existed = super().remove_option(section, setting)
        if existed and section != self.default_section:  # type: ignore
            self.persist()
        return existed

    def persist(self) -> None:
        defaults = deepcopy(self.defaults())
        self[self.default_section] = {}  # type: ignore
        with self.config_file_path.open("w") as f:
            super().write(f)
        self[self.default_section] = defaults  # type: ignore

    def check_settings_support_post_read(self) -> None:
        unsupported_settings = [
            self.optionxform(setting)
            for setting in self["adr"].keys()
            if self.optionxform(setting) not in self.defaults()
        ]
        if unsupported_settings:
            raise PyadrConfigFileSettingsNotSupported(
                f"{unsupported_settings} not in {list(self.defaults().keys())}"
            )

    def check_setting_supported(self, setting: str) -> None:
        if self.optionxform(setting) not in self.defaults():
            raise PyadrConfigSettingNotSupported(
                f"'{self.optionxform(setting)}' not in {list(self.defaults().keys())}"
            )

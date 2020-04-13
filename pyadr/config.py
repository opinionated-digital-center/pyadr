from configparser import ConfigParser
from copy import deepcopy

from pyadr.const import DEFAULT_ADR_PATH, DEFAULT_CONFIG_FILE_PATH
from pyadr.exceptions import (
    PyadrConfigFileSettingsNotSupported,
    PyadrConfigSettingNotSupported,
)

CONFIG_SETTINGS = ["records-dir"]


class Config(ConfigParser):
    config_file_path = DEFAULT_CONFIG_FILE_PATH

    def __init__(self):
        defaults = {"records-dir": str(DEFAULT_ADR_PATH)}
        super().__init__(defaults=defaults)

        self.add_section("adr")

        if self.config_file_path.exists():
            self.read(self.config_file_path)

        unsupported_settings = [
            self.optionxform(setting)
            for setting in self["adr"].keys()
            if self.optionxform(setting) not in CONFIG_SETTINGS
        ]
        if unsupported_settings:
            raise PyadrConfigFileSettingsNotSupported(
                f"{unsupported_settings} not in {CONFIG_SETTINGS}"
            )

    def set(self, section, setting, value=None):
        if self.optionxform(setting) not in CONFIG_SETTINGS:
            raise PyadrConfigSettingNotSupported(
                f"'{self.optionxform(setting)}' not in {CONFIG_SETTINGS}"
            )
        super().set(section, setting, value)

    def write(self):
        defaults = deepcopy(self.defaults())
        self[self.default_section] = {}
        with self.config_file_path.open("w") as f:
            super().write(f)
        self[self.default_section] = defaults


config = Config()["adr"]

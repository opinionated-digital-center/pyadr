from configparser import ConfigParser
from copy import deepcopy

from pyadr.const import DEFAULT_ADR_PATH, DEFAULT_CONFIG_FILE_PATH
from pyadr.exceptions import (
    PyadrConfigFileItemsNotSupported,
    PyadrConfigItemNotSupported,
)

CONFIG_OPTIONS = ["records_dir"]


class Config(ConfigParser):
    config_file_path = DEFAULT_CONFIG_FILE_PATH

    def __init__(self):
        defaults = {"records_dir": str(DEFAULT_ADR_PATH)}
        super().__init__(defaults=defaults)

        self.add_section("adr")

        if self.config_file_path.exists():
            self.read(self.config_file_path)

        unsupported_options = [
            self.optionxform(o)
            for o in self["adr"].keys()
            if self.optionxform(o) not in CONFIG_OPTIONS
        ]
        if unsupported_options:
            raise PyadrConfigFileItemsNotSupported(
                f"{unsupported_options} not in {CONFIG_OPTIONS}"
            )

    def set(self, section, option, value=None):
        if self.optionxform(option) not in CONFIG_OPTIONS:
            raise PyadrConfigItemNotSupported(
                f"'{self.optionxform(option)}' not in {CONFIG_OPTIONS}"
            )
        super().set(section, option, value)

    def write(self):
        defaults = deepcopy(self.defaults())
        self[self.default_section] = {}
        with self.config_file_path.open("w") as f:
            super().write(f)
        self[self.default_section] = defaults


config = Config()["adr"]

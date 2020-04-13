from configparser import ConfigParser
from copy import deepcopy

from pyadr.const import DEFAULT_ADR_PATH, DEFAULT_CONFIG_FILE_PATH


class Config(ConfigParser):
    def __init__(self, config_file_path=DEFAULT_CONFIG_FILE_PATH):
        defaults = {"records_dir": str(DEFAULT_ADR_PATH)}
        super().__init__(defaults=defaults)

        self.config_file_path = config_file_path

        self.add_section("adr")

        if self.config_file_path.exists():
            self.read(self.config_file_path)

    def write(self):
        defaults = deepcopy(self.defaults())
        self[self.default_section] = {}
        with self.config_file_path.open("w") as f:
            super().write(f)
        self[self.default_section] = defaults


config = Config()["adr"]

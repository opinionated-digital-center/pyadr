from copy import deepcopy

from pyadr.config import AdrConfig
from pyadr.const import ADR_DEFAULT_SETTINGS, DEFAULT_CONFIG_FILE_PATH
from pyadr.git.const import GIT_ADR_DEFAULT_SETTINGS


class GitAdrConfig(AdrConfig):
    config_file_path = DEFAULT_CONFIG_FILE_PATH

    def __init__(self):
        defaults = {**ADR_DEFAULT_SETTINGS, **GIT_ADR_DEFAULT_SETTINGS}
        sorted_defaults = {}
        for key in sorted(defaults.keys()):
            sorted_defaults[key] = defaults[key]
        super().__init__(defaults=sorted_defaults)

        self.section_defaults = {
            "adr": ADR_DEFAULT_SETTINGS,
            "git": GIT_ADR_DEFAULT_SETTINGS,
        }

        self.add_section("adr")
        self.add_section("git")

        if self.config_file_path.exists():
            self.read(self.config_file_path)

        self.check_filled_settings_supported()

    def persist(self) -> None:
        defaults = deepcopy(self.defaults())
        self[self.default_section] = {}  # type: ignore

        with self.config_file_path.open("w") as f:
            self.write(f)

        self[self.default_section] = defaults  # type: ignore

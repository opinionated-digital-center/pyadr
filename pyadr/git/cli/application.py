import cleo

from pyadr import __version__
from pyadr.cli import LoggingAppConfig
from pyadr.git.cli.commands import GitInitCommand


class App(cleo.Application):
    def __init__(self, config=None):
        super().__init__(
            config=config or LoggingAppConfig("ADR Process Tool for Git", __version__)
        )

        self.add(GitInitCommand())

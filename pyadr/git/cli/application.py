import cleo

from pyadr import __version__
from pyadr.cli.config import LoggingAppConfig
from pyadr.git.cli.commands import (
    GitConfigCommand,
    GitInitCommand,
    GitNewCommand,
    GitPreMergeChecksCommand,
    GitProposeCommand,
)


class App(cleo.Application):
    def __init__(self, config=None):
        super().__init__(
            config=config or LoggingAppConfig("ADR Process Tool for Git", __version__)
        )

        self.add(GitConfigCommand())
        self.add(GitInitCommand())
        self.add(GitNewCommand())
        self.add(GitProposeCommand())
        self.add(GitPreMergeChecksCommand())

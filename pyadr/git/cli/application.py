import cleo

from pyadr import __version__
from pyadr.cli.config import LoggingAppConfig
from pyadr.git.cli.commands import (
    GitAcceptCommand,
    GitCommitCommand,
    GitConfigCommand,
    GitGenerateTocCommand,
    GitHelperCommand,
    GitInitCommand,
    GitNewCommand,
    GitPreMergeChecksCommand,
    GitProposeCommand,
    GitRejectCommand,
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
        self.add(GitAcceptCommand())
        self.add(GitRejectCommand())
        self.add(GitCommitCommand())
        self.add(GitHelperCommand())
        self.add(GitPreMergeChecksCommand())
        self.add(GitGenerateTocCommand())

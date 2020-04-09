import cleo

from pyadr import __version__
from pyadr.cli.commands import (
    AcceptCommand,
    GenerateTocCommand,
    InitCommand,
    NewCommand,
    RejectCommand,
)
from pyadr.cli.config import LoggingAppConfig


class App(cleo.Application):
    def __init__(self, config=None):
        super().__init__(
            config=config or LoggingAppConfig("ADR Process Tool", __version__)
        )

        self.add(InitCommand())
        self.add(NewCommand())
        self.add(AcceptCommand())
        self.add(RejectCommand())
        self.add(GenerateTocCommand())

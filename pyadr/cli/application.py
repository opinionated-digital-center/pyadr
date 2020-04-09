import cleo

from .. import __version__
from .commands import (
    AcceptCommand,
    GenerateTocCommand,
    InitCommand,
    NewCommand,
    RejectCommand,
)


class Application(cleo.Application):
    def __init__(self):
        super().__init__("ADR Process Tool", __version__)

        self.add(InitCommand())
        self.add(NewCommand())
        self.add(AcceptCommand())
        self.add(RejectCommand())
        self.add(GenerateTocCommand())

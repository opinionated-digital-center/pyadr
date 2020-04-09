import logging

import cleo
from cleo.config.application_config import ApplicationConfig
from loguru import logger

from .. import __version__
from .commands import (
    AcceptCommand,
    GenerateTocCommand,
    InitCommand,
    NewCommand,
    RejectCommand,
)
from .io import ClikitDebuggerHandler, ClikitHandler


class App(cleo.Application):
    def __init__(self, config=None):
        super().__init__(config=config or AppConfig())

        self.add(InitCommand())
        self.add(NewCommand())
        self.add(AcceptCommand())
        self.add(RejectCommand())
        self.add(GenerateTocCommand())


class AppConfig(ApplicationConfig):
    def __init__(self):
        super().__init__("ADR Process Tool", __version__)


class LoggingAppConfig(AppConfig):
    def create_io(self, *args, **kwargs):
        # remove loguru's default handler
        logger.remove(0)

        # add cli's own handler
        io = super().create_io(*args, **kwargs)
        logger.add(ClikitHandler(io), format="{message}", level=logging.INFO)
        logger.add(ClikitDebuggerHandler(io), colorize=True, level=logging.DEBUG)
        logger.info("Logger initialized.")
        logger.debug("debug message.")

        return io

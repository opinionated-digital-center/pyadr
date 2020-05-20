import logging

from clikit.api.io import flags as verbosity
from loguru import logger

LOGGING_VERBOSE = 18
LOGGING_VERY_VERBOSE = 16

logger.level("VERBOSE", LOGGING_VERBOSE, color="<bold>", icon="🔈️")
logger.level("VERY_VERBOSE", LOGGING_VERY_VERBOSE, color="<bold>", icon="🔊")

_levels = {
    logger.level("CRITICAL").no: verbosity.NORMAL,
    logger.level("ERROR").no: verbosity.NORMAL,
    logger.level("WARNING").no: verbosity.NORMAL,
    logger.level("SUCCESS").no: verbosity.NORMAL,
    logger.level("INFO").no: verbosity.NORMAL,
    logger.level("VERBOSE").no: verbosity.VERBOSE,
    logger.level("VERY_VERBOSE").no: verbosity.VERY_VERBOSE,
    logger.level("DEBUG").no: verbosity.DEBUG,
}


class ClikitHandler(logging.Handler):
    """Logging handler that redirects all messages to clikit io object."""

    def __init__(self, io, level=logging.NOTSET):
        super().__init__(level=level)
        self.io = io

    def emit(self, record: logging.LogRecord):
        level = _levels[record.levelno]
        if self.io.verbosity <= verbosity.VERY_VERBOSE:
            self.write_line(level, record)

    def write_line(self, level: int, record: logging.LogRecord):
        if record.levelno >= logging.WARNING:
            text = record.getMessage()
            self.io.error_line(text, flags=level)
        elif self.io.verbosity >= level:
            text = record.getMessage()
            self.io.write_line(text)


class ClikitDebuggerHandler(ClikitHandler):
    """Logging handler that redirects and format debug messages to clikit io object."""

    def emit(self, record: logging.LogRecord):
        level = _levels[record.levelno]
        if self.io.verbosity > verbosity.VERY_VERBOSE:
            self.write_line(level, record)

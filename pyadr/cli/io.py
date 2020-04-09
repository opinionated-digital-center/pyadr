import logging

from clikit.api.io import flags as verbosity

_levels = {
    logging.CRITICAL: verbosity.NORMAL,
    logging.ERROR: verbosity.NORMAL,
    logging.WARNING: verbosity.NORMAL,
    logging.INFO: verbosity.NORMAL,
    logging.DEBUG: verbosity.DEBUG,
}


class ClikitHandler(logging.Handler):
    """Logging handler that redirects all messages to clikit io object."""

    def __init__(self, io, level=logging.NOTSET):
        super().__init__(level=level)
        self.io = io

    def emit(self, record: logging.LogRecord):
        level = _levels[record.levelno]
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
        if self.io.verbosity >= verbosity.VERBOSE:
            self.write_line(level, record)

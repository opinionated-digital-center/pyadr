"""All package specific exceptions"""


class PyadrError(Exception):
    """Base exception for errors raised by pyadr"""


class PyadrNoPreviousAdrError(PyadrError):
    pass

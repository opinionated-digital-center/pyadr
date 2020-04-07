"""All package specific exceptions"""


class PyadrError(Exception):
    """Base exception for errors raised by pyadr"""


class PyadrNoNumberedAdrError(PyadrError):
    """No numbered ADR was found"""


class PyadrNoLineWithSuffixError(PyadrError):
    """No numbered ADR was found"""

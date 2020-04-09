"""All package specific exceptions"""


class PyadrError(Exception):
    """Base exception for errors raised by pyadr"""


class PyadrNoNumberedAdrError(PyadrError):
    """No numbered ADR was found"""


class PyadrNoLineWithSuffixError(PyadrError):
    """The searched line with suffix could not be found"""


class PyadrAdrDirectoryAlreadyExistsError(PyadrError):
    """ADR directory already exists"""


class PyadrAdrDirectoryDoesNotExistsError(PyadrError):
    """ADR directory does not exist"""


################################################
# Git related Errors
################################################


class PyadrGitError(PyadrError):
    """Base exception for errors raised by pyadr"""


class PyadrInvalidGitRepositoryError(PyadrGitError):
    """Could not find a valid repository"""


class PyadrGitIndexNotEmptyError(PyadrGitError):
    """Files are staged in the index"""


class PyadrGitBranchAlreadyExistsError(PyadrGitError):
    """Branch already exists"""

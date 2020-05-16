from pyadr.exceptions import PyadrError


class PyadrGitError(PyadrError):
    """Base exception for errors raised by pyadr"""


class PyadrInvalidGitRepositoryError(PyadrGitError):
    """Could not find a valid repository"""


class PyadrGitIndexNotEmptyError(PyadrGitError):
    """Files are staged in the index"""


class PyadrGitBranchAlreadyExistsError(PyadrGitError):
    """Branch already exists"""


class PyadrGitMainBranchDoesNotExistError(PyadrGitError):
    """Main branch (master or other specified) does not exist"""


class PyadrGitPreMergeChecksFailedError(PyadrGitError):
    """Pre-merge checks have failed"""


class PyadrGitAdrNotStagedOrCommittedError(PyadrGitError):
    """ADR file was expected to be staged or committed"""

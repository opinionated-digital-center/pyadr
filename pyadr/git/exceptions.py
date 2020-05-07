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


class PyadrSomeAdrFilenamesIncorrectError(PyadrGitError):
    """Check on the name of each ADR files has failed"""


class PyadrSomeAdrStatusesAreProposedError(PyadrGitError):
    """Check on the fact that no ADR status is 'proposed' has failed"""


class PyadrSomeAdrFileContentFormatIncorrectError(PyadrGitError):
    """Check on the format of ADR file content has failed"""


class PyadrSomeAdrNumbersNotUniqueError(PyadrGitError):
    """Some ADRs have the same number"""

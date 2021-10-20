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
    """Main branch (main or other specified) does not exist"""


class PyadrGitPreMergeChecksFailedError(PyadrGitError):
    """Pre-merge checks have failed"""


class PyadrGitAdrNotStagedOrCommittedError(PyadrGitError):
    """ADR file was expected to be staged or committed"""


class PyadrGitAdrNotStagedError(PyadrGitError):
    """ADR file was expected to be staged"""


class PyadrGitAdrBadFilenameFormatOrTitleError(PyadrGitError):
    """ADR filename formot incorrect or title portion different from title in file"""

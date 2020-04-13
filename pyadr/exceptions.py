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


class PyadrNoProposedAdrError(PyadrError):
    """Could not find a proposed ADR"""


class PyadrTooManyProposedAdrError(PyadrError):
    """Too many proposed ADR found"""


class PyadrConfigSettingNotSupported(PyadrError):
    """Config setting not supported"""


class PyadrConfigFileSettingsNotSupported(PyadrError):
    """Config settings in the config file not supported"""


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


class PyadrGitMainBranchDoesNotExistError(PyadrGitError):
    """Main branch (master or other specified) does not exist"""

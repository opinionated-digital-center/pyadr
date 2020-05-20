"""All package specific exceptions"""
from pyadr.const import VALID_ADR_CONTENT_FORMAT


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


class PyadrAdrFormatError(PyadrError):
    """ADR file format error"""

    def __init__(self, item_name: str, source: str):
        adr_format_message = (
            "{item} not found in ADR '{source}', "
            + "where as it should be of format:\n"
            + VALID_ADR_CONTENT_FORMAT
        )
        super(PyadrAdrFormatError, self).__init__(
            adr_format_message.format(item=item_name, source=source)
        )


class PyadrAdrTitleNotFoundError(PyadrAdrFormatError):
    """ADR title was not found in ADR file"""

    def __init__(self, source: str):
        super(PyadrAdrTitleNotFoundError, self).__init__(
            item_name="Title", source=source
        )


class PyadrAdrStatusNotFoundError(PyadrAdrFormatError):
    """ADR status was not found in ADR file"""

    def __init__(self, source: str):
        super(PyadrAdrStatusNotFoundError, self).__init__(
            item_name="Status", source=source
        )


class PyadrAdrDateNotFoundError(PyadrAdrFormatError):
    """ADR date was not found in ADR file"""

    def __init__(self, source: str):
        super(PyadrAdrDateNotFoundError, self).__init__(item_name="Date", source=source)


class PyadrSomeAdrFilenamesIncorrectError(PyadrError):
    """Check on the name of each ADR files has failed"""


class PyadrAdrFilenameIncorrectError(PyadrError):
    """ADR filename is badly formatted and/or not synched with the ADR content"""


class PyadrSomeAdrStatusesAreProposedError(PyadrError):
    """Check on the fact that no ADR status is 'proposed' has failed"""


class PyadrSomeAdrIdsNotUniqueError(PyadrError):
    """Some ADRs have the same number"""


class PyadrAdrRepoChecksFailedError(PyadrError):
    """ADR repository checks have failed"""


class PyadrAdrFilenameFormatError(PyadrError):
    """ADR filename format incorrect"""


class PyadrStatusIncompatibleWithReviewRequestError(PyadrError):
    """Cannot create a review request branch with status of the given ADR"""

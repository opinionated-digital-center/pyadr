"""Package constants"""
from pathlib import Path

###############################
# STATUSES
###############################

STATUS_ANY = "<any>"
STATUS_ANY_WITHOUT_ID = "<any status without any id yet>"
STATUS_ANY_WITH_ID = "<any status with an id>"

STATUS_PROPOSED = "proposed"
STATUS_ACCEPTED = "accepted"
STATUS_REJECTED = "rejected"
STATUS_DEPRECATED = "deprecated"
STATUS_SUPERSEDING = "superseding"
VALID_STATUSES = [
    STATUS_PROPOSED,
    STATUS_ACCEPTED,
    STATUS_REJECTED,
    STATUS_DEPRECATED,
    STATUS_SUPERSEDING,
]
STATUSES_WITH_ID = [
    STATUS_ANY_WITH_ID,
    STATUS_ACCEPTED,
    STATUS_REJECTED,
    STATUS_DEPRECATED,
    STATUS_SUPERSEDING,
]
STATUSES_WITHOUT_ID = [
    STATUS_ANY_WITHOUT_ID,
    STATUS_PROPOSED,
]

###############################
# REVIEW REQUESTS
###############################

REVIEW_REQUESTS = {
    STATUS_PROPOSED: "propose",
    STATUS_DEPRECATED: "deprecate",
    STATUS_SUPERSEDING: "supersede",
}
###############################
# CONFIG AND SETTINGS
###############################

DEFAULT_CONFIG_FILE_NAME = ".adr"
DEFAULT_CONFIG_FILE_PATH = Path(DEFAULT_CONFIG_FILE_NAME)
DEFAULT_ADR_PATH = Path("docs", "adr")

ADR_DEFAULT_SETTINGS = {"records-dir": str(DEFAULT_ADR_PATH)}

###############################
# CONTENT FORMAT
###############################

VALID_ADR_CONTENT_FORMAT = """>>>>>
# Title

* Status: a_status
[..]
* Date: YYYY-MM-DD
[..]
<<<<<
"""

###############################
# REGEX
###############################

ADR_ID_NOT_SET_REGEX = r"XXXX"
ADR_ID_REGEX = r"[0-9][0-9][0-9][0-9]"
ADR_TITLE_SLUG_REGEX = r"[a-z0-9-]*"

ADR_ID_NOT_SET_REGEX_WITH_SEPARATOR = ADR_ID_NOT_SET_REGEX + "-"
ADR_ID_REGEX_WITH_SEPARATOR = ADR_ID_REGEX + "-"

VALID_ADR_FILENAME_REGEX = (
    r"^("
    + ADR_ID_NOT_SET_REGEX
    + r"|"
    + ADR_ID_REGEX
    + r")-"
    + ADR_TITLE_SLUG_REGEX
    + r"\.md"
)
VALID_ADR_FILENAME_WITHOUT_ID_REGEX = (
    r"^" + ADR_ID_NOT_SET_REGEX + r"-" + ADR_TITLE_SLUG_REGEX + r"\.md"
)
VALID_ADR_FILENAME_WITH_ID_REGEX = (
    r"^" + ADR_ID_REGEX + r"-" + ADR_TITLE_SLUG_REGEX + r"\.md"
)

VALID_ADR_FILENAME_SKIP_TITLE_REGEX = (
    r"^(" + ADR_ID_NOT_SET_REGEX + r"|" + ADR_ID_REGEX + r")-.*\.md"
)
VALID_ADR_FILENAME_WITHOUT_ID_SKIP_TITLE_REGEX = (
    r"^" + ADR_ID_NOT_SET_REGEX + r"-.*\.md"
)
VALID_ADR_FILENAME_WITH_ID_SKIP_TITLE_REGEX = r"^" + ADR_ID_REGEX + r"-.*\.md"

FILENAME_REGEXES = {
    STATUS_ANY: {
        "full": VALID_ADR_FILENAME_REGEX,
        "skip_title": VALID_ADR_FILENAME_SKIP_TITLE_REGEX,
    },
    STATUS_ANY_WITHOUT_ID: {
        "full": VALID_ADR_FILENAME_WITHOUT_ID_REGEX,
        "skip_title": VALID_ADR_FILENAME_WITHOUT_ID_SKIP_TITLE_REGEX,
    },
    STATUS_ANY_WITH_ID: {
        "full": VALID_ADR_FILENAME_WITH_ID_REGEX,
        "skip_title": VALID_ADR_FILENAME_WITH_ID_SKIP_TITLE_REGEX,
    },
    STATUS_PROPOSED: {
        "full": VALID_ADR_FILENAME_WITHOUT_ID_REGEX,
        "skip_title": VALID_ADR_FILENAME_WITHOUT_ID_SKIP_TITLE_REGEX,
    },
    STATUS_ACCEPTED: {
        "full": VALID_ADR_FILENAME_WITH_ID_REGEX,
        "skip_title": VALID_ADR_FILENAME_WITH_ID_SKIP_TITLE_REGEX,
    },
    STATUS_REJECTED: {
        "full": VALID_ADR_FILENAME_WITH_ID_REGEX,
        "skip_title": VALID_ADR_FILENAME_WITH_ID_SKIP_TITLE_REGEX,
    },
    STATUS_DEPRECATED: {
        "full": VALID_ADR_FILENAME_WITH_ID_REGEX,
        "skip_title": VALID_ADR_FILENAME_WITH_ID_SKIP_TITLE_REGEX,
    },
    STATUS_SUPERSEDING: {
        "full": VALID_ADR_FILENAME_WITH_ID_REGEX,
        "skip_title": VALID_ADR_FILENAME_WITH_ID_SKIP_TITLE_REGEX,
    },
}

###############################
# REGEX ERROR MESSAGES
###############################

REGEX_ERROR_MESSAGE_PREFIX = (
    "(status to verify against: '{status}')\nADR(s)'s filename follow the format '"
)

REGEX_ERROR_MESSAGE_ADR_FILENAME = "".join(
    [
        REGEX_ERROR_MESSAGE_PREFIX,
        ADR_ID_NOT_SET_REGEX,
        "-<adr-title-in-slug-format>.md' or '",
        ADR_ID_REGEX,
        "-<adr-title-in-slug-format>.md'",
    ]
)
REGEX_ERROR_MESSAGE_ADR_FILENAME_WITHOUT_ID = "".join(
    [
        REGEX_ERROR_MESSAGE_PREFIX,
        ADR_ID_NOT_SET_REGEX,
        "-<adr-title-in-slug-format>.md'",
    ]
)
REGEX_ERROR_MESSAGE_ADR_FILENAME_WITH_ID = "".join(
    [REGEX_ERROR_MESSAGE_PREFIX, ADR_ID_REGEX, "-<adr-title-in-slug-format>.md'"]
)

REGEX_ERROR_MESSAGE_ADR_FILENAME_SKIP_TITLE = "".join(
    [
        REGEX_ERROR_MESSAGE_PREFIX,
        ADR_ID_NOT_SET_REGEX,
        "-*.md' or '",
        ADR_ID_REGEX,
        "-*.md'",
    ]
)
REGEX_ERROR_MESSAGE_ADR_FILENAME_WITHOUT_ID_SKIP_TITLE = "".join(
    [REGEX_ERROR_MESSAGE_PREFIX, ADR_ID_NOT_SET_REGEX, "-*.md'"]
)
REGEX_ERROR_MESSAGE_ADR_FILENAME_WITH_ID_SKIP_TITLE = "".join(
    [REGEX_ERROR_MESSAGE_PREFIX, ADR_ID_REGEX, "-*.md'"]
)

REGEX_ERROR_MESSAGES = {
    STATUS_ANY: {
        "full": REGEX_ERROR_MESSAGE_ADR_FILENAME.format(status=STATUS_ANY),
        "skip_title": REGEX_ERROR_MESSAGE_ADR_FILENAME_SKIP_TITLE.format(
            status=STATUS_ANY
        ),
        "id_prefix": "' or '".join(
            [ADR_ID_REGEX_WITH_SEPARATOR, ADR_ID_NOT_SET_REGEX_WITH_SEPARATOR]
        ),
    },
    STATUS_ANY_WITHOUT_ID: {
        "full": REGEX_ERROR_MESSAGE_ADR_FILENAME_WITHOUT_ID.format(
            status=STATUS_ANY_WITHOUT_ID
        ),
        "skip_title": REGEX_ERROR_MESSAGE_ADR_FILENAME_WITHOUT_ID_SKIP_TITLE.format(
            status=STATUS_ANY_WITHOUT_ID
        ),
        "id_prefix": ADR_ID_NOT_SET_REGEX_WITH_SEPARATOR,
    },
    STATUS_ANY_WITH_ID: {
        "full": REGEX_ERROR_MESSAGE_ADR_FILENAME_WITH_ID.format(
            status=STATUS_ANY_WITH_ID
        ),
        "skip_title": REGEX_ERROR_MESSAGE_ADR_FILENAME_WITH_ID_SKIP_TITLE.format(
            status=STATUS_ANY_WITH_ID
        ),
        "id_prefix": ADR_ID_REGEX_WITH_SEPARATOR,
    },
    STATUS_PROPOSED: {
        "full": REGEX_ERROR_MESSAGE_ADR_FILENAME_WITHOUT_ID.format(
            status=STATUS_PROPOSED
        ),
        "skip_title": REGEX_ERROR_MESSAGE_ADR_FILENAME_WITHOUT_ID_SKIP_TITLE.format(
            status=STATUS_PROPOSED
        ),
        "id_prefix": ADR_ID_NOT_SET_REGEX_WITH_SEPARATOR,
    },
    STATUS_ACCEPTED: {
        "full": REGEX_ERROR_MESSAGE_ADR_FILENAME_WITH_ID.format(status=STATUS_ACCEPTED),
        "skip_title": REGEX_ERROR_MESSAGE_ADR_FILENAME_WITH_ID_SKIP_TITLE.format(
            status=STATUS_ACCEPTED
        ),
        "id_prefix": ADR_ID_REGEX,
    },
    STATUS_REJECTED: {
        "full": REGEX_ERROR_MESSAGE_ADR_FILENAME_WITH_ID.format(status=STATUS_REJECTED),
        "skip_title": REGEX_ERROR_MESSAGE_ADR_FILENAME_WITH_ID_SKIP_TITLE.format(
            status=STATUS_REJECTED
        ),
        "id_prefix": ADR_ID_REGEX_WITH_SEPARATOR,
    },
    STATUS_DEPRECATED: {
        "full": REGEX_ERROR_MESSAGE_ADR_FILENAME_WITH_ID.format(
            status=STATUS_DEPRECATED
        ),
        "skip_title": REGEX_ERROR_MESSAGE_ADR_FILENAME_WITH_ID_SKIP_TITLE.format(
            status=STATUS_DEPRECATED
        ),
        "id_prefix": ADR_ID_REGEX_WITH_SEPARATOR,
    },
    STATUS_SUPERSEDING: {
        "full": REGEX_ERROR_MESSAGE_ADR_FILENAME_WITH_ID.format(
            status=STATUS_SUPERSEDING
        ),
        "skip_title": REGEX_ERROR_MESSAGE_ADR_FILENAME_WITH_ID_SKIP_TITLE.format(
            status=STATUS_SUPERSEDING
        ),
        "id_prefix": ADR_ID_NOT_SET_REGEX_WITH_SEPARATOR,
    },
}

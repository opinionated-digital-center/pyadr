"""Package constants"""
from pathlib import Path

STATUS_PROPOSED = "proposed"
STATUS_ACCEPTED = "accepted"
STATUS_REJECTED = "rejected"

DEFAULT_ADR_PATH = Path("docs", "adr")

DEFAULT_CONFIG_FILE_NAME = ".adr"
DEFAULT_CONFIG_FILE_PATH = Path(DEFAULT_CONFIG_FILE_NAME)
ADR_DEFAULT_SETTINGS = {"records-dir": str(DEFAULT_ADR_PATH)}

VALID_ADR_CONTENT_FORMAT = """>>>>>
# Title

* Status: a_status
[..]
* Date: YYYY-MM-DD
[..]
<<<<<
"""
VALID_ADR_FILENAME_REGEX = r"^[0-9][0-9][0-9][0-9]-[a-z0-9-]*\.md"

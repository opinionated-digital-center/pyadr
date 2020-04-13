"""Package constants"""
from pathlib import Path

STATUS_PROPOSED = "proposed"
STATUS_ACCEPTED = "accepted"
STATUS_REJECTED = "rejected"

DEFAULT_ADR_PATH = Path("docs", "adr")

DEFAULT_CONFIG_FILE_NAME = ".adr"
DEFAULT_CONFIG_FILE_PATH = Path(DEFAULT_CONFIG_FILE_NAME)
ADR_DEFAULT_SETTINGS = {"records-dir": str(DEFAULT_ADR_PATH)}

"""Package constants"""
import os
from pathlib import Path

STATUS_PROPOSED = "proposed"
STATUS_ACCEPTED = "accepted"
STATUS_REJECTED = "rejected"

CWD = Path(os.getcwd())
DEFAULT_ADR_PATH = Path("docs", "adr")
DEFAULT_CONFIG_FILE_PATH = Path(".adr")

"""Package constants"""
import os
from pathlib import Path

STATUS_PROPOSED = "proposed"
STATUS_ACCEPTED = "accepted"
STATUS_REJECTED = "rejected"

CWD = os.getcwd()
ADR_REPO_REL_PATH = Path("docs", "adr")
ADR_REPO_ABS_PATH = Path(CWD) / ADR_REPO_REL_PATH

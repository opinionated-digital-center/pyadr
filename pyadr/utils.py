from pathlib import Path

from loguru import logger

from pyadr.config import config
from pyadr.exceptions import PyadrAdrDirectoryDoesNotExistsError


def verify_adr_dir_exists():
    adr_repo_path = Path(config["records-dir"])
    if not adr_repo_path.exists():
        logger.error(
            f"Directory '{adr_repo_path}/' does not exist. "
            "Initialise your ADR repo first."
        )
        raise PyadrAdrDirectoryDoesNotExistsError()

from loguru import logger

from pyadr.const import ADR_REPO_ABS_PATH, ADR_REPO_REL_PATH
from pyadr.exceptions import PyadrAdrDirectoryDoesNotExistsError


def verify_adr_dir_exists():
    if not ADR_REPO_ABS_PATH.exists():
        logger.error(
            f"Directory '{ADR_REPO_REL_PATH}/' does not exist. "
            "Initialise your ADR repo first."
        )
        raise PyadrAdrDirectoryDoesNotExistsError()

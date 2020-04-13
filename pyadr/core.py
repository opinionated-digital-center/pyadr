import shutil
from pathlib import Path
from typing import Dict, List

from loguru import logger
from slugify import slugify

from pyadr import assets
from pyadr.config import Config
from pyadr.const import ADR_DEFAULT_SETTINGS, STATUS_ACCEPTED, STATUS_PROPOSED
from pyadr.content_utils import (
    build_toc_content_from_adrs_by_status,
    extract_adrs_by_status,
)
from pyadr.exceptions import (
    PyadrAdrDirectoryAlreadyExistsError,
    PyadrAdrDirectoryDoesNotExistsError,
    PyadrNoNumberedAdrError,
    PyadrNoProposedAdrError,
    PyadrTooManyProposedAdrError,
)
from pyadr.file_utils import rename_reviewed_adr_file, update_adr_title_status

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources  # type: ignore


class AdrCore(object):
    def __init__(self, default_settings: Dict[str, str] = ADR_DEFAULT_SETTINGS):
        sorted_default_settings = {}
        for key in sorted(default_settings.keys()):
            sorted_default_settings[key] = default_settings[key]

        self.config = Config(sorted_default_settings)["adr"]

    ###########################################
    # CONFIGURE ADR
    ###########################################
    def configure(self, setting: str, value: str) -> None:
        self.config[setting] = value
        logger.info(f"Configured '{setting}' to '{value}'.")

    def unset_config_setting(self, setting: str) -> None:
        del self.config[setting]
        logger.info(f"Config setting '{setting}' unset.")

    def list_config(self) -> None:
        for key in self.config.keys():
            self.print_config_setting(key)

    def print_config_setting(self, setting: str) -> None:
        logger.info(f"{setting} = {self.config[setting]}")

    ###########################################
    # INIT ADR
    ###########################################
    def init_adr_repo(self, force: bool = False) -> List[Path]:
        self.verify_and_prepare_pre_init(force)
        self.create_adr_repo_dir()
        created_files = [
            self._init_adr_template(),
            self._init_adr_0000(),
            self._init_adr_0001(),
        ]
        logger.info(
            f"ADR repository successfully created at "
            f"'{Path(self.config['records-dir']).resolve()}/'."
        )
        return created_files

    def verify_and_prepare_pre_init(self, force: bool = False) -> None:
        adr_repo_abs_path = Path(self.config["records-dir"]).resolve()
        if force:
            if adr_repo_abs_path.exists():
                logger.warning(
                    f"Directory '{adr_repo_abs_path}/' already exists. "
                    f"Used '--force' option => Erasing..."
                )
                shutil.rmtree(adr_repo_abs_path)
                logger.warning("... erased.")

        else:
            if adr_repo_abs_path.exists():
                logger.error(
                    f"Directory '{adr_repo_abs_path}/' already exists. "
                    "You can use '--force' option to erase."
                )
                raise PyadrAdrDirectoryAlreadyExistsError()

    def create_adr_repo_dir(self):
        adr_repo_path = Path(self.config["records-dir"])
        logger.info(f"Creating ADR repo directory '{adr_repo_path}'.")
        adr_repo_path.mkdir(parents=True)
        logger.info(f"... done.")

    def _init_adr_template(self) -> Path:
        template_path = Path(self.config["records-dir"], "template.md")

        logger.info(f"Copying MADR template to '{template_path}'...")
        with template_path.open("w") as f:
            f.write(pkg_resources.read_text(assets, "madr-template.md"))  # type: ignore

        logger.info(f"... done.")
        return template_path

    def _init_adr_0000(self) -> Path:
        return self._init_adr_file("0000-record-architecture-decisions.md")

    def _init_adr_0001(self) -> Path:
        return self._init_adr_file(
            "0001-use-markdown-architectural-decision-records.md"
        )

    def _init_adr_file(self, filename: str) -> Path:
        path = Path(self.config["records-dir"], filename)

        logger.info(f"Creating ADR '{path}'...")
        with path.open("w") as f:
            f.write(pkg_resources.read_text(assets, filename))  # type: ignore
        update_adr_title_status(path, status=STATUS_ACCEPTED)

        logger.info(f"... done.")
        return path

    ###########################################
    # NEW ADR
    ###########################################
    def new_adr(self, title: str, pre_checks: bool = True) -> Path:
        if pre_checks:
            self.verify_adr_dir_exists()

        adr_path = Path(self.config["records-dir"], f"XXXX-{slugify(title)}.md")

        with adr_path.open("w") as f:
            f.write(pkg_resources.read_text(assets, "madr-template.md"))  # type: ignore
        update_adr_title_status(adr_path, title=title, status=STATUS_PROPOSED)

        logger.warning(f"Created ADR '{adr_path}'.")
        return adr_path

    ###########################################
    # GENERATE TOC
    ###########################################
    def generate_toc(self, pre_checks: bool = True) -> None:
        if pre_checks:
            self.verify_adr_dir_exists()

        adr_paths = sorted(
            Path(self.config["records-dir"]).glob("[0-9][0-9][0-9][0-9]-*")
        )

        adrs_by_status = extract_adrs_by_status(
            Path(self.config["records-dir"]), adr_paths
        )

        toc_content = build_toc_content_from_adrs_by_status(adrs_by_status)

        toc_path = Path(self.config["records-dir"], "index.md")
        with toc_path.open("w") as f:
            f.writelines(toc_content)

        logger.info(f"Markdown table of content generated in '{toc_path}'")

    ###########################################
    # ACCEPT / REJECT
    ###########################################
    def accept_or_reject(self, status: str, toc: bool = False) -> None:
        found_proposed_adrs = sorted(Path(self.config["records-dir"]).glob("XXXX-*"))
        logger.info(
            f"Current Working Directory is: '{Path(self.config['records-dir'])}'"
        )
        if not len(found_proposed_adrs):
            logger.error(
                "Could not find a proposed ADR "
                "(should be of format 'docs/adr/XXXX-adr-title.md')."
            )
            raise PyadrNoProposedAdrError()

        elif len(found_proposed_adrs) > 1:
            logger.error(
                f"Can handle only 1 proposed ADR but found {len(found_proposed_adrs)}:"
            )
            for adr in found_proposed_adrs:
                logger.error(f"    => '{adr}'")
            raise PyadrTooManyProposedAdrError()

        proposed_adr = found_proposed_adrs[0]
        try:
            reviewed_adr = rename_reviewed_adr_file(
                proposed_adr, Path(self.config["records-dir"])
            )
        except PyadrNoNumberedAdrError as e:
            logger.error(
                "There should be at least one initial reviewed ADR "
                "(usually 'docs/adr/0000-record-architecture-decisions.md')."
            )
            raise PyadrNoNumberedAdrError(e)

        logger.info(f"Renamed ADR to: {reviewed_adr}")

        if toc:
            self.generate_toc()

        update_adr_title_status(reviewed_adr, status=status)
        logger.info(f"Changed ADR status to: {status}")

        ###########################################
        # SHARED FUNC
        ###########################################

    def verify_adr_dir_exists(self):
        adr_repo_path = Path(self.config["records-dir"])
        if not adr_repo_path.exists():
            logger.error(
                f"Directory '{adr_repo_path}/' does not exist. "
                "Initialise your ADR repo first."
            )
            raise PyadrAdrDirectoryDoesNotExistsError()

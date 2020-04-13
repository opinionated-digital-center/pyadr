import shutil
from pathlib import Path
from typing import List

from loguru import logger
from slugify import slugify

from pyadr import assets
from pyadr.config import config
from pyadr.const import STATUS_ACCEPTED, STATUS_PROPOSED
from pyadr.content_utils import retrieve_title_status_and_date_from_madr_content_stream
from pyadr.exceptions import (
    PyadrAdrDirectoryAlreadyExistsError,
    PyadrNoNumberedAdrError,
    PyadrNoProposedAdrError,
    PyadrTooManyProposedAdrError,
)
from pyadr.file_utils import rename_reviewed_adr_file, update_adr_title_status
from pyadr.utils import verify_adr_dir_exists

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources  # type: ignore


###########################################
# CONFIGURE ADR
###########################################
def configure(item: str, value: str) -> None:
    config[item] = value
    logger.info(f"Configured '{item}' to '{value}'.")


def unset_config_item(item: str) -> None:
    del config[item]
    logger.info(f"Config item '{item}' unset.")


def list_config():
    for key in config.keys():
        print_config_item(key)


def print_config_item(key: str):
    logger.info(f"{key} = {config[key]}")


###########################################
# INIT ADR
###########################################
def init_adr_repo(force: bool = False) -> List[Path]:
    verify_and_prepare_pre_init(force)
    create_adr_repo_dir()
    created_files = [
        _init_adr_template(),
        _init_adr_0000(),
        _init_adr_0001(),
    ]
    logger.info(
        f"ADR repository successfully created at "
        f"'{Path(config['records-dir']).resolve()}/'."
    )
    return created_files


def verify_and_prepare_pre_init(force: bool = False) -> None:
    adr_repo_abs_path = Path(config["records-dir"]).resolve()
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


def create_adr_repo_dir():
    adr_repo_path = Path(config["records-dir"])
    logger.info(f"Creating ADR repo directory '{adr_repo_path}'.")
    adr_repo_path.mkdir(parents=True)
    logger.info(f"... done.")


def _init_adr_template() -> Path:
    template_path = Path(config["records-dir"], "template.md")

    logger.info(f"Copying MADR template to '{template_path}'...")
    with template_path.open("w") as f:
        f.write(pkg_resources.read_text(assets, "madr-template.md"))  # type: ignore

    logger.info(f"... done.")
    return template_path


def _init_adr_0000() -> Path:
    return _init_adr_file("0000-record-architecture-decisions.md")


def _init_adr_0001() -> Path:
    return _init_adr_file("0001-use-markdown-architectural-decision-records.md")


def _init_adr_file(filename: str) -> Path:
    path = Path(config["records-dir"], filename)

    logger.info(f"Creating ADR '{path}'...")
    with path.open("w") as f:
        f.write(pkg_resources.read_text(assets, filename))  # type: ignore
    update_adr_title_status(path, status=STATUS_ACCEPTED)

    logger.info(f"... done.")
    return path


###########################################
# NEW ADR
###########################################
def new_adr(title: str, pre_checks: bool = True) -> Path:
    if pre_checks:
        verify_adr_dir_exists()

    adr_path = Path(config["records-dir"], f"XXXX-{slugify(title)}.md")

    with adr_path.open("w") as f:
        f.write(pkg_resources.read_text(assets, "madr-template.md"))  # type: ignore
    update_adr_title_status(adr_path, title=title, status=STATUS_PROPOSED)

    logger.warning(f"Created ADR '{adr_path}'.")
    return adr_path


###########################################
# ACCEPT / REJECT
###########################################
def accept_or_reject(status: str, toc: bool = False) -> None:
    found_proposed_adrs = sorted(Path(config["records-dir"]).glob("XXXX-*"))
    logger.info(f"Current Working Directory is: '{Path(config['records-dir'])}'")
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
            proposed_adr, Path(config["records-dir"])
        )
    except PyadrNoNumberedAdrError as e:
        logger.error(
            "There should be at least one initial reviewed ADR "
            "(usually 'docs/adr/0000-record-architecture-decisions.md')."
        )
        raise PyadrNoNumberedAdrError(e)

    logger.info(f"Renamed ADR to: {reviewed_adr}")

    if toc:
        generate_toc()

    update_adr_title_status(reviewed_adr, status=status)
    logger.info(f"Changed ADR status to: {status}")


###########################################
# GENERATE TOC
###########################################
def generate_toc(pre_checks: bool = True) -> None:
    if pre_checks:
        verify_adr_dir_exists()

    adr_paths = sorted(Path(config["records-dir"]).glob("[0-9][0-9][0-9][0-9]-*"))

    adrs_by_status = _extract_adrs_by_status(adr_paths)

    toc_content = _build_toc_content_from_adrs_by_status(adrs_by_status)

    toc_path = Path(config["records-dir"], "index.md")
    with toc_path.open("w") as f:
        f.writelines(toc_content)

    logger.info(f"Markdown table of content generated in '{toc_path}'")


def _build_toc_content_from_adrs_by_status(adrs_by_status):
    toc_content = [
        "<!-- This file has been generated by `pyadr`. Manual changes will be "
        "erased at next generation. -->\n",
        "# Architecture Decision Records\n",
    ]
    for status in ["accepted", "rejected", "superseded", "deprecated", "non-standard"]:
        if status != "non-standard":
            toc_content.append("\n")
            toc_content.append(f"## {adrs_by_status[status]['status-title']}\n")
            toc_content.append("\n")
            if adrs_by_status[status]["adrs"]:
                toc_content.extend(adrs_by_status[status]["adrs"])
            else:
                toc_content.append("* None\n")
        else:
            toc_content.append("\n")
            toc_content.append(f"## {adrs_by_status[status]['status-title']}\n")
            if adrs_by_status[status]["adrs-by-status"]:
                for value in adrs_by_status[status]["adrs-by-status"].values():
                    toc_content.append("\n")
                    toc_content.append(f"### {value['status-title']}\n")
                    toc_content.append("\n")
                    toc_content.extend(value["adrs"])
            else:
                toc_content.append("\n")
                toc_content.append("* None\n")
    return toc_content


def _extract_adrs_by_status(adr_paths):
    adrs_by_status = {
        "accepted": {"status-title": "Accepted Records", "adrs": []},
        "rejected": {"status-title": "Rejected Records", "adrs": []},
        "superseded": {"status-title": "Superseded Records", "adrs": []},
        "deprecated": {"status-title": "Deprecated Records", "adrs": []},
        "non-standard": {
            "status-title": "Records with non-standard statuses",
            "adrs-by-status": {},
        },
    }
    for adr in adr_paths:
        with adr.open() as f:
            (
                title,
                (status, status_phrase),
                date,
            ) = retrieve_title_status_and_date_from_madr_content_stream(f)
        try:
            status_supplement = ""
            if status_phrase:
                status_supplement = f": {status} {status_phrase}"
            adrs_by_status[status]["adrs"].append(
                f"* [{title}]({Path(config['records-dir']) / adr.name})"
                f"{status_supplement}\n"
            )
        except KeyError:
            if status not in adrs_by_status["non-standard"]["adrs-by-status"].keys():
                adrs_by_status["non-standard"]["adrs-by-status"][status] = {
                    "status-title": f"Status `{status}`",
                    "adrs": [],
                }
            adrs_by_status["non-standard"]["adrs-by-status"][status]["adrs"].append(
                f"* [{title}]({Path(config['records-dir']) / adr.name})"
                f"{status_supplement}\n"
            )
    return adrs_by_status

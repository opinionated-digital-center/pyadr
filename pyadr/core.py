import re
import shutil
from pathlib import Path
from typing import List, Optional, Tuple

from loguru import logger
from slugify import slugify

from pyadr import assets
from pyadr.config import AdrConfig
from pyadr.const import (
    FILENAME_REGEXES,
    REGEX_ERROR_MESSAGES,
    STATUS_ACCEPTED,
    STATUS_ANY_WITH_ID,
    STATUS_PROPOSED,
    VALID_ADR_CONTENT_FORMAT,
    VALID_ADR_FILENAME_WITH_ID_REGEX,
)
from pyadr.content_utils import (
    adr_status_from_file,
    adr_title_lowercase_from_file,
    adr_title_slug_from_file,
    adr_title_status_and_date_from_file,
    build_toc_content_from_adrs_by_status,
    extract_adrs_by_status,
)
from pyadr.exceptions import (
    PyadrAdrDirectoryAlreadyExistsError,
    PyadrAdrDirectoryDoesNotExistsError,
    PyadrAdrFilenameFormatError,
    PyadrAdrFilenameIncorrectError,
    PyadrAdrFormatError,
    PyadrAdrRepoChecksFailedError,
    PyadrNoNumberedAdrError,
    PyadrNoProposedAdrError,
    PyadrSomeAdrFilenamesIncorrectError,
    PyadrSomeAdrIdsNotUniqueError,
    PyadrSomeAdrStatusesAreProposedError,
    PyadrTooManyProposedAdrError,
)
from pyadr.file_utils import calculate_next_adr_id, update_adr

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources  # type: ignore


class AdrCore(object):
    def __init__(self):
        self.config = AdrConfig()

    ###########################################
    # CONFIGURE ADR
    ###########################################
    def configure(self, setting: str, value: str) -> None:
        self.config["adr"][setting] = value
        logger.info(f"Configured '{setting}' to '{value}'.")

    def unset_config_setting(self, setting: str) -> None:
        del self.config["adr"][setting]
        logger.info(f"AdrConfig setting '{setting}' unset.")

    def list_config(self) -> None:
        raw_config = self.config.raw()
        for setting in raw_config.keys():
            logger.info(f"{setting} = {raw_config[setting]}")

    def print_config_setting(self, setting: str) -> None:
        raw_config = self.config.raw()
        logger.info(f"{setting} = {raw_config[setting]}")

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
            f"'{Path(self.config['adr']['records-dir']).resolve()}/'."
        )
        return created_files

    def verify_and_prepare_pre_init(self, force: bool = False) -> None:
        adr_repo_abs_path = Path(self.config["adr"]["records-dir"]).resolve()
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
        adr_repo_path = Path(self.config["adr"]["records-dir"])
        logger.info(f"Creating ADR repo directory '{adr_repo_path}'.")
        adr_repo_path.mkdir(parents=True)
        logger.log("VERBOSE", "... done.")

    def _init_adr_template(self) -> Path:
        template_path = Path(self.config["adr"]["records-dir"], "template.md")

        logger.info(f"Copying MADR template to '{template_path}'...")
        with template_path.open("w") as f:
            f.write(pkg_resources.read_text(assets, "madr-template.md"))  # type: ignore

        logger.log("VERBOSE", "... done.")
        return template_path

    def _init_adr_0000(self) -> Path:
        return self._init_adr_file("0000-record-architecture-decisions.md")

    def _init_adr_0001(self) -> Path:
        return self._init_adr_file(
            "0001-use-markdown-architectural-decision-records.md"
        )

    def _init_adr_file(self, filename: str) -> Path:
        path = Path(self.config["adr"]["records-dir"], filename)

        logger.info(f"Creating ADR '{path}'...")
        with path.open("w") as f:
            f.write(pkg_resources.read_text(assets, filename))  # type: ignore
        update_adr(path, status=STATUS_ACCEPTED)

        logger.log("VERBOSE", "... done.")
        return path

    ###########################################
    # NEW ADR
    ###########################################
    def new_adr(self, title: str, pre_checks: bool = True) -> Path:
        if pre_checks:
            self.verify_adr_dir_exists()

        adr_path = Path(self.config["adr"]["records-dir"], f"XXXX-{slugify(title)}.md")

        logger.info(f"Creating ADR '{adr_path}'...")
        with adr_path.open("w") as f:
            f.write(pkg_resources.read_text(assets, "madr-template.md"))  # type: ignore
        update_adr(adr_path, title=title, status=STATUS_PROPOSED)
        logger.log("VERBOSE", "... done.")

        return adr_path

    ###########################################
    # ACCEPT / REJECT
    ###########################################
    def accept_or_reject(self, file: str, status: str, toc: bool = False) -> Path:
        processed_adr = self._apply_accept_or_reject_to_proposed_adr(Path(file), status)

        if toc:
            self.generate_toc()

        return processed_adr

    def _adr_filename_format_correct(
        self, path: Path, status: str = None, check_title_format: bool = True
    ) -> bool:
        status = self._resolve_status(path, status)
        full_or_skip_title = self._resolve_regex_type(check_title_format)

        return bool(
            re.compile(FILENAME_REGEXES[status][full_or_skip_title]).match(path.name)
        )

    def _resolve_status(self, path: Path, status: str = None) -> str:
        if status is None:
            status = adr_status_from_file(path)
        return status

    def _resolve_regex_type(self, check_title_format: bool = True) -> str:
        if check_title_format:
            return "full"
        else:
            return "skip_title"

    def _verify_adr_filename_format(
        self, path: Path, status: str = None, check_title_format: bool = True
    ) -> None:
        if not self._adr_filename_format_correct(path, status, check_title_format):
            status = self._resolve_status(path, status)
            full_or_skip_title = self._resolve_regex_type(check_title_format)

            logger.error(REGEX_ERROR_MESSAGES[status][full_or_skip_title] + ".")
            raise PyadrAdrFilenameFormatError(str(path))

    def _verify_one_and_only_one_proposed_adr_found(
        self, found_proposed_adrs: List[Path]
    ) -> None:
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

    def _get_next_adr_id(self) -> str:
        try:
            next_adr_id = calculate_next_adr_id(Path(self.config["adr"]["records-dir"]))
        except PyadrNoNumberedAdrError as e:
            logger.error(
                "There should be at least one initial accepted/rejected ADR "
                "(usually 'docs/adr/0000-record-architecture-decisions.md')."
            )
            raise PyadrNoNumberedAdrError(e)
        else:
            return next_adr_id

    def _apply_accept_or_reject_to_proposed_adr(
        self, proposed_adr: Path, status: str
    ) -> Path:
        next_adr_id = self._get_next_adr_id()
        processed_adr = self._sync_adr_filename(proposed_adr, next_adr_id)
        logger.info(f"Renamed ADR to: {processed_adr}")

        update_adr(processed_adr, status=status)
        logger.info(f"Changed ADR status to: {status}")

        return processed_adr

    def _sync_adr_filename(self, adr_path: Path, adr_id: str) -> Path:
        renamed_path = self._build_adr_filename(adr_path, adr_id)
        if adr_path != renamed_path:
            self._apply_filepath_update(adr_path, renamed_path)

        return renamed_path

    def _build_adr_filename(self, adr_path: Path, adr_id: str) -> Path:
        title_slug = adr_title_slug_from_file(adr_path)
        renamed_path = adr_path.with_name(
            "-".join([adr_id, title_slug]) + adr_path.suffix
        )
        return renamed_path

    def _apply_filepath_update(self, path: Path, renamed_path: Path) -> None:
        path.rename(renamed_path)

    ###########################################
    # GENERATE TOC
    ###########################################
    def generate_toc(self, pre_checks: bool = True) -> Path:
        if pre_checks:
            self.verify_adr_dir_exists()

        adr_paths = sorted(
            Path(self.config["adr"]["records-dir"]).glob("[0-9][0-9][0-9][0-9]-*")
        )

        adrs_by_status = extract_adrs_by_status(
            Path(self.config["adr"]["records-dir"]), adr_paths
        )

        toc_content = build_toc_content_from_adrs_by_status(adrs_by_status)

        toc_path = Path(self.config["adr"]["records-dir"], "index.md")
        with toc_path.open("w") as f:
            f.writelines(toc_content)

        logger.info(f"Markdown table of content generated in '{toc_path}'")

        return toc_path

    ###########################################
    # HELPER FUNCTIONS
    ###########################################
    def print_title_slug(self, file: str) -> None:
        logger.info(adr_title_slug_from_file(Path(file)))

    def print_title_lowercase(self, file: str) -> None:
        logger.info(adr_title_lowercase_from_file(Path(file)))

    def sync_filename(self, file: str) -> None:
        path = Path(file)

        self._verify_adr_filename_format(path, check_title_format=False)

        renamed_path = self._sync_adr_filename(path, path.stem.split("-", 1)[0])

        if path != renamed_path:
            logger.info(f"File renamed to '{str(renamed_path)}'.")
        else:
            logger.info("File name already up-to-date.")

    ###########################################
    # CHECK ADR REPO
    ###########################################
    def check_adr_repo(self, check_no_proposed: bool = True) -> None:
        at_least_one_check_failed = self._check_adr_repo(check_no_proposed)

        if at_least_one_check_failed:
            raise PyadrAdrRepoChecksFailedError
        else:
            logger.info("All checks passed.")

    def _check_adr_repo(self, check_no_proposed: bool = False) -> bool:
        at_least_one_check_failed = False

        adr_files = self._list_adr_files()

        try:
            self._check_adr_numbers_unique(adr_files)
        except PyadrSomeAdrIdsNotUniqueError:
            at_least_one_check_failed = True

        adrs_with_invalid_content_format = (
            self._filter_adrs_with_invalid_content_format(adr_files)  # noqa
        )
        if adrs_with_invalid_content_format:
            at_least_one_check_failed = True

        adr_files_checked_for_content_format = [
            file for file in adr_files if file not in adrs_with_invalid_content_format
        ]

        try:
            self._verify_adr_filenames(
                adr_files_checked_for_content_format,
                status=STATUS_ANY_WITH_ID,
                check_title_format=True,
            )
        except PyadrSomeAdrFilenamesIncorrectError:
            at_least_one_check_failed = True

        if check_no_proposed:
            try:
                self._check_no_adr_is_proposed(adr_files_checked_for_content_format)
            except PyadrSomeAdrStatusesAreProposedError:
                at_least_one_check_failed = True

        return at_least_one_check_failed

    def _check_adr_numbers_unique(self, adr_files: List[Path]) -> None:
        rex = re.compile(VALID_ADR_FILENAME_WITH_ID_REGEX)
        adrs_with_valid_filenames = [file for file in adr_files if rex.match(file.name)]
        unique_numbers = set(
            [file.stem.split("-", 1)[0] for file in adrs_with_valid_filenames]
        )
        adrs_aggregated_by_number = [
            [file for file in adrs_with_valid_filenames if file.stem.startswith(number)]
            for number in unique_numbers
        ]
        adrs_with_duplicate_number = list(
            filter(lambda x: len(x) > 1, adrs_aggregated_by_number)
        )
        if adrs_with_duplicate_number:
            logger.error(
                "ADRs must have a unique number, "
                "but the following files have the same number:"
            )
            for files in sorted(adrs_with_duplicate_number):
                logger.error(f"  => {[str(file) for file in sorted(files)]}.")
            raise PyadrSomeAdrIdsNotUniqueError

    def _filter_adrs_with_invalid_content_format(
        self, adr_files: List[Path]
    ) -> List[Path]:
        adr_files_with_invalid_content_format = []
        for adr in adr_files:
            try:
                adr_title_status_and_date_from_file(adr)
            except PyadrAdrFormatError:
                adr_files_with_invalid_content_format.append(adr)

        if adr_files_with_invalid_content_format:
            logger.error(
                "ADR must be of format:"
                "\n" + VALID_ADR_CONTENT_FORMAT + ""
                "but the following files where not:"
            )
            for file in sorted(adr_files_with_invalid_content_format):
                logger.error(f"  => '{str(file)}'.")
        return adr_files_with_invalid_content_format

    def _check_no_adr_is_proposed(self, adr_files: List[Path]) -> None:
        def adr_has_status(adr_path: Path, target_status: str) -> bool:
            (
                _,
                (status, _),
                _,
            ) = adr_title_status_and_date_from_file(adr_path)

            return status == target_status

        adrs_with_status_proposed = [
            file for file in adr_files if adr_has_status(file, STATUS_PROPOSED)
        ]

        if adrs_with_status_proposed:
            logger.error("ADR(s) must not have their status set to 'proposed', " "but:")
            for file in sorted(adrs_with_status_proposed):
                logger.error(f"  => '{str(file)}' has status 'proposed'.")
            raise PyadrSomeAdrStatusesAreProposedError

    def _verify_adr_filename(
        self, adr_path: Path, status: str = None, check_title_format: bool = True
    ) -> None:
        error_messages = self._verify_adr_filenames(
            [adr_path], status, check_title_format, log_and_raise=False
        )
        if error_messages:
            for message in error_messages:
                logger.error(message)
            raise PyadrAdrFilenameIncorrectError(adr_path)

    def _verify_adr_filenames(
        self,
        adr_files: List[Path],
        status: str = None,
        check_title_format: bool = True,
        log_and_raise: bool = True,
    ) -> Optional[List[str]]:
        """
        Verify a list of ADR filenames to make sur that:

        * the format of the ID portion of the filename is correct
        * the title portion of the filename is synched with the title of the ADR

        Args:
            adr_files: list of ADR files
            status: either `None` or a valid status ;
                    if `None` and the list contains only one file, then status will be
                    fetched from the file content ;
                    if `None` and the list contains more than one file, then status will
                    be set to `STATUS_ANY_WITH_ID`
            check_title_format: if True, will check the format of the title portion of
                                the ADR file
            log_and_raise: if True, will log errors found on filenames and will raise
                           an error

        Returns: an optional list of error messages

        """

        def title_slug_correct_and_title_slug(file: Path) -> Tuple[bool, str]:
            title_slug = adr_title_slug_from_file(file)

            try:
                title_in_filename = file.stem.split("-", 1)[1]
            except IndexError:
                title_in_filename = ""

            return title_in_filename != title_slug, title_slug

        if len(adr_files) == 1:
            status = self._resolve_status(adr_files[0], status)
        else:
            if status is None:
                status = STATUS_ANY_WITH_ID
        full_or_skip_title = self._resolve_regex_type(check_title_format)

        filenames_correctness_status = {}
        for file in sorted(adr_files):
            filenames_correctness_status[file] = {
                "format_not_valid": not self._adr_filename_format_correct(
                    file, status, check_title_format
                ),
                "with_incorrect_title_slug": title_slug_correct_and_title_slug(file),
            }

        error_messages = []
        for file, error_status in filenames_correctness_status.items():
            if error_status["format_not_valid"]:
                error_messages.append(
                    f"  => '{str(file)}' does not start with "
                    f"'{REGEX_ERROR_MESSAGES[status]['id_prefix']}'."
                )
            if error_status["with_incorrect_title_slug"][0]:  # type: ignore
                error_messages.append(
                    f"  => '{str(file)}' does not have the correct title slug "  # type: ignore  # noqa
                    f"('{error_status['with_incorrect_title_slug'][1]}')."
                    # type: ignore  # noqa
                )

        if error_messages:
            error_messages.sort()
            error_messages.insert(
                0, REGEX_ERROR_MESSAGES[status][full_or_skip_title] + ", but:"
            )
            if log_and_raise:
                for message in error_messages:
                    logger.error(message)
                raise PyadrSomeAdrFilenamesIncorrectError
            else:
                return error_messages
        else:
            return None

    def _list_adr_files(self) -> List[Path]:
        adr_files = [
            file
            for file in Path(self.config["adr"]["records-dir"]).glob("*.md")
            if file.name not in ["template.md", "index.md"]
        ]
        return adr_files

    ###########################################
    # SHARED FUNC
    ###########################################
    def verify_adr_dir_exists(self):
        adr_repo_path = Path(self.config["adr"]["records-dir"])

        logger.info(f"Verifying adr repo directory '{adr_repo_path}' exists... ")
        if not adr_repo_path.exists():
            logger.error(
                f"Directory '{adr_repo_path}/' does not exist. "
                "Initialise your ADR repo first."
            )
            raise PyadrAdrDirectoryDoesNotExistsError()
        logger.log("VERBOSE", "... done.")

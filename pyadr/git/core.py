import re
from pathlib import Path
from typing import List, Tuple

from loguru import logger

from pyadr.const import STATUS_PROPOSED, VALID_ADR_CONTENT_FORMAT
from pyadr.content_utils import (
    adr_title_slug,
    adr_title_slug_from_content_stream,
    retrieve_title_status_and_date_from_madr_content_stream,
)
from pyadr.core import AdrCore
from pyadr.exceptions import PyadrAdrFormatError
from pyadr.git.const import GIT_ADR_DEFAULT_SETTINGS
from pyadr.git.exceptions import (
    PyadrGitPreMergeChecksFailedError,
    PyadrSomeAdrFilenamesIncorrectError,
    PyadrSomeAdrNumbersNotUniqueError,
    PyadrSomeAdrStatusesAreProposedError,
)
from pyadr.git.utils import (
    create_feature_branch_and_checkout,
    get_verified_repo_client,
    verify_branch_does_not_exist,
    verify_index_empty,
    verify_main_branch_exists,
)


class GitAdrCore(AdrCore):
    def __init__(self):
        super().__init__(GIT_ADR_DEFAULT_SETTINGS)

    ###########################################
    # PROPERTIES
    ###########################################
    @property
    def commit_msg_prefix(self) -> str:
        if self.config.getboolean("adr-only-repo"):
            return "feat(adr):"
        else:
            return "docs(adr):"

    ###########################################
    # GIT INIT ADR
    ###########################################
    def git_init_adr_repo(self, force: bool = False) -> None:
        repo = get_verified_repo_client(Path.cwd())

        verify_index_empty(repo)

        init_branch_name = "adr-init-repo"
        verify_branch_does_not_exist(repo, init_branch_name)

        created_files = self.init_adr_repo(force=force)

        if "master" not in repo.heads:
            logger.info("Git repo empty. Will commit files to 'master'.")
        else:
            create_feature_branch_and_checkout(repo, init_branch_name)

        repo.index.add([str(p) for p in created_files])

        message = f"{self.commit_msg_prefix} initialise adr repository"
        repo.index.commit(message)

        logger.info(
            f"Files committed to branch '{repo.head.ref.name}' "
            f"with commit message '{message}'."
        )
        logger.info("ADR Git repo initialised.")

    ###########################################
    # GIT NEW ADR
    ###########################################
    def git_new_adr(self, title: str, pre_checks: bool = True) -> None:
        repo = get_verified_repo_client(Path.cwd())

        if pre_checks:
            self.verify_adr_dir_exists()
            verify_main_branch_exists(repo, branch="master")

        verify_index_empty(repo)

        adr_branch_name = f"adr-{adr_title_slug(title)}"
        verify_branch_does_not_exist(repo, adr_branch_name)

        new_adr_path = self.new_adr(title, pre_checks=False)

        create_feature_branch_and_checkout(repo, adr_branch_name)

        repo.index.add([str(new_adr_path)])

        logger.info(f"File '{new_adr_path}' staged.")

        logger.info("New ADR added to Git repo.")

    ###########################################
    # GIT PRE MERGE CHECKS
    ###########################################
    def git_pre_merge_checks(self) -> None:
        at_least_one_check_failed = False

        adr_files = self._list_adr_files()

        try:
            self._check_adr_numbers_unique(adr_files)
        except PyadrSomeAdrNumbersNotUniqueError:
            at_least_one_check_failed = True

        adrs_with_invalid_content_format = self._filter_adrs_with_invalid_content_format(  # noqa
            adr_files
        )
        if adrs_with_invalid_content_format:
            at_least_one_check_failed = True

        adr_files_checked_for_content_format = [
            file for file in adr_files if file not in adrs_with_invalid_content_format
        ]

        try:
            self._check_all_adr_filenames_correct(adr_files_checked_for_content_format)
        except PyadrSomeAdrFilenamesIncorrectError:
            at_least_one_check_failed = True

        try:
            self._check_no_adr_is_proposed(adr_files_checked_for_content_format)
        except PyadrSomeAdrStatusesAreProposedError:
            at_least_one_check_failed = True

        if at_least_one_check_failed:
            raise PyadrGitPreMergeChecksFailedError
        else:
            logger.info("All checks passed.")

    def _check_adr_numbers_unique(self, adr_files: List[Path]) -> None:
        rex = re.compile(r"^[0-9][0-9][0-9][0-9]-.*\.md")
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
                "ADR files must have a unique number, "
                "but the following files have the same number:"
            )
            for files in sorted(adrs_with_duplicate_number):
                logger.error(f"  => {[str(file) for file in sorted(files)]}.")
            raise PyadrSomeAdrNumbersNotUniqueError

    def _filter_adrs_with_invalid_content_format(
        self, adr_files: List[Path]
    ) -> List[Path]:
        adr_files_with_invalid_content_format = []
        for adr in adr_files:
            with adr.open() as f:
                try:
                    retrieve_title_status_and_date_from_madr_content_stream(f)
                except PyadrAdrFormatError:
                    adr_files_with_invalid_content_format.append(adr)

        if adr_files_with_invalid_content_format:
            logger.error(
                "ADR file names must be of format:"
                "\n" + VALID_ADR_CONTENT_FORMAT + ""
                "but the following files where not:"
            )
            for file in sorted(adr_files_with_invalid_content_format):
                logger.error(f"  => '{str(file)}'.")
        return adr_files_with_invalid_content_format

    def _check_no_adr_is_proposed(self, adr_files: List[Path]) -> None:
        def adr_has_status(adr_path: Path, target_status: str) -> bool:
            with adr_path.open() as f:
                (
                    _,
                    (status, _),
                    _,
                ) = retrieve_title_status_and_date_from_madr_content_stream(
                    f, stream_source=str(adr_path)
                )

            return status == target_status

        adrs_with_status_proposed = [
            file for file in adr_files if adr_has_status(file, STATUS_PROPOSED)
        ]

        if adrs_with_status_proposed:
            logger.error(
                "ADR files must not have their status set to 'proposed', "
                "but the following files do:"
            )
            for file in sorted(adrs_with_status_proposed):
                logger.error(f"  => '{str(file)}'.")
            raise PyadrSomeAdrStatusesAreProposedError

    def _check_all_adr_filenames_correct(self, adr_files: List[Path]) -> None:
        def has_filename_without_title_slug_and_title_slug(
            file: Path,
        ) -> Tuple[bool, str]:
            with file.open() as f:
                title_slug = adr_title_slug_from_content_stream(
                    f, stream_source=str(file)
                )

            try:
                title_part = file.stem.split("-", 1)[1]
            except IndexError:
                title_part = ""

            return title_part != title_slug, title_slug

        rex = re.compile(r"^[0-9][0-9][0-9][0-9]-.*\.md")
        filenames_correctness_status = {
            file: {
                "starts_incorrectly": not rex.match(file.name),
                "with_incorrect_title_slug": has_filename_without_title_slug_and_title_slug(  # noqa
                    file
                ),
            }
            for file in sorted(adr_files)
        }

        error_messages = []
        for file, status in filenames_correctness_status.items():
            if status["starts_incorrectly"]:
                error_messages.append(
                    f"  => '{str(file)}' does not start with 4 digits followed by '-'."
                )
            if status["with_incorrect_title_slug"][0]:  # type: ignore
                error_messages.append(
                    f"  => '{str(file)}' should end with "  # type: ignore
                    f"'{status['with_incorrect_title_slug'][1]}'."  # type: ignore
                )
        if error_messages:
            logger.error(
                "ADR file names must be of format "
                "'[0-9][0-9][0-9][0-9]-<adr-title-in-slug-format>.md', "
                "but the following files where not:"
            )
            for message in sorted(error_messages):
                logger.error(message)
            raise PyadrSomeAdrFilenamesIncorrectError

    def _list_adr_files(self) -> List[Path]:
        adr_files = [
            file
            for file in Path(self.config["records-dir"]).glob("*.md")
            if file.name not in ["template.md", "index.md"]
        ]
        return adr_files

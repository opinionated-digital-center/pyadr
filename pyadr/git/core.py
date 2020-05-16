import re
from pathlib import Path
from typing import List, Tuple

from git import Repo
from loguru import logger
from slugify import slugify

from pyadr.const import (
    STATUS_PROPOSED,
    VALID_ADR_CONTENT_FORMAT,
    VALID_ADR_FILENAME_REGEX,
)
from pyadr.content_utils import (
    adr_title_slug_from_file,
    retrieve_title_status_and_date_from_madr,
)
from pyadr.core import AdrCore
from pyadr.exceptions import PyadrAdrFormatError
from pyadr.git.const import GIT_ADR_DEFAULT_SETTINGS
from pyadr.git.exceptions import (
    PyadrGitAdrNotStagedOrCommittedError,
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
        self._repo = None

    ###########################################
    # PROPERTIES
    ###########################################
    @property
    def commit_msg_prefix(self) -> str:
        if self.config.getboolean("adr-only-repo"):
            return "feat(adr):"
        else:
            return "docs(adr):"

    @property
    def repo(self) -> Repo:
        if not self._repo:
            self._repo = get_verified_repo_client(Path.cwd())
        return self._repo

    ###########################################
    # GIT INIT ADR
    ###########################################
    def git_init_adr_repo(self, force: bool = False) -> None:
        verify_index_empty(self.repo)

        init_branch_name = "adr-init-repo"
        verify_branch_does_not_exist(self.repo, init_branch_name)

        created_files = self.init_adr_repo(force=force)

        if "master" not in self.repo.heads:
            logger.info("Git repo empty. Will commit files to 'master'.")
        else:
            create_feature_branch_and_checkout(self.repo, init_branch_name)

        self.repo.index.add([str(p) for p in created_files])

        message = f"{self.commit_msg_prefix} initialise adr repository"
        self.repo.index.commit(message)

        logger.info(
            f"Files committed to branch '{self.repo.head.ref.name}' "
            f"with commit message '{message}'."
        )
        logger.info("ADR Git repo initialised.")

    ###########################################
    # GIT NEW ADR
    ###########################################
    def git_new_adr(self, title: str, pre_checks: bool = True) -> None:
        if pre_checks:
            self.verify_adr_dir_exists()
            verify_main_branch_exists(self.repo, branch="master")

        verify_index_empty(self.repo)

        adr_branch_name = f"adr-{slugify(title)}"
        verify_branch_does_not_exist(self.repo, adr_branch_name)

        new_adr_path = self.new_adr(title, pre_checks=False)

        create_feature_branch_and_checkout(self.repo, adr_branch_name)

        self.repo.index.add([str(new_adr_path)])

        logger.info(f"File '{new_adr_path}' staged.")

        logger.info("New ADR added to Git repo.")

    ###########################################
    # ACCEPT / REJECT
    ###########################################
    def git_accept_or_reject(
        self, status: str, toc: bool = False, commit: bool = False,
    ) -> None:
        processed_adr = self.accept_or_reject(status, toc)

        if commit:
            self.repo.index.commit(
                f"{self.commit_msg_prefix} [{status}] {processed_adr.stem}"
            )

    def _verify_proposed_adr(self):
        proposed_adr = super()._verify_proposed_adr()
        self._verify_file_staged_or_committed(proposed_adr)
        return proposed_adr

    def _verify_file_staged_or_committed(self, path: Path) -> None:
        file_staged = str(path) in [
            d.a_path
            for d in list(
                self.repo.index.diff(self.repo.head.commit).iter_change_type("D")
            )
        ]
        file_committed = str(path) in list(self.repo.head.commit.stats.files.keys())
        if not (file_staged or file_committed):
            logger.error(f"File {path} should be staged or committed first.")
            raise PyadrGitAdrNotStagedOrCommittedError(path)

    def _apply_filepath_update(self, path: Path, renamed_path: Path) -> None:
        self.repo.git.mv(str(path), str(renamed_path))

    ###########################################
    # GENERATE TOC
    ###########################################
    def generate_toc(self, pre_checks: bool = True) -> Path:
        toc_path = super().generate_toc()
        self.repo.index.add([str(toc_path)])
        return toc_path

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
        rex = re.compile(VALID_ADR_FILENAME_REGEX)
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
            try:
                retrieve_title_status_and_date_from_madr(adr)
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
            (_, (status, _), _,) = retrieve_title_status_and_date_from_madr(adr_path)

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
            title_slug = adr_title_slug_from_file(file)

            try:
                title_part = file.stem.split("-", 1)[1]
            except IndexError:
                title_part = ""

            return title_part != title_slug, title_slug

        rex = re.compile(VALID_ADR_FILENAME_REGEX)
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

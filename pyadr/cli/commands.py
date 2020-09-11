"""Console script for pyadr."""
from typing import List

import cleo

from pyadr.const import STATUS_ACCEPTED, STATUS_REJECTED
from pyadr.core import AdrCore
from pyadr.exceptions import PyadrAdrRepoChecksFailedError


class BaseCommand(cleo.Command):
    def __init__(self):
        super().__init__()
        self.adr_core = AdrCore()


class ConfigCommand(BaseCommand):
    """
    Configure an ADR repository

    config
        {setting? : Configuration setting.}
        {value? : Configuration value.}
        {--l|list : List configuration settings.}
        {--u|unset : Unset configuration setting.}
    """

    def handle(self):
        if self.option("list"):
            self.adr_core.list_config()
        elif self.option("unset"):
            if not self.argument("setting"):
                self.line_error('Not enough arguments (missing: "words").')
            self.adr_core.unset_config_setting(self.argument("setting"))
        elif self.argument("setting"):
            if self.argument("value"):
                self.adr_core.configure(
                    self.argument("setting"), self.argument("value")
                )
            else:
                self.adr_core.print_config_setting(self.argument("setting"))


class InitCommand(BaseCommand):
    """
    Initialise an ADR repository

    init
        {--f|force : If set, will erase existing repository.}
    """

    def handle(self):
        self.adr_core.init_adr_repo(force=self.option("force"))


class NewCommand(BaseCommand):
    """
    Create an new ADR

    new
        {words* : Words in the title.}
    """

    def handle(self):
        self.adr_core.new_adr(title=" ".join(self.argument("words")))


class ProposeCommand(NewCommand):
    """
    Propose a new ADR (same as 'new' command)

    propose
        {words* : Words in the title}
    """


class AcceptCommand(BaseCommand):
    """
    Accept a proposed ADR by assigning an ID, updating filename, status and date

    accept
        {file : ADR file.}
        {--t|toc : If set, generates also the table of content.}
    """

    def handle(self):
        self.adr_core.accept_or_reject(
            self.argument("file"), STATUS_ACCEPTED, self.option("toc")
        )


class RejectCommand(BaseCommand):
    """
    Reject a proposed ADR by assigning an ID, updating filename, status and date

    reject
        {file : ADR file.}
        {--t|toc : If set, generates also the table of content.}
    """

    def handle(self):
        self.adr_core.accept_or_reject(
            self.argument("file"), STATUS_REJECTED, self.option("toc")
        )


class GenerateTocCommand(BaseCommand):
    """
    Generate a table of content of the ADRs

    toc
    """

    def handle(self):
        self.adr_core.generate_toc()


class CheckAdrRepoCommand(BaseCommand):
    """
    Perform sanity checks typically required on ADR files before merging a Pull Request

    check-adr-repo
        {--p|no-proposed : If set, will also check that there are no proposed ADR.}
    """

    def handle(self):
        try:
            self.adr_core.check_adr_repo(self.option("no-proposed"))
        except PyadrAdrRepoChecksFailedError:
            return 1


class HelperSlugCommand(BaseCommand):
    """
    Return the ADR's title in slug format

    slug
        {file : ADR file.}
    """

    def handle(self):
        self.adr_core.print_title_slug(self.argument("file"))


class HelperLowercaseCommand(BaseCommand):
    """
    Return the ADR's title in lowercase

    lowercase
        {file : ADR file.}
    """

    def handle(self):
        self.adr_core.print_title_lowercase(self.argument("file"))


class HelperSyncFilenameCommand(BaseCommand):
    """
    Sync the ADR's filename with its actual title

    sync-filename
        {file : ADR file.}
    """

    def handle(self):
        self.adr_core.sync_filename(self.argument("file"))


class HelperCommand(BaseCommand):
    """
    Helper command generating and syncing various useful things

    helper
    """

    commands: List[BaseCommand] = []

    def __init__(self):
        self.commands.extend(
            [
                HelperSlugCommand(),
                HelperLowercaseCommand(),
                HelperSyncFilenameCommand(),
            ]
        )
        super().__init__()

    def handle(self):
        return self.call("help", self.config.name)

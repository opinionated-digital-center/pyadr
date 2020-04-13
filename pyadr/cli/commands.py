"""Console script for pyadr."""

import cleo

from pyadr.const import STATUS_ACCEPTED, STATUS_REJECTED
from pyadr.core import AdrCore
from pyadr.exceptions import PyadrError


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
        try:
            if self.option("list"):
                self.adr_core.list_config()
            elif self.option("unset"):
                self.adr_core.unset_config_setting(self.argument("setting"))
            elif not self.argument("value"):
                self.adr_core.print_config_setting(self.argument("setting"))
            else:
                self.adr_core.configure(
                    self.argument("setting"), self.argument("value")
                )
        except PyadrError:
            return 1


class InitCommand(BaseCommand):
    """
    Initialise an ADR repository

    init
        {--f|force : If set, will erase existing repository.}
    """

    def handle(self):
        try:
            self.adr_core.init_adr_repo(force=self.option("force"))
        except PyadrError:
            return 1


class NewCommand(BaseCommand):
    """
    Create an new ADR

    new
        {words* : Words in the title.}
    """

    def handle(self):
        try:
            self.adr_core.new_adr(title=" ".join(self.argument("words")))
        except PyadrError:
            return 1


class ProposeCommand(NewCommand):
    """
    Propose a new ADR (same as 'new' command... Here for coherence)

    propose
        {words* : Words in the title}
    """


class AcceptCommand(BaseCommand):
    """
    Accept a proposed ADR

    accept
        {--t|toc : If set, generates also the table of content.}
    """

    def handle(self):
        try:
            self.adr_core.accept_or_reject(STATUS_ACCEPTED, self.option("toc"))
        except PyadrError:
            return 1


class RejectCommand(BaseCommand):
    """
    Reject a proposed ADR

    reject
        {--t|toc : If set, generates also the table of content.}
    """

    def handle(self):
        try:
            self.adr_core.accept_or_reject(STATUS_REJECTED, self.option("toc"))
        except PyadrError:
            return 1


class GenerateTocCommand(BaseCommand):
    """
    Generate a table of content of the ADRs

    generate-toc
    """

    def handle(self):
        try:
            self.adr_core.generate_toc()
        except PyadrError:
            return 1

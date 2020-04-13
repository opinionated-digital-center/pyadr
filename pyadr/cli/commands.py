"""Console script for pyadr."""

import cleo

from pyadr.const import STATUS_ACCEPTED, STATUS_REJECTED
from pyadr.core import (
    accept_or_reject,
    configure,
    generate_toc,
    init_adr_repo,
    list_config,
    new_adr,
    print_config_item,
    unset_config_item,
)
from pyadr.exceptions import PyadrError


class ConfigCommand(cleo.Command):
    """
    Configure an ADR repository

    config
        {item? : Configuration item.}
        {value? : Configuration value.}
        {--l|list : List configuration settings.}
        {--u|unset : Unset configuration setting.}
    """

    def handle(self):
        try:
            if self.option("list"):
                list_config()
            elif self.option("unset"):
                unset_config_item(self.argument("item"))
            elif not self.argument("value"):
                print_config_item(self.argument("item"))
            else:
                configure(self.argument("item"), self.argument("value"))
        except PyadrError:
            return 1


class InitCommand(cleo.Command):
    """
    Initialise an ADR repository

    init
        {--f|force : If set, will erase existing repository.}
    """

    def handle(self):
        try:
            init_adr_repo(force=self.option("force"))
        except PyadrError:
            return 1


class NewCommand(cleo.Command):
    """
    Create an new ADR

    new
        {words* : Words in the title.}
    """

    def handle(self):
        try:
            new_adr(title=" ".join(self.argument("words")))
        except PyadrError:
            return 1


class AcceptCommand(cleo.Command):
    """
    Accept a proposed ADR

    accept
        {--t|toc : If set, generates also the table of content.}
    """

    def handle(self):
        try:
            accept_or_reject(STATUS_ACCEPTED, self.option("toc"))
        except PyadrError:
            return 1


class RejectCommand(cleo.Command):
    """
    Reject a proposed ADR

    reject
        {--t|toc : If set, generates also the table of content.}
    """

    def handle(self):
        try:
            accept_or_reject(STATUS_REJECTED, self.option("toc"))
        except PyadrError:
            return 1


class GenerateTocCommand(cleo.Command):
    """
    Generate a table of content of the ADRs

    generate-toc
    """

    def handle(self):
        try:
            generate_toc()
        except PyadrError:
            return 1

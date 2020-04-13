"""Console script for pyadr."""
import cleo

from pyadr.const import CWD
from pyadr.exceptions import PyadrError
from pyadr.git.core import git_init_adr_repo, git_new_adr


class ConfigCommand(cleo.Command):
    """
    Configure an ADR repository

    config
        {item? : Configuration item.}
        {value? : Configuration value.}
        {--l|list : List configuration settings.}
        {--u|unset : Unset configuration setting.}
    """


class GitInitCommand(cleo.Command):
    """
    Initialise a Git ADR repository

    init
        {--f|force : If set, will erase existing ADR directory}
    """

    def handle(self):
        try:
            git_init_adr_repo(CWD, force=self.option("force"))
        except PyadrError:
            return 1


class GitNewCommand(cleo.Command):
    """
    Create an new ADR

    new
        {words* : Words in the title}
    """

    def handle(self):
        try:
            git_new_adr(CWD, title=" ".join(self.argument("words")))
        except PyadrError:
            return 1

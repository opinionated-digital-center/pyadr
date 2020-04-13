"""Console script for pyadr."""
import cleo

from pyadr.core import configure, list_config, print_config_item, unset_config_item
from pyadr.exceptions import PyadrError
from pyadr.git.core import git_init_adr_repo, git_new_adr


class GitConfigCommand(cleo.Command):
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


class GitInitCommand(cleo.Command):
    """
    Initialise a Git ADR repository

    init
        {--f|force : If set, will erase existing ADR directory}
    """

    def handle(self):
        try:
            git_init_adr_repo(force=self.option("force"))
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
            git_new_adr(title=" ".join(self.argument("words")))
        except PyadrError:
            return 1

"""Console script for git adr."""
import cleo

from pyadr.exceptions import PyadrError
from pyadr.git.core import GitAdrCore


class BaseGitCommand(cleo.Command):
    def __init__(self):
        super().__init__()
        self.git_adr_core = GitAdrCore()


class GitConfigCommand(BaseGitCommand):
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
                self.git_adr_core.list_config()
            elif self.option("unset"):
                self.git_adr_core.unset_config_setting(self.argument("setting"))
            elif not self.argument("value"):
                self.git_adr_core.print_config_setting(self.argument("setting"))
            else:
                self.git_adr_core.configure(
                    self.argument("setting"), self.argument("value")
                )
        except PyadrError:
            return 1


class GitInitCommand(BaseGitCommand):
    """
    Initialise a Git ADR repository

    init
        {--f|force : If set, will erase existing ADR directory.}
        {--a|adr-only-repo : ADR only repo. This will affect the prefixes of
                             commit messages}
    """

    def handle(self):
        if self.option("adr-only-repo"):
            self.git_adr_core.config["adr-only-repo"] = "true"

        try:
            self.git_adr_core.git_init_adr_repo(force=self.option("force"))
        except PyadrError:
            return 1


class GitNewCommand(BaseGitCommand):
    """
    Create an new ADR

    new
        {words* : Words in the title}
    """

    def handle(self):
        try:
            self.git_adr_core.git_new_adr(title=" ".join(self.argument("words")))
        except PyadrError:
            return 1


class GitProposeCommand(GitNewCommand):
    """
    Create an proposal ADR (same as new... Here for coherence)

    propose
        {words* : Words in the title}
    """

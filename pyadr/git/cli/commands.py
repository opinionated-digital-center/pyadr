"""Console script for pyadr."""
import cleo

from pyadr.const import CWD
from pyadr.exceptions import PyadrError
from pyadr.git.core import git_init_adr_repo


class GitInitCommand(cleo.Command):
    """
    Initialise a git ADR repository

    init
        {--f|force : If set, will erase existing ADR directory}
    """

    def handle(self):
        try:
            git_init_adr_repo(CWD, force=self.option("force"))
        except PyadrError:
            return 1

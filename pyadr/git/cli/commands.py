"""Console script for git adr."""
import cleo

from pyadr.const import STATUS_ACCEPTED, STATUS_REJECTED
from pyadr.git.core import GitAdrCore
from pyadr.git.exceptions import PyadrGitError, PyadrGitPreMergeChecksFailedError


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
        except PyadrGitError:
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
        except PyadrGitError:
            return 1


class GitProposeCommand(GitNewCommand):
    """
    Create an proposal ADR (same as new... Here for coherence)

    propose
        {words* : Words in the title}
    """


class GitAcceptCommand(BaseGitCommand):
    """
    Accept a proposed ADR

    accept
        {--t|toc : If set, generates also the table of content.}
        {--c|commit : If set, commits the processed ADR.}
    """

    def handle(self):
        self.git_adr_core.git_accept_or_reject(
            STATUS_ACCEPTED, self.option("toc"), self.option("commit")
        )


class GitRejectCommand(BaseGitCommand):
    """
    Reject a proposed ADR

    reject
        {--t|toc : If set, generates also the table of content.}
        {--c|commit : If set, commits the processed ADR.}
    """

    def handle(self):
        self.git_adr_core.git_accept_or_reject(
            STATUS_REJECTED, self.option("toc"), self.option("commit")
        )


class GitPreMergeChecksCommand(BaseGitCommand):
    """
    Performs sanity checks typically required on ADR files before merging a Pull Request

    pre-merge-checks
    """

    def handle(self):
        try:
            self.git_adr_core.git_pre_merge_checks()
        except PyadrGitPreMergeChecksFailedError:
            return 1


class GitHelperSlugCommand(BaseGitCommand):
    """
    Print the ADR's title in slug format

    slug
        {file : ADR file to use as source.}
    """

    def handle(self):
        self.git_adr_core.print_title_slug(self.argument("file"))


class GitHelperLowercaseCommand(BaseGitCommand):
    """
    Print the ADR's title in lowercase

    lowercase
        {file : ADR file to use as source.}
    """

    def handle(self):
        self.git_adr_core.print_title_lowercase(self.argument("file"))


class GitHelperResyncFilenameCommand(BaseGitCommand):
    """
    Resync the ADR's filename with its actual title

    resync-filename
        {file : ADR file to use as source.}
    """

    def handle(self):
        self.git_adr_core.resync_filename(self.argument("file"))


class GitHelperCommitMessageCommand(BaseGitCommand):
    """
    Print the commit message related to the ADR

    commit-message
        {file : ADR file to use as source.}
    """

    def handle(self):
        self.git_adr_core.print_commit_message(self.argument("file"))


class GitHelperBranchTitleCommand(BaseGitCommand):
    """
    Print the branch title related to the ADR's review request

    branch-title
        {file : ADR file to use as source.}
    """

    def handle(self):
        self.git_adr_core.print_branch_title(self.argument("file"))


class GitHelperCommand(BaseGitCommand):
    """
    Helper command generating and syncing various useful things

    helper
    """

    commands = [
        GitHelperSlugCommand(),
        GitHelperLowercaseCommand(),
        GitHelperResyncFilenameCommand(),
        GitHelperCommitMessageCommand(),
        GitHelperBranchTitleCommand(),
    ]

    def handle(self):
        return self.call("help", self.config.name)

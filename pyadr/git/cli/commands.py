"""Console script for git adr."""
# flake8: noqa: B950
from typing import Callable, List

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
            if not self.argument("setting"):
                self.line_error('Not enough arguments (missing: "words").')
            self.git_adr_core.unset_config_setting(self.argument("setting"))
        elif self.argument("setting"):
            if self.argument("value"):
                self.git_adr_core.configure(
                    self.argument("setting"), self.argument("value")
                )
            else:
                self.git_adr_core.print_config_setting(self.argument("setting"))


class GitInitCommand(BaseGitCommand):
    """
    Initialise a Git ADR repository

    init
        {--f|force : If set, will erase existing ADR directory.}
        {--a|adr-only-repo : ADR only repo. This will affect the prefixes of
                             commit messages.}
    """

    def handle(self):
        if self.option("adr-only-repo"):
            self.git_adr_core.config["git"]["adr-only-repo"] = "true"

        try:
            self.git_adr_core.git_init_adr_repo(force=self.option("force"))
        except PyadrGitError:
            return 1


class GitNewCommand(BaseGitCommand):
    """
    Create an new ADR, create a feature branch and stage new ADR in feature branch

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
    Propose a new ADR (same as 'new' command)

    propose
        {words* : Words in the title}
    """


class GitAcceptCommand(BaseGitCommand):
    """
    Accept a proposed ADR by assigning an ID, updating filename, status and date, and stage to the current branch

    accept
        {file : ADR file.}
        {--t|toc : If set, generates and stages the table of content after the ADR's
                   update.}
        {--c|commit : If set, commits the updated ADR.}
    """

    def handle(self):
        self.git_adr_core.git_accept_or_reject(
            self.argument("file"),
            STATUS_ACCEPTED,
            self.option("toc"),
            self.option("commit"),
        )


class GitRejectCommand(BaseGitCommand):  # noqa
    """
    Reject a proposed ADR by assigning an ID, updating filename, status and date, and stage to the current branch

    reject
        {file : ADR file.}
        {--t|toc : If set, generates and stages the table of content after the ADR's
                   update.}
        {--c|commit : If set, commits the updated ADR.}
    """

    def handle(self):
        self.git_adr_core.git_accept_or_reject(
            self.argument("file"),
            STATUS_REJECTED,
            self.option("toc"),
            self.option("commit"),
        )


class GitCommitCommand(BaseGitCommand):
    """
    Commit an ADR

    commit
        {file : ADR file.}
    """

    def handle(self):
        self.git_adr_core.commit_adr(self.argument("file"))


class GitPreMergeChecksCommand(BaseGitCommand):
    """
    Perform sanity checks typically required on ADR files before merging a Pull Request

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
        {file : ADR file.}
    """

    def handle(self):
        self.git_adr_core.print_title_slug(self.argument("file"))


class GitHelperLowercaseCommand(BaseGitCommand):
    """
    Print the ADR's title in lowercase

    lowercase
        {file : ADR file.}
    """

    def handle(self):
        self.git_adr_core.print_title_lowercase(self.argument("file"))


class GitHelperSyncFilenameCommand(BaseGitCommand):
    """
    Sync the ADR's filename with its actual title

    sync-filename
        {file : ADR file.}
    """

    def handle(self):
        self.git_adr_core.sync_filename(self.argument("file"))


class GitHelperCommitMessageCommand(BaseGitCommand):
    """
    Print the commit message related to the ADR

    commit-message
        {file : ADR file.}
    """

    def handle(self):
        self.git_adr_core.print_commit_message(self.argument("file"))


class GitHelperBranchTitleCommand(BaseGitCommand):
    """
    Print the branch title related to the ADR's review request

    branch-title
        {file : ADR file.}
    """

    def handle(self):
        self.git_adr_core.print_branch_title(self.argument("file"))


class GitHelperCommand(BaseGitCommand):
    """
    Helper command generating and syncing various useful things

    helper
    """

    commands: List[BaseGitCommand] = []

    def __init__(self):
        self.commands.extend(
            [
                GitHelperSlugCommand(),
                GitHelperLowercaseCommand(),
                GitHelperSyncFilenameCommand(),
                GitHelperCommitMessageCommand(),
                GitHelperBranchTitleCommand(),
            ]
        )
        super().__init__()

    def handle(self):
        return self.call("help", self.config.name)


class GitGenerateTocCommand(BaseGitCommand):
    """
    Generate a table of content of the ADRs

    toc
    """

    def handle(self):
        self.git_adr_core.generate_toc()

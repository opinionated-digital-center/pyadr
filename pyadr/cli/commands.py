"""Console script for pyadr."""
import sys

import cleo

from ..const import ADR_REPO_ABS_PATH, CWD, STATUS_ACCEPTED, STATUS_REJECTED
from ..core import generate_toc, init_adr_repo, new_adr
from ..exceptions import PyadrNoNumberedAdrError
from ..file_utils import rename_reviewed_adr_file, update_adr_title_status


class InitCommand(cleo.Command):
    """
    Initialise an ADR repository

    init
        {--f|force : If set, will erase existing repository}
    """

    def handle(self):
        init_adr_repo(self.option("force"))


class NewCommand(cleo.Command):
    """
    Create an new ADR

    new
        {words* : Words in the title}
    """

    def handle(self):
        new_adr(title=" ".join(self.argument("words")))


class BaseReviewCommand(cleo.Command):
    """
    Base class for review commands
    """

    def handle(self):
        raise NotImplementedError()

    def _accept_or_reject(self, status: str):
        self.line(f"Current Working Directory is: '{CWD}'")
        found_proposed_adrs = sorted(ADR_REPO_ABS_PATH.glob("XXXX-*"))

        if not len(found_proposed_adrs):
            self.line_error(
                "There is no ADR to accept/reject "
                "(should be of format './docs/adr/XXXX-adr-title.md')"
            )
            sys.exit(1)

        elif len(found_proposed_adrs) > 1:
            self.line_error(
                f"There should be only one ADR to accept/reject but there are "
                f"{len(found_proposed_adrs)}:"
            )
            for adr in found_proposed_adrs:
                self.line_error(f"    => './{adr.relative_to(CWD)}'")
            sys.exit(1)

        proposed_adr = found_proposed_adrs[0]
        try:
            reviewed_adr = rename_reviewed_adr_file(proposed_adr, ADR_REPO_ABS_PATH)
        except PyadrNoNumberedAdrError:
            self.line_error(
                "There should be at least one initial reviewed ADR "
                "(usually './docs/adr/0000-record-architecture-decisions.md')."
            )
            sys.exit(1)
        self.line(f"Renamed ADR to: {reviewed_adr}")

        if self.option("toc"):
            path = generate_toc()
            self.line(
                f"Markdown table of content generated in './{path.relative_to(CWD)}'"
            )

        update_adr_title_status(reviewed_adr, status=status)
        self.line(f"Change ADR status to: {status}")


class AcceptCommand(BaseReviewCommand):
    """
    Accept a proposed ADR

    accept
        {--t|toc : If set, generates also the table of content}
    """

    def handle(self):
        self._accept_or_reject(STATUS_ACCEPTED)


class RejectCommand(BaseReviewCommand):
    """
    Reject a proposed ADR

    reject
        {--t|toc : If set, generates also the table of content}
    """

    def handle(self):
        self._accept_or_reject(STATUS_REJECTED)


class GenerateTocCommand(cleo.Command):
    """
    Generate a table of content of the ADRs

    generate-toc
    """

    def handle(self):
        path = generate_toc()
        self.line(f"Markdown table of content generated in './{path.relative_to(CWD)}'")

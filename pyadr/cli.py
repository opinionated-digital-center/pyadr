"""Console script for pyadr."""

import sys

import cleo

from pyadr.core import generate_toc

from . import __version__
from .const import ADR_REPO_ABS_PATH, CWD, STATUS_ACCEPTED, STATUS_REJECTED
from .exceptions import PyadrNoPreviousAdrError
from .file_utils import rename_reviewed_adr_file, update_adr_file_content_to_status


class BaseReviewCommand(cleo.Command):
    """
    Base class for review commands
    """

    def handle(self):
        raise NotImplementedError()

    def _accept_or_reject(self, status: str):
        self.line(f"Current Working Directory is: {CWD}")
        found_proposed_adrs = sorted(ADR_REPO_ABS_PATH.glob("XXXX-*"))

        if not len(found_proposed_adrs):
            self.line_error(
                "There is no ADR to approve/reject "
                "(should be of format 'docs/adr/XXXX-adr-title.md')"
            )
            sys.exit(1)

        elif len(found_proposed_adrs) > 1:
            self.line_error(
                f"There should be only one ADR to approve/reject but there are "
                f"{len(found_proposed_adrs)}:"
            )
            for adr in found_proposed_adrs:
                self.line_error(f"    => '{adr.relative_to(CWD)}'")
            sys.exit(1)

        proposed_adr = found_proposed_adrs[0]
        try:
            reviewed_adr = rename_reviewed_adr_file(proposed_adr, ADR_REPO_ABS_PATH)
        except PyadrNoPreviousAdrError:
            self.line_error(
                "There should be at least one initial reviewed ADR "
                "(usually 'docs/adr/0000-record-architecture-decisions.md')."
            )
            sys.exit(1)
        self.line(f"Renamed ADR to: {reviewed_adr}")

        update_adr_file_content_to_status(reviewed_adr, status)
        self.line(f"Change ADR status to: {status}")


class ApproveCommand(BaseReviewCommand):
    """
    Approve a proposed ADR

    approve
    """

    def handle(self):
        self._accept_or_reject(STATUS_ACCEPTED)


class RejectCommand(BaseReviewCommand):
    """
    Reject a proposed ADR

    reject
    """

    def handle(self):
        self._accept_or_reject(STATUS_REJECTED)


class GenerateTocCommand(cleo.Command):
    """
    Generate a table of content of the ADRs

    generate-toc
    """

    def handle(self):
        generate_toc()
        self.line("Markdown table of content generated in `docs/adr/index.md`")


class Application(cleo.Application):
    def __init__(self):
        super().__init__("ADR Process Tool", __version__)

        self.add(ApproveCommand())
        self.add(RejectCommand())
        self.add(GenerateTocCommand())


def main(args=None):
    return Application().run()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

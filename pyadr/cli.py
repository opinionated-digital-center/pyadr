"""Console script for pyadr."""
import re
import shutil
import sys
from datetime import datetime

import cleo
from slugify import slugify

from pyadr.core import generate_toc

from . import assets  # relative-import the *package* containing the templates
from . import __version__
from .const import (
    ADR_REPO_ABS_PATH,
    ADR_REPO_REL_PATH,
    CWD,
    STATUS_ACCEPTED,
    STATUS_PROPOSED,
    STATUS_REJECTED,
)
from .exceptions import PyadrNoPreviousAdrError
from .file_utils import rename_reviewed_adr_file, update_adr_file_content

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources  # type: ignore


class InitCommand(cleo.Command):
    """
    Initialise an ADR repository

    init
        {--f|force : If set, will erase existing repository}
    """

    def handle(self):
        if self.option("force"):
            if ADR_REPO_ABS_PATH.exists():
                self.line(
                    f"Repository directory exists at '{ADR_REPO_ABS_PATH}/'. Erasing..."
                )
                shutil.rmtree(ADR_REPO_ABS_PATH)
                self.line("... Erased.")

        else:
            if ADR_REPO_ABS_PATH.exists():
                self.line_error(
                    f"Error: directory '{ADR_REPO_ABS_PATH}/' already exists. "
                    "Please erase (with -f) or backup before proceeding."
                )
                sys.exit(1)

        ADR_REPO_ABS_PATH.mkdir(parents=True)

        template_path = ADR_REPO_ABS_PATH / "template.md"
        with template_path.open("w") as f:
            f.write(pkg_resources.read_text(assets, "madr-template.md"))
        self.line(f"Copied MADR template to './{template_path.relative_to(CWD)}'.")

        adr_0000_filename = "0000-record-architecture-decisions.md"
        adr_0000_path = ADR_REPO_ABS_PATH / adr_0000_filename
        with adr_0000_path.open("w") as f:
            today = datetime.today().strftime("%Y-%m-%d")
            f.write(
                re.sub(
                    r"^Date: .*$",
                    f"Date: {today}",
                    pkg_resources.read_text(assets, adr_0000_filename),
                    1,
                    re.MULTILINE,
                )
            )
        self.line(f"Created ADR './{adr_0000_path.relative_to(CWD)}'.")

        adr_madr_filename = "XXXX-use-markdown-architectural-decision-records.md"
        adr_madr_path = ADR_REPO_ABS_PATH / adr_madr_filename
        with adr_madr_path.open("w") as f:
            f.write(pkg_resources.read_text(assets, adr_madr_filename))
        reviewed_adr = rename_reviewed_adr_file(adr_madr_path, ADR_REPO_ABS_PATH)
        update_adr_file_content(reviewed_adr, status=STATUS_ACCEPTED)
        self.line(f"Created ADR './{reviewed_adr.relative_to(CWD)}'.")

        self.line(f"ADR repository successfully initialised at '{ADR_REPO_ABS_PATH}/'.")


class NewCommand(cleo.Command):
    """
    Create an new ADR

    new
        {words* : Words in the title}
    """

    def handle(self):
        if not ADR_REPO_ABS_PATH.exists():
            self.line_error(
                f"Directory './{ADR_REPO_REL_PATH}/' does not exist. "
                "Initialise your ADR repo first."
            )
            sys.exit(1)

        title = " ".join(self.argument("words"))
        adr_path = ADR_REPO_ABS_PATH / f"XXXX-{slugify(title)}.md"

        with adr_path.open("w") as f:
            f.write(pkg_resources.read_text(assets, "madr-template.md"))
        update_adr_file_content(adr_path, title=title, status=STATUS_PROPOSED)

        self.line(f"Created ADR './{adr_path.relative_to(CWD)}'.")


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
                "There is no ADR to approve/reject "
                "(should be of format './docs/adr/XXXX-adr-title.md')"
            )
            sys.exit(1)

        elif len(found_proposed_adrs) > 1:
            self.line_error(
                f"There should be only one ADR to approve/reject but there are "
                f"{len(found_proposed_adrs)}:"
            )
            for adr in found_proposed_adrs:
                self.line_error(f"    => './{adr.relative_to(CWD)}'")
            sys.exit(1)

        proposed_adr = found_proposed_adrs[0]
        try:
            reviewed_adr = rename_reviewed_adr_file(proposed_adr, ADR_REPO_ABS_PATH)
        except PyadrNoPreviousAdrError:
            self.line_error(
                "There should be at least one initial reviewed ADR "
                "(usually './docs/adr/0000-record-architecture-decisions.md')."
            )
            sys.exit(1)
        self.line(f"Renamed ADR to: {reviewed_adr}")

        update_adr_file_content(reviewed_adr, status=status)
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
        self.line("Markdown table of content generated in './docs/adr/index.md'")


class Application(cleo.Application):
    def __init__(self):
        super().__init__("ADR Process Tool", __version__)

        self.add(InitCommand())
        self.add(NewCommand())
        self.add(ApproveCommand())
        self.add(RejectCommand())
        self.add(GenerateTocCommand())


def main(args=None):
    return Application().run()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover

"""Console script for pyadr."""

import cleo

from pyadr.const import CWD, STATUS_ACCEPTED, STATUS_REJECTED
from pyadr.core import accept_or_reject, generate_toc, init_adr_repo, new_adr
from pyadr.exceptions import PyadrError


class InitCommand(cleo.Command):
    """
    Initialise an ADR repository

    init
        {--f|force : If set, will erase existing repository}
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
        {words* : Words in the title}
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
        {--t|toc : If set, generates also the table of content}
    """

    def handle(self):
        try:
            accept_or_reject(CWD, STATUS_ACCEPTED, self.option("toc"))
        except PyadrError:
            return 1


class RejectCommand(cleo.Command):
    """
    Reject a proposed ADR

    reject
        {--t|toc : If set, generates also the table of content}
    """

    def handle(self):
        try:
            accept_or_reject(CWD, STATUS_REJECTED, self.option("toc"))
        except PyadrError:
            return 1


class GenerateTocCommand(cleo.Command):
    """
    Generate a table of content of the ADRs

    generate-toc
    """

    def handle(self):
        try:
            generate_toc(CWD)
        except PyadrError:
            return 1

Feature: Verify ADR repo state before accepting/rejecting proposed ADR

    Background:
        Given a new working directory

    Scenario: Fail when no existing numbered ADR in repository
        Given an empty file named "docs/adr/XXXX-an-adr.md"
        When I run "pyadr accept docs/adr/XXXX-an-adr.md"
        Then it should fail with
            """
            There should be at least one initial accepted/rejected ADR (usually 'docs/adr/0000-record-architecture-decisions.md').
            """

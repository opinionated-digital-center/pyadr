Feature: Verify ADR repo state before accepting/rejecting proposed ADR

    Background:
        Given a new working directory

    Scenario: Fail when no existing numbered ADR in repository
        Given an empty file named "docs/adr/XXXX-an-adr.md"
        When I run "pyadr accept"
        Then it should fail with
            """
            There should be at least one initial reviewed ADR (usually 'docs/adr/0000-record-architecture-decisions.md').
            """

    Scenario: Fail when there is no proposed ADR in repository
        Given an empty file named "docs/adr/0000-record-architecture-decisions.md"
        When I run "pyadr accept"
        Then it should fail with
            """
            Could not find a proposed ADR (should be of format 'docs/adr/XXXX-adr-title.md')
            """

    Scenario: Fail when too many proposed ADR in repository
        Given an empty file named "docs/adr/0000-record-architecture-decisions.md"
        And an empty file named "docs/adr/XXXX-a-first-adr.md"
        And an empty file named "docs/adr/XXXX-a-second-adr.md"
        When I run "pyadr accept"
        Then it should fail with
            """
            Can handle only 1 proposed ADR but found 2:
              => 'docs/adr/XXXX-a-first-adr.md'
              => 'docs/adr/XXXX-a-second-adr.md'
            """

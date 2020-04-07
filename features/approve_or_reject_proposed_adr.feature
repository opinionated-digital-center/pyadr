Feature: Approve or reject proposed ADR

    Background:
        Given a new working directory

    Scenario: Increment ID for first accepted (same code for rejected, no need to duplicate test) ADR
        Given an empty file named "docs/adr/0000-record-architecture-decisions.md"
        Given a file named "docs/adr/XXXX-my-adr-title.md" with:
            """
            # My ADR Title

            * Status: proposed
            * Date: 2020-03-26

            ## Context and Problem Statement

            Context and problem statement.

            ## Decision Outcome

            Decision outcome.
            """
        When I run "pyadr approve"
        Then the file named "docs/adr/XXXX-my-adr-title.md" should not exist
        And the file named "docs/adr/0001-my-adr-title.md" should exist

    Scenario: Increment ID for subsequent accepted (same code for rejected, no need to duplicate test) ADR
        Given an empty file named "docs/adr/0001-a-first-adr.md"
        And a file named "docs/adr/XXXX-my-adr-title.md" with:
            """
            # My ADR Title

            * Status: proposed
            * Date: 2020-03-26

            ## Context and Problem Statement

            Context and problem statement.

            ## Decision Outcome

            Decision outcome.
            """
        When I run "pyadr approve"
        Then the file named "docs/adr/XXXX-my-adr-title.md" should not exist
        And the file named "docs/adr/0002-my-adr-title.md" should exist

    Scenario: Ensure filename corresponds to title of accepted (same code for rejected, no need to duplicate test) ADR
        Given an empty file named "docs/adr/0001-my-first-adr.md"
        And a file named "docs/adr/XXXX-my-adr-title.md" with:
            """
            # My ADR Updated Title

            * Status: proposed
            * Date: 2020-03-26

            ## Context and Problem Statement

            Context and problem statement.

            ## Decision Outcome

            Decision outcome.
            """
        When I run "pyadr approve"
        Then the file named "docs/adr/XXXX-my-adr-title.md" should not exist
        And the file named "docs/adr/0002-my-adr-updated-title.md" should exist

    Scenario: Update Status and Date for approved ADR
        Given an empty file named "docs/adr/0000-record-architecture-decisions.md"
        And a file named "docs/adr/XXXX-my-adr-title.md" with:
            """
            # My ADR Title

            * Status: proposed
            * Date: 2020-03-26

            ## Context and Problem Statement

            Context and problem statement.

            ## Decision Outcome

            Decision outcome.
            """
        When I run "pyadr approve"
        Then the file "docs/adr/0001-my-adr-title.md" should contain:
            """
            # My ADR Title

            * Status: accepted
            * Date: {__TODAY_YYYY_MM_DD__}

            ## Context and Problem Statement

            Context and problem statement.

            ## Decision Outcome

            Decision outcome.
            """

    Scenario: Update Status and Date for rejected ADR
        Given an empty file named "docs/adr/0000-record-architecture-decisions.md"
        Given a file named "docs/adr/XXXX-my-adr-title.md" with:
            """
            # My ADR Title

            * Status: proposed
            * Date: 2020-03-26

            ## Context and Problem Statement

            Context and problem statement.

            ## Decision Outcome

            Decision outcome.
            """
        When I run "pyadr reject"
        Then the file named "docs/adr/XXXX-my-adr-title.md" should not exist
        And the file named "docs/adr/0001-my-adr-title.md" should exist
        And the file "docs/adr/0001-my-adr-title.md" should contain:
            """
            # My ADR Title

            * Status: rejected
            * Date: {__TODAY_YYYY_MM_DD__}

            ## Context and Problem Statement

            Context and problem statement.

            ## Decision Outcome

            Decision outcome.
            """

    Scenario: Generate index when approving if requested
        Given an accepted adr file named "docs/adr/0000-record-architecture-decisions.md"
        Given a file named "docs/adr/XXXX-my-adr-title.md" with:
            """
            # My ADR Title

            * Status: proposed
            * Date: 2020-03-26

            ## Context and Problem Statement

            Context and problem statement.

            ## Decision Outcome

            Decision outcome.
            """
        When I run "pyadr approve --toc"
        Then it should pass with:
            """
            Markdown table of content generated in './docs/adr/index.md'
            """
        And the file named "docs/adr/index.md" should exist

    Scenario: Generate index whe rejecting if requested
        Given an accepted adr file named "docs/adr/0000-record-architecture-decisions.md"
        Given a file named "docs/adr/XXXX-my-adr-title.md" with:
            """
            # My ADR Title

            * Status: proposed
            * Date: 2020-03-26

            ## Context and Problem Statement

            Context and problem statement.

            ## Decision Outcome

            Decision outcome.
            """
        When I run "pyadr reject --toc"
        Then it should pass with:
            """
            Markdown table of content generated in './docs/adr/index.md'
            """
        And the file named "docs/adr/index.md" should exist

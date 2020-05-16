Feature: Create a new ADR

    Background:
        Given a new working directory

    Scenario: Fail when no title is given
        When I run "pyadr new"
        Then it should fail with:
            """
            Not enough arguments (missing: "words").
            """

    Scenario: Fail when no ADR repo directory
        When I run "pyadr new My ADR Title"
        Then it should fail with:
            """
            Directory 'docs/adr/' does not exist. Initialise your ADR repo first.
            """

    Scenario: Create a new ADR and succeed with a success message
        Given a directory named "docs/adr/"
        When I run "pyadr new My ADR Title"
        Then it should pass with:
            """
            Created ADR 'docs/adr/XXXX-my-adr-title.md'.
            """
        And the file named "docs/adr/XXXX-my-adr-title.md" should exist
        And the file "docs/adr/XXXX-my-adr-title.md" should contain:
            """
            # My ADR Title

            * Status: proposed
            """
        And the file "docs/adr/XXXX-my-adr-title.md" should contain:
            """
            * Date: {__TODAY_YYYY_MM_DD__}

            """

    Scenario: Propose a new ADR (same as create, different command name)
        Given a directory named "docs/adr/"
        When I run "pyadr propose My ADR Title"
        Then it should pass
        And the file named "docs/adr/XXXX-my-adr-title.md" should exist

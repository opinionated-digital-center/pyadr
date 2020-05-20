Feature: Commit adrs

    Background:
        Given a new working directory
        And an initialised git adr repo

    Scenario: Commit proposed ADR: Passing for proposed ADRs
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr commit docs/adr/XXXX-my-adr-title.md"
        Then it should pass with
            """
            Committing ADR 'docs/adr/XXXX-my-adr-title.md'...
            Committed ADR 'docs/adr/XXXX-my-adr-title.md' with message 'docs(adr): [proposed] XXXX-my-adr-title'.
            """
        And the file "docs/adr/XXXX-my-adr-title.md" should be committed in the last commit
        And the head commit message should be
            """
            docs(adr): [proposed] XXXX-my-adr-title
            """

    Scenario: Commit proposed ADR: Passing for accepted ADRs
        Given an accepted adr file named "docs/adr/0002-my-adr-title.md"
        And I stage the file "docs/adr/0002-my-adr-title.md"
        When I run "git adr commit docs/adr/0002-my-adr-title.md"
        Then it should pass
        And the file "docs/adr/0002-my-adr-title.md" should be committed in the last commit
        And the head commit message should be
            """
            docs(adr): [accepted] 0002-my-adr-title
            """

    Scenario: Commit proposed ADR: Fail if not previously staged
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr commit docs/adr/XXXX-my-adr-title.md"
        Then it should fail with
            """
            ADR 'docs/adr/XXXX-my-adr-title.md' should be staged first.
            """

Feature: Commit adrs

    Background:
        Given a new working directory

    Scenario: Commit proposed ADR in standard repo
        Given an initialised git adr repo
        And a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr commit docs/adr/XXXX-my-adr-title.md"
        Then it should pass
        And the file "docs/adr/XXXX-my-adr-title.md" should be committed in the last commit
        And the head commit message should be
            """
            chore(adr): [proposed] XXXX-my-adr-title
            """

    Scenario: Commit proposed ADR in adr only repo
        Given an initialised git adr only repo
        And a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr commit docs/adr/XXXX-my-adr-title.md"
        Then it should pass
        And the file "docs/adr/XXXX-my-adr-title.md" should be committed in the last commit
        And the head commit message should be
            """
            chore(adr): [proposed] XXXX-my-adr-title
            """

    Scenario: Commit accepted ADR in standard repo
        Given an initialised git adr repo
        And an accepted adr file named "docs/adr/0002-my-adr-title.md"
        And I stage the file "docs/adr/0002-my-adr-title.md"
        When I run "git adr commit docs/adr/0002-my-adr-title.md"
        Then it should pass
        And the file "docs/adr/0002-my-adr-title.md" should be committed in the last commit
        And the head commit message should be
            """
            docs(adr): [accepted] 0002-my-adr-title
            """

    Scenario: Commit accepted ADR in adr only repo
        Given an initialised git adr only repo
        And an accepted adr file named "docs/adr/0002-my-adr-title.md"
        And I stage the file "docs/adr/0002-my-adr-title.md"
        When I run "git adr commit docs/adr/0002-my-adr-title.md"
        Then it should pass
        And the file "docs/adr/0002-my-adr-title.md" should be committed in the last commit
        And the head commit message should be
            """
            feat(adr): [accepted] 0002-my-adr-title
            """

    Scenario: Commit ADR command output
        Given an initialised git adr repo
        And a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr commit docs/adr/XXXX-my-adr-title.md"
        Then the command output should contain
            """
            Committing ADR 'docs/adr/XXXX-my-adr-title.md'...
            Committed ADR 'docs/adr/XXXX-my-adr-title.md' with message 'chore(adr): [proposed] XXXX-my-adr-title'.
            """

    Scenario: Commit proposed ADR: Fail if not previously staged
        Given an initialised git adr repo
        And a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr commit docs/adr/XXXX-my-adr-title.md"
        Then it should fail with
            """
            ADR 'docs/adr/XXXX-my-adr-title.md' should be staged first.
            """

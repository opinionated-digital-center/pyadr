Feature: Helper for the various names and messages - Git included - adr only repo

    Background:
        Given a new working directory
        And an initialised git adr only repo

    Scenario: Commit message for ADR only repos starts with 'feat(adr)'
        Given a proposed adr file named "XXXX-my-adr-title.md"
        When I run "git adr helper commit-message XXXX-my-adr-title.md"
        Then it should pass with
            """
            chore(adr): [proposed] XXXX-my-adr-title
            """

    Scenario: Return commit message for other than proposed adr in an adr only repo
        Given an accepted adr file named "0002-my-adr-title.md"
        When I run "git adr helper commit-message 0002-my-adr-title.md"
        Then it should pass with
            """
            feat(adr): [accepted] 0002-my-adr-title
            """

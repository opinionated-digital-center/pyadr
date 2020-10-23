Feature: Helper for the various names and messages - Git included - project repo

    Background:
        Given a new working directory
        And an initialised git adr repo

    Scenario: Return commit message for proposed adr
        Given a proposed adr file named "XXXX-my-adr-title.md"
        When I run "git adr helper commit-message XXXX-my-adr-title.md"
        Then it should pass with
            """
            chore(adr): [proposed] XXXX-my-adr-title
            """

    Scenario: Return commit message for other than proposed adr
        Given an accepted adr file named "0002-my-adr-title.md"
        When I run "git adr helper commit-message 0002-my-adr-title.md"
        Then it should pass with
            """
            docs(adr): [accepted] 0002-my-adr-title
            """

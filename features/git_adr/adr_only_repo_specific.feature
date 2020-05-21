Feature: ADR only repo specific tests

    Scenario: Commit message for ADR only repos starts with 'feat(adr)'
        Given a new working directory
        And an initialised git adr only repo
        Given a proposed adr file named "XXXX-my-adr-title.md"
        When I run "git adr helper commit-message XXXX-my-adr-title.md"
        Then it should pass with
            """
            feat(adr): [proposed] XXXX-my-adr-title
            """

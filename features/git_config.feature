Feature: Configure Git ADR cli - Git specific

    Background:
        Given a new working directory

    Scenario: Valid config settings
        When I run "git adr config --list"
        Then it should pass with
            """
            adr-only-repo = false
            records-dir = docs/adr
            """

    Scenario: Get  config setting value
        When I run "git adr config adr-only-repo"
        Then it should pass

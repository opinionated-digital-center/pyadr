Feature: Configure Git ADR cli
    Shared features with pyadr. Only a minimum is retested, as much code base is the same.

    Background:
        Given a new working directory

    @wip
    Scenario: List config items
        When I run "git adr config --list"
        Then it should pass with
            """
            records-dir = docs/adr
            """

    @wip
    Scenario: Get config item value
        When I run "git adr config records-dir"
        Then it should pass

    @wip
    Scenario: Read config file
        Given a file named ".adr" with
            """
            [adr]
            records-dir = another_dir
            """
        When I run "git adr config records-dir"
        Then it should pass with
            """
            records-dir = another_dir
            """

    @wip
    Scenario: Set config item: ADR directory
        When I run "git adr config records-dir another_dir"
        Then it should pass
        And a file named ".adr" should exist

    @wip
    Scenario: Unset config items
        Given a file named ".adr" with
            """
            [adr]
            records-dir = another_dir
            """
        When I run "git adr config records-dir --unset"
        Then it should pass
        And the file ".adr" should not contain
            """
            records-dir = another_dir
            """

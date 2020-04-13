Feature: Configure ADR cli

    Background:
        Given a new working directory

    @wip
    Scenario: List config items
        When I run "pyadr config --list"
        Then it should pass with
            """
            records-dir = docs/adr
            """

    @wip
    Scenario: Get config item value
        When I run "pyadr config records-dir"
        Then it should pass with
            """
            records-dir = docs/adr
            """

    @wip
    Scenario: Read config file
        Given a file named ".adr" with
            """
            [adr]
            records-dir = another_dir
            """
        When I run "pyadr config records-dir"
        Then it should pass with
            """
            records-dir = another_dir
            """

    @wip
    Scenario: Write to config file when setting config item
        Given the file named ".adr" does not exist
        When I run "pyadr config records-dir another_dir"
        Then it should pass
        And a file named ".adr" should exist
        And the file ".adr" should contain
            """
            [adr]
            records-dir = another_dir
            """

    @wip
    Scenario: Set config item: ADR directory
        When I run "pyadr config records-dir another_dir"
        Then it should pass with
            """
            Configured 'records-dir' to 'another_dir'
            """
        And a file named ".adr" should exist
        And the file ".adr" should contain
            """
            [adr]
            records-dir = another_dir
            """

    @wip
    Scenario: Unset config items
        Given a file named ".adr" with
            """
            [adr]
            records-dir = another_dir
            """
        When I run "pyadr config records-dir --unset"
        Then it should pass with
            """
            Config item 'records-dir' unset.
            """
        And the file ".adr" should not contain
            """
            records-dir = another_dir
            """

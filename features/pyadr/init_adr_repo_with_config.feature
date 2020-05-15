Feature: Initialise an ADR repository

    Background:
        Given a new working directory

    Scenario: Fail when a repo already exists - records-dir config option set
        Given a file named ".adr" with
            """
            [adr]
            records-dir = another_adr_dir
            """
        And a directory named "another_adr_dir"
        When I run "pyadr init"
        Then it should fail

    Scenario: Create the repo directory - records-dir config option set
        Given a file named ".adr" with
            """
            [adr]
            records-dir = another_adr_dir
            """
        When I run "pyadr init"
        Then it should pass
        And the directory "another_adr_dir" exists
        And the file named "another_adr_dir/template.md" should exist
        And the file named "another_adr_dir/0000-record-architecture-decisions.md" should exist
        And the file named "another_adr_dir/0001-use-markdown-architectural-decision-records.md" should exist

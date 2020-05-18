Feature: Check ADRs well formed

    Background:
        Given a new working directory

    Scenario: Check all ADR file names are slugs of the ADR title
        Given a file named "docs/adr/0002-an-adr.md" with:
            """
            # A different ADR Title

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/0003-another-adr.md" with:
            """
            # Yet another different ADR title

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/0004-a-last-adr.md" with:
            """
            # A last ADR

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        When I run "pyadr check-adr-repo"
        Then it should fail with:
            """
            Filename of ADR(s) processed (status '<any status with an id>') must be at least of format '[0-9][0-9][0-9][0-9]-<adr-title-in-slug-format>.md', but:
              => 'docs/adr/0002-an-adr.md' does not have the correct title slug ('a-different-adr-title').
              => 'docs/adr/0003-another-adr.md' does not have the correct title slug ('yet-another-different-adr-title').
            """

    Scenario: Check all ADR file names have '[0-9][0-9][0-9][0-9]' followed by '-'
        Given a file named "docs/adr/XXXX-an-adr.md" with:
            """
            # An ADR

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/000X-another-adr.md" with:
            """
            # Another ADR

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/000-yet-another-adr.md" with:
            """
            # Yet another ADR

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/00023-a-last-adr.md" with:
            """
            # A last ADR

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        When I run "pyadr check-adr-repo"
        Then it should fail with:
            """
            Filename of ADR(s) processed (status '<any status with an id>') must be at least of format '[0-9][0-9][0-9][0-9]-<adr-title-in-slug-format>.md', but:
              => 'docs/adr/000-yet-another-adr.md' does not start with '[0-9][0-9][0-9][0-9]' followed by '-'.
              => 'docs/adr/00023-a-last-adr.md' does not start with '[0-9][0-9][0-9][0-9]' followed by '-'.
              => 'docs/adr/000X-another-adr.md' does not start with '[0-9][0-9][0-9][0-9]' followed by '-'.
              => 'docs/adr/XXXX-an-adr.md' does not start with '[0-9][0-9][0-9][0-9]' followed by '-'.
            """

    Scenario: Check all ADR files have a unique number
        Given a file named "docs/adr/0002-an-adr.md" with:
            """
            # An ADR

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/0002-another-adr.md" with:
            """
            # Another ADR

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/0002-a-last-adr.md" with:
            """
            # A last ADR

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/0003-more-adr.md" with:
            """
            # More ADR

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/0003-yet-more-adr.md" with:
            """
            # Yet more ADR

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        When I run "pyadr check-adr-repo"
        Then it should fail with:
            """
            ADR files must have a unique number, but the following files have the same number:
              => ['docs/adr/0002-a-last-adr.md', 'docs/adr/0002-an-adr.md', 'docs/adr/0002-another-adr.md'].
              => ['docs/adr/0003-more-adr.md', 'docs/adr/0003-yet-more-adr.md'].
            """

    Scenario: Check all ADR files have a title followed by a status and a date
        Given a file named "docs/adr/0002-an-adr.md" with:
            """
            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        When I run "pyadr check-adr-repo"
        Then it should fail with
            """
            ADR must be of format:
            >>>>>
            # Title

            * Status: a_status
            [..]
            * Date: YYYY-MM-DD
            [..]
            <<<<<
            but the following files where not:
              => 'docs/adr/0002-an-adr.md'.
            """

    Scenario: Pass checks when all conditions are filled
        Given a file named "docs/adr/0002-an-adr.md" with:
            """
            # An ADR

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/0003-another-adr.md" with:
            """
            # Another ADR

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/0004-yet-another-adr.md" with:
            """
            # Yet Another ADR

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/0005-a-last-adr.md" with:
            """
            # A last ADR

            * Status: proposed
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        When I run "pyadr check-adr-repo"
        Then it should pass with
            """
            All checks passed.
            """

    Scenario: `no-proposed` option - Check all ADR files have a status other than 'proposed'
        Given a file named "docs/adr/0002-an-adr.md" with:
            """
            # An ADR

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/0003-another-adr.md" with:
            """
            # Another ADR

            * Status: proposed
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        When I run "pyadr check-adr-repo --no-proposed"
        Then it should fail with:
            """
            ADR files must not have their status set to 'proposed', but the following files do:
              => 'docs/adr/0003-another-adr.md'.
            """

Feature: Helper for the various names and messages

    Background:
        Given a new working directory

    Scenario: Fail when adr format incorrect
        # We won't test all formatting errors here as they are already tested in
        # unit tests.
        Given an empty file named "foo-bar-file"
        When I run "pyadr helper slug foo-bar-file"
        Then it should fail with:
            """
            [PyadrAdrTitleNotFoundError]
            """

    Scenario: Return title slug
        Given an accepted adr file named "0001-my-adr-title.md"
        When I run "pyadr helper slug 0001-my-adr-title.md"
        Then it should pass with
            """
            my-adr-title
            """

    Scenario: Return title in lowercase
        Given an accepted adr file named "0001-my-adr-title.md"
        When I run "pyadr helper lowercase 0001-my-adr-title.md"
        Then it should pass with
            """
            my adr title
            """

    Scenario: Resync ADR filename with its title
        Given a file named "0001-my-adr-title.md" with:
            """
            # My ADR Updated Title

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            Context and problem statement.

            ## Decision Outcome

            Decision outcome.
            """
        When I run "pyadr helper resync-filename 0001-my-adr-title.md"
        Then it should pass with
            """
            File renamed to '0001-my-adr-updated-title.md'.
            """
        And the file named "0001-my-adr-title.md" should not exist
        And the file named "0001-my-adr-updated-title.md" should exist

    Scenario: Fail before resync filename if initial filename format not suitable
        Given a file named "001-my-adr-title.md" with:
            """
            # My ADR Title

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement
            [..]
            """
        When I run "pyadr helper resync-filename 001-my-adr-title.md"
        Then it should fail with
            """
            [PyadrAdrFilenameFormatError]
            001-my-adr-title.md

            Filename of ADR(s) processed (status 'accepted') must be at least of format '[0-9][0-9][0-9][0-9]-*.md'.
            """

    Scenario: No resync if filename already correct
        Given an accepted adr file named "0001-my-adr-title.md"
        When I run "pyadr helper resync-filename 0001-my-adr-title.md"
        Then it should pass with
            """
            File name already up-to-date.
            """

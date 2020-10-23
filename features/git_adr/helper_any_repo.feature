Feature: Helper for the various names and messages - Git included - Any repo type
    Since 'git adr' makes calls to 'pyadr', some features will be already fully
    tested in the bdd tests for 'pyadr'.

    Background:
        Given a new working directory
        And an initialised git adr repo

    Scenario: Sync ADR filename with its title - untracked files
        Given a file named "0002-my-adr-title.md" with:
            """
            # My ADR Updated Title

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            Context and problem statement.

            ## Decision Outcome

            Decision outcome.
            """
        When I run "git adr helper sync-filename 0002-my-adr-title.md"
        Then it should pass
        And the file named "0002-my-adr-title.md" should not exist
        And the file named "0002-my-adr-updated-title.md" should exist
        And the file "0002-my-adr-updated-title.md" should be staged

    Scenario: Sync ADR filename with its title - staged file
        Given a file named "0002-my-adr-title.md" with:
            """
            # My ADR Updated Title

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            Context and problem statement.

            ## Decision Outcome

            Decision outcome.
            """
        And I stage the file "0002-my-adr-title.md"
        When I run "git adr helper sync-filename 0002-my-adr-title.md"
        Then it should pass
        And the file named "0002-my-adr-title.md" should not exist
        And the file named "0002-my-adr-updated-title.md" should exist
        And the file "0002-my-adr-updated-title.md" should be staged

    Scenario: Sync ADR filename with its title - committed file
        Given a file named "0002-my-adr-title.md" with:
            """
            # My ADR Updated Title

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            Context and problem statement.

            ## Decision Outcome

            Decision outcome.
            """
        And I stage the file "0002-my-adr-title.md"
        And I commit the staged files with message "foo bar"
        When I run "git adr helper sync-filename 0002-my-adr-title.md"
        Then it should pass
        And the file named "0002-my-adr-title.md" should not exist
        And the file named "0002-my-adr-updated-title.md" should exist
        And the file "0002-my-adr-updated-title.md" should be staged

    Scenario: No sync if filename already correct
        Given an accepted adr file named "0002-my-adr-title.md"
        When I run "git adr helper sync-filename 0002-my-adr-title.md"
        Then it should pass
        And the file "0002-my-adr-title.md" should not be staged

    Scenario: Return commit message fail on wrong filename format
        Given a proposed adr file named "XXXXX-my-adr-title.md"
        When I run "git adr helper commit-message XXXXX-my-adr-title.md"
        Then it should fail with
            """
              PyadrAdrFilenameIncorrectError
              XXXXX-my-adr-title.md
            """
        And the command output should contain
            """
            (status to verify against: 'proposed')
            ADR(s)'s filename follow the format 'XXXX-<adr-title-in-slug-format>.md', but:
              => 'XXXXX-my-adr-title.md' does not start with 'XXXX-'.
            """

    Scenario: Return commit message fail on unsynched filename title
        Given a file named "XXXX-my-adr-title.md" with:
            """
            # My ADR Updated Title

            * Status: proposed
            * Date: 2020-03-26

            ## Context and Problem Statement
            [..]
            """
        When I run "git adr helper commit-message XXXX-my-adr-title.md"
        Then it should fail with
            """
              PyadrAdrFilenameIncorrectError
              XXXX-my-adr-title.md
            """
        And the command output should contain
            """
            (status to verify against: 'proposed')
            ADR(s)'s filename follow the format 'XXXX-<adr-title-in-slug-format>.md', but:
              => 'XXXX-my-adr-title.md' does not have the correct title slug ('my-adr-updated-title').
            """

    Scenario: Return branch title
        Given a proposed adr file named "XXXX-my-adr-title.md"
        When I run "git adr helper branch-title XXXX-my-adr-title.md"
        Then it should pass with
            """
            propose-my-adr-title
            """

    Scenario: Return branch title fail on unsynched filename title
        Given a file named "XXXX-my-adr-title.md" with:
            """
            # My ADR Updated Title

            * Status: proposed
            * Date: 2020-03-26

            ## Context and Problem Statement
            [..]
            """
        When I run "git adr helper branch-title XXXX-my-adr-title.md"
        Then it should fail with
            """
              PyadrAdrFilenameIncorrectError
            """
    Scenario: Fail on branch option if ADR status not valid (propose, deprecate, supersede)
        Given an accepted adr file named "0001-my-adr-title.md"
        When I run "git adr helper branch-title 0001-my-adr-title.md"
        Then it should fail with
            """
              PyadrStatusIncompatibleWithReviewRequestError
              ADR: '0001-my-adr-title.md'; status: 'accepted'.
            """
        And the command output should contain
            """
            Can only create review request branches for ADR statuses: ['proposed', 'deprecated', 'superseding'].
            """


# TODO
#    Scenario: Fail on commit message option for superseding if no superseded file given
#
#    Scenario: Fail on commit message option if ADR status not valid
#

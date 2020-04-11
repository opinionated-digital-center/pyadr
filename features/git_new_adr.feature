Feature: Create a new ADR - Git included
    Since 'git adr' makes calls to 'pyadr', some features will be already fully
    tested in the bdd tests for 'pyadr'.

    Background:
        Given a new working directory

    Scenario: Fail when no ADR repo directory
        When I run "git adr new My ADR Title"
        Then it should fail with:
            """
            No Git repository found in directory '{__WORKDIR__}/'. Please initialise a Git repository before running command.
            """

    Scenario: Fail when no title is given
        When I run "git adr new"
        Then it should fail with:
            """
            Not enough arguments (missing: "words").
            """

    Scenario: Fail when no master branch
        Given an empty git repo
        And a directory named "docs/adr/"
        When I run "git adr new My ADR Title"
        Then it should fail with:
            """
            Verifying branch 'master' exists...
            ... branch 'master' does not exist. Correct before running command.
            """

    Scenario: Create a new ADR
        Given an initialised git adr repo
        When I run "git adr new My ADR Title"
        Then it should pass
        And the file named "docs/adr/XXXX-my-adr-title.md" should exist

    Scenario: Create feature branch and commit new ADR file
        Given an initialised git adr repo
        When I run "git adr new My ADR Title"
        Then it should pass with
            """
            Files committed to branch 'adr-my-adr-title' with commit message
            """
        And the branch "adr-my-adr-title" should exist
        And the head should be at branch "adr-my-adr-title"
        And there should be 1 commit between head and the branch "master"
        And the file "docs/adr/XXXX-my-adr-title.md" should have been committed in the last commit

    Scenario: Fail when index dirty
        Given an initialised git adr repo
        And a file named "foo" with
            """
            bar
            """
        And I add the file "foo" to the git index
        When I run "git adr new My ADR Title"
        Then it should fail with
            """
            Verifying Git index is empty...
            ... files staged in Git index. Clean before running command.
            """

    Scenario: Fail when feature branch already exists
        Given an initialised git adr repo
        And I create the branch "adr-my-adr-title"
        When I run "git adr new My ADR Title"
        Then it should fail with
            """
            Verifying branch 'adr-my-adr-title' does not exist...
            ... branch 'adr-my-adr-title' already exists. Clean before running command.
            """

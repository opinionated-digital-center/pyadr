Feature: Initialise a git ADR repository
    Since 'git adr' makes calls to 'pyadr', some features will be already fully
    tested in the bdd tests for 'pyadr'.

    Background:
        Given a new working directory

    Scenario: Fail when an ADR repo directory already exists
        Given a directory named "docs/adr"
        When I run "git adr init"
        Then it should fail

    Scenario: Fail when a git repo has not been initialised
        When I run "git adr init"
        Then it should fail with:
            """
            No Git repository found in directory '{__WORKDIR__}/'. Please initialise a Git repository before running command.
            """

    Scenario: Create and commit initial ADR files on empty git repo
        Given an empty git repo
        When I run "git adr init"
        Then it should pass with
            """
            Files committed to branch 'master' with commit message
            """
        And the command output should contain
            """
            Git repo empty. Will commit files to 'master'.
            """
        And there should be 1 commit in "master"
        And the head commit message should be
            """
            docs(adr): initialise adr repository
            """
        And 3 files should have been committed in the last commit
        And the file "docs/adr/template.md" should have been committed in the last commit
        And the file "docs/adr/0000-record-architecture-decisions.md" should have been committed in the last commit
        And the file "docs/adr/0001-use-markdown-architectural-decision-records.md" should have been committed in the last commit

    Scenario: Initialise for ADR only repo
        Given an empty git repo
        When I run "git adr init --adr-only-repo"
        Then it should pass
        And the head commit message should be
            """
            feat(adr): initialise adr repository
            """

    Scenario: Create and commit initial ADR files on a non-empty git repo
        Given a starting git repo
        When I run "git adr init"
        Then it should pass with
            """
            Files committed to branch 'adr-init-repo' with commit message
            """
        And the branch "adr-init-repo" should exist
        And the head should be at branch "adr-init-repo"
        And there should be 1 commit between head and the branch "master"

    Scenario: Fail when index dirty
        Given a starting git repo
        And a file named "foo" with
            """
            bar
            """
        And I add the file "foo" to the git index
        When I run "git adr init"
        Then it should fail with
            """
            Verifying Git index is empty...
            ... files staged in Git index. Clean before running command.
            """

    Scenario: Fail when init branch exists
        Given an empty git repo
        And a file named "foo" with
            """
            bar
            """
        And I add the file "foo" to the git index
        And I commit the git index with message "foo bar"
        And I create the branch "adr-init-repo"
        When I run "git adr init"
        Then it should fail with
            """
            Verifying branch 'adr-init-repo' does not exist...
            ... branch 'adr-init-repo' already exists. Clean before running command.
            """

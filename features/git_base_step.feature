Feature: Git steps reused throughout the features

    Scenario: Create a starting repo
        Given a starting git repo
        Then a git repo should exist
        And the file named "initial_commit_file" should exist
        And the file "initial_commit_file" should contain
            """
            foo bar
            """
        And the head commit message should be
            """
            chore: initial commit
            """
        And 1 files should have been committed in the last commit
        And the file "initial_commit_file" should have been committed in the last commit

    Scenario: Create a starting repo
        Given an initialised git adr repo
        Then a git repo should exist
        And the directory "docs/adr" should exist
        And 3 files should have been committed in the last commit
        And the file "docs/adr/template.md" should have been committed in the last commit
        And the file "docs/adr/0000-record-architecture-decisions.md" should have been committed in the last commit
        And the file "docs/adr/0001-use-markdown-architectural-decision-records.md" should have been committed in the last commit

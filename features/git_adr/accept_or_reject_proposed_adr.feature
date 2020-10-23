Feature: Accept or reject proposed ADR - Git included

    Background:
        Given a new working directory
        And an initialised git adr repo

    Scenario: The proposed ADR should be already staged or committed
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr accept docs/adr/XXXX-my-adr-title.md"
        Then it should fail
        And the command output should contain
            """
              PyadrGitAdrNotStagedOrCommittedError
              docs/adr/XXXX-my-adr-title.md
            """
        And the command output should contain
            """
            ADR 'docs/adr/XXXX-my-adr-title.md' should be staged or committed first.
            """

    Scenario: Accepting should pass when the proposed ADR is staged (code shared with rejected => no need to duplicate test)
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr accept docs/adr/XXXX-my-adr-title.md"
        Then it should pass

    Scenario: Accepting should pass when the proposed ADR is committed (code shared with rejected => no need to duplicate test)
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        And I commit the staged files with message "foo bar"
        When I run "git adr accept docs/adr/XXXX-my-adr-title.md"
        Then it should pass

    Scenario: An incremented ID number should be assigned to the accepted ADR (code shared with rejected => no need to duplicate test)
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr accept docs/adr/XXXX-my-adr-title.md"
        Then it should pass
        And the file named "docs/adr/XXXX-my-adr-title.md" should not exist
        And the file named "docs/adr/0002-my-adr-title.md" should exist

    Scenario: The accepted ADR's filename should correspond to title of the ADR (code shared with rejected => no need to duplicate test)
        Given a file named "docs/adr/XXXX-my-adr-title.md" with:
            """
            # My Adr Updated Title

            * Status: proposed
            * Date: 2020-03-26

            ## Context and Problem Statement

            Context and problem statement.

            ## Decision Outcome

            Decision outcome.
            """
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr accept docs/adr/XXXX-my-adr-title.md"
        Then it should pass
        And the file named "docs/adr/XXXX-my-adr-title.md" should not exist
        And the file named "docs/adr/0002-my-adr-updated-title.md" should exist

    Scenario: The renaming of the ADR file should be traced by git (code shared with rejected => no need to duplicate test)
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        And I commit the staged files with message "dummy message"
        When I run "git adr accept docs/adr/XXXX-my-adr-title.md"
        Then it should pass
        And the file "docs/adr/0002-my-adr-title.md" should be staged as renamed

    Scenario: Accepted ADR's Status and Date should be updated
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr accept docs/adr/XXXX-my-adr-title.md"
        Then it should pass
        And the file "docs/adr/0002-my-adr-title.md" should contain:
            """
            # My Adr Title

            * Status: accepted
            * Date: {__TODAY_YYYY_MM_DD__}

            ## Context and Problem Statement

            Context and problem statement.

            ## Decision Outcome

            Decision outcome.
            """

    Scenario: Rejected ADR's Status and Date should be updated
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr reject docs/adr/XXXX-my-adr-title.md"
        Then it should pass
        And the file named "docs/adr/XXXX-my-adr-title.md" should not exist
        And the file named "docs/adr/0002-my-adr-title.md" should exist
        And the file "docs/adr/0002-my-adr-title.md" should contain:
            """
            # My Adr Title

            * Status: rejected
            * Date: {__TODAY_YYYY_MM_DD__}

            ## Context and Problem Statement

            Context and problem statement.

            ## Decision Outcome

            Decision outcome.
            """

#    Scenario: All changes to accepted ADR should be staged (code shared with rejected => no need to duplicate test)
#        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
#        And I stage the file "docs/adr/XXXX-my-adr-title.md"
#        When I run "git adr accept docs/adr/XXXX-my-adr-title.md"
#        Then it should pass
#        And the file "docs/adr/0002-my-adr-title.md" should be staged
#        And the file "docs/adr/0002-my-adr-title.md" should NOT be marked in the git working tree as modified

    Scenario: Optionnaly, one should be able to re-generate the index upon acceptance
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr accept docs/adr/XXXX-my-adr-title.md --toc"
        Then it should pass with:
            """
            Markdown table of content generated in 'docs/adr/index.md'
            """
        And the file named "docs/adr/index.md" should exist
        And the file "docs/adr/index.md" should be staged

    Scenario: Optionnaly, one should be able to re-generate the index upon rejection
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr reject docs/adr/XXXX-my-adr-title.md --toc"
        Then it should pass with:
            """
            Markdown table of content generated in 'docs/adr/index.md'
            """
        And the file named "docs/adr/index.md" should exist
        And the file "docs/adr/index.md" should be staged

    Scenario: Optionnaly, one should be able to commit the ADR upon acceptance
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr accept docs/adr/XXXX-my-adr-title.md --commit"
        Then it should pass
        And the file "docs/adr/0002-my-adr-title.md" should be committed in the last commit
        And the head commit message should be
            """
            docs(adr): [accepted] 0002-my-adr-title
            """

    Scenario: Optionnaly, one should be able to commit the ADR upon rejection
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr reject docs/adr/XXXX-my-adr-title.md --commit"
        Then it should pass
        And the file "docs/adr/0002-my-adr-title.md" should be committed in the last commit
        And the head commit message should be
            """
            docs(adr): [rejected] 0002-my-adr-title
            """

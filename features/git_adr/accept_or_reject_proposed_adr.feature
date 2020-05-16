Feature: Accept or reject proposed ADR - Git included

    Background:
        Given a new working directory

    Scenario: Fail if the proposed ADR is not staged or committed
        Given an initialised git adr repo
        And a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr accept"
        Then it should fail
        And the command output should contain
            """
            [PyadrGitAdrNotStagedOrCommittedError]
            docs/adr/XXXX-my-adr-title.md
            """
        And the command output should contain
            """
            File docs/adr/XXXX-my-adr-title.md should be staged or committed first.
            """

    Scenario: Pass if the proposed ADR is staged
        Given an initialised git adr repo
        And a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr accept"
        Then it should pass

    Scenario: Pass if the proposed ADR is committed
        Given an initialised git adr repo
        And a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        And I commit the staged files with message "foo bar"
        When I run "git adr accept"
        Then it should pass

    Scenario: Increment ID of accepted ADR (same code for rejected, no need to duplicate test)
        Given an initialised git adr repo
        And a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr accept"
        Then it should pass
        And the file named "docs/adr/XXXX-my-adr-title.md" should not exist
        And the file named "docs/adr/0002-my-adr-title.md" should exist

    Scenario: Ensure filename corresponds to title of accepted ADR (same code for rejected, no need to duplicate test)
        Given an initialised git adr repo
        And a file named "docs/adr/XXXX-my-adr-title.md" with:
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
        When I run "git adr accept"
        Then it should pass
        And the file named "docs/adr/XXXX-my-adr-title.md" should not exist
        And the file named "docs/adr/0002-my-adr-updated-title.md" should exist

    Scenario: Ensure git traced filename change of accepted ADR (same code for rejected, no need to duplicate test)
        Given an initialised git adr repo
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr accept"
        Then it should pass
        And the file "docs/adr/0002-my-adr-title.md" should be staged

    Scenario: Update Status and Date for accepted ADR
        Given an initialised git adr repo
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr accept"
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

    Scenario: Update Status and Date for rejected ADR
        Given an initialised git adr repo
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr reject"
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

    Scenario: Generate index when approving if requested and add it to index
        Given an initialised git adr repo
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr accept --toc"
        Then it should pass with:
            """
            Markdown table of content generated in 'docs/adr/index.md'
            """
        And the file named "docs/adr/index.md" should exist
        And the file "docs/adr/index.md" should be staged

    Scenario: Generate index when rejecting if requested and add it to index
        Given an initialised git adr repo
        Given a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr reject --toc"
        Then it should pass with:
            """
            Markdown table of content generated in 'docs/adr/index.md'
            """
        And the file named "docs/adr/index.md" should exist
        And the file "docs/adr/index.md" should be staged

    Scenario: Commit files on `accept --commit` option
        Given an initialised git adr repo
        And a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr accept --commit"
        Then it should pass
        And the file "docs/adr/0002-my-adr-title.md" should be committed in the last commit
        And the head commit message should be
            """
            docs(adr): [accepted] 0002-my-adr-title
            """

    Scenario: Commit files on `reject --commit` option
        Given an initialised git adr repo
        And a proposed adr file named "docs/adr/XXXX-my-adr-title.md"
        And I stage the file "docs/adr/XXXX-my-adr-title.md"
        When I run "git adr reject --commit"
        Then it should pass
        And the file "docs/adr/0002-my-adr-title.md" should be committed in the last commit
        And the head commit message should be
            """
            docs(adr): [rejected] 0002-my-adr-title
            """

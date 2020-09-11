Feature: Generate a table of content in markdown

    Scenario: Generate a table of content in markdown - all statuses have adr
        Given a new working directory
        And a file named "docs/adr/0001-an-accepted-adr.md" with:
            """
            # An accepted ADR

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/0002-a-rejected-adr.md" with:
            """
            # A rejected ADR

            * Status: rejected
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/0003-a-superseded-adr.md" with:
            """
            # A superseded ADR

            * Status: superseded by [ADR-0001](0001-an-accepted-adr.md)
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/0004-a-deprecated-adr.md" with:
            """
            # A deprecated ADR

            * Status: deprecated
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/0005-an-adr-with-a-non-standard-status.md" with:
            """
            # An ADR with a non-standard status

            * Status: foo
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        When I run "pyadr toc"
        Then it should pass with:
            """
            Markdown table of content generated in 'docs/adr/index.md'
            """
        And the file "docs/adr/index.md" should contain:
            """
            # Architecture Decision Records

            ## Accepted Records

            * [0001 - An accepted ADR](0001-an-accepted-adr.md)

            ## Rejected Records

            * [0002 - A rejected ADR](0002-a-rejected-adr.md)

            ## Superseded Records

            * [0003 - A superseded ADR](0003-a-superseded-adr.md): superseded by [ADR-0001](0001-an-accepted-adr.md)

            ## Deprecated Records

            * [0004 - A deprecated ADR](0004-a-deprecated-adr.md)

            ## Records with non-standard statuses

            ### Status `foo`

            * [0005 - An ADR with a non-standard status](0005-an-adr-with-a-non-standard-status.md)
            """

    Scenario: Generate a table of content in markdown - some statuses don't have adr
        Given a new working directory
        And a file named "docs/adr/0001-an-adr.md" with:
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
        When I run "pyadr toc"
        Then it should pass
        And the file named "docs/adr/index.md" should exist
        And the file "docs/adr/index.md" should contain:
            """
            # Architecture Decision Records

            ## Accepted Records

            * [0001 - An ADR](0001-an-adr.md)
            * [0002 - Another ADR](0002-another-adr.md)

            ## Rejected Records

            * None

            ## Superseded Records

            * None

            ## Deprecated Records

            * None

            ## Records with non-standard statuses

            * None
            """

    Scenario: Do not include proposed ADRs in table of content
        Given a new working directory
        And a file named "docs/adr/0001-an-adr.md" with:
            """
            # An ADR

            * Status: accepted
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        And a file named "docs/adr/XXXX-another-adr.md" with:
            """
            # Another ADR

            * Status: proposed
            * Date: 2020-03-26

            ## Context and Problem Statement

            [..]
            """
        When I run "pyadr toc"
        Then it should pass
        And the file named "docs/adr/index.md" should exist
        And the file "docs/adr/index.md" should contain:
            """
            # Architecture Decision Records

            ## Accepted Records

            * [0001 - An ADR](0001-an-adr.md)

            ## Rejected Records

            * None

            ## Superseded Records

            * None

            ## Deprecated Records

            * None

            ## Records with non-standard statuses

            * None
            """

Feature: Initialise an ADR repository

    Background:
        Given a new working directory

    Scenario: Fail when a repo already exists
        Given a directory named "docs/adr"
        When I run "pyadr init"
        Then it should fail with:
            """
            Directory '{__WORKDIR__}/docs/adr/' already exists. You can use '--force' option to erase.
            """

    Scenario: Force init the repo
        Given a directory named "docs/adr"
        And an empty file named "docs/adr/to-be-erased"
        When I run "pyadr init -f"
        Then it should pass with:
            """
            Directory '{__WORKDIR__}/docs/adr/' already exists. Used '--force' option => Erasing...
            ... Erased.
            """
        And the file named "docs/adr/to-be-erased" should not exist

    Scenario: Succeed with a success message
        When I run "pyadr init"
        Then it should pass with:
            """
            ADR repository successfully initialised at '{__WORKDIR__}/docs/adr/'.
            """

    Scenario: Create the repo directory
        When I run "pyadr init"
        Then it should pass
        And the directory "docs/adr" exists

    Scenario: Should copy the MADR template to the repo
        When I run "pyadr init"
        Then it should pass with:
            """
            Copied MADR template to './docs/adr/template.md'.
            """
        And the file named "docs/adr/template.md" should exist
        And the file "docs/adr/template.md" should contain:
        """
        # [short title of solved problem and solution]

        * Status: [proposed | rejected | accepted | deprecated | ... | superseded by [ADR-0005](0005-example.md)]
        """

    Scenario: Create the ADR to record architecture decisions
        When I run "pyadr init"
        Then it should pass with:
            """
            Created ADR './docs/adr/0000-record-architecture-decisions.md'.
            """
        And the file named "docs/adr/0000-record-architecture-decisions.md" should exist
        And the file "docs/adr/0000-record-architecture-decisions.md" should contain:
        """
        # Record architecture decisions

        * Status: accepted
        * Date: {__TODAY_YYYY_MM_DD__}

        ## Context

        We need to record the architectural decisions made on Opinionated Digital Center.

        ## Decision

        We will use Architecture Decision Records, as [described by Michael Nygard](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions).

        ## Consequences

        See Michael Nygard's article, linked above.
        """

    Scenario: Create the ADR to use MADR
        When I run "pyadr init"
        Then it should pass with:
            """
            Created ADR './docs/adr/0001-use-markdown-architectural-decision-records.md'.
            """
        And the file named "docs/adr/0001-use-markdown-architectural-decision-records.md" should exist
        And the file "docs/adr/0001-use-markdown-architectural-decision-records.md" should contain:
        """
        # Use Markdown Architectural Decision Records

        Adapted from
        [MADR's similar decision record](https://github.com/adr/madr/blob/2.1.2/docs/adr/0000-use-markdown-architectural-decision-records.md).

        * Status: accepted
        * Date: {__TODAY_YYYY_MM_DD__}

        ## Context and Problem Statement

        We want to record architectural decisions made in this project.
        Which format and structure should these records follow?

        ## Considered Options

        * [MADR](https://adr.github.io/madr/) 2.1.2 - The Markdown Architectural Decision Records
        * [Michael Nygard's template](http://thinkrelevance.com/blog/2011/11/15/documenting-architecture-decisions) - The first incarnation of the term "ADR"
        * [Sustainable Architectural Decisions](https://www.infoq.com/articles/sustainable-architectural-design-decisions) - The Y-Statements
        * Other templates listed at <https://github.com/joelparkerhenderson/architecture_decision_record>
        * Formless - No conventions for file format and structure

        ## Decision Outcome

        Chosen option: "MADR 2.1.2", because

        * Implicit assumptions should be made explicit.
          Design documentation is important to enable people understanding the decisions later on.
          See also [A rational design process: How and why to fake it](https://doi.org/10.1109/TSE.1986.6312940).
        * The MADR format is lean and fits our development style.
        * The MADR structure is comprehensible and facilitates usage & maintenance.
        * The MADR project is vivid.
        * Version 2.1.2 is the latest one available when starting to document ADRs.

        ### Positive Consequences

        The ADR are more structured. See especially:
        * [MADR-0002 - Do not use numbers in headings](https://github.com/adr/madr/blob/2.1.2/docs/adr/0002-do-not-use-numbers-in-headings.md).
        * [MADR-0005 - Use (unique number and) dashes in filenames](https://github.com/adr/madr/blob/2.1.2/docs/adr/0005-use-dashes-in-filenames.md).
        * [MADR-0010 - Support categories (in form of subfolders with local ids)](https://github.com/adr/madr/blob/2.1.2/docs/adr/0010-support-categories.md).
        * See [full set of MADR ADRs](https://github.com/adr/madr/blob/2.1.2/docs/adr).

        ### Negative Consequences

        * Learning curve will be slightly longer.
        """

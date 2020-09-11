Feature: Generate a table of content in markdown

    Scenario: Toc command available to `git adr`
        When I run "git adr"
        Then it should pass
        And the command output should contain "toc"

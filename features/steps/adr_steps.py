from behave import given
from behave4cli.command_steps import step_a_file_named_filename_with


@given('an accepted adr file named "{filename}"')
def step_an_accepted_adr_file_named_filename(context, filename):
    context.surrogate_text = """
# My ADR Title

* Status: accepted
* Date: 2020-03-26

## Context and Problem Statement

Context and problem statement.

## Decision Outcome

Decision outcome.
"""
    step_a_file_named_filename_with(context, filename)

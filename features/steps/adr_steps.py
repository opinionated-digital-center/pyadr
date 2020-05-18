from pathlib import Path

from behave import given
from behave4cli.command_steps import step_a_file_named_filename_with
from hamcrest import assert_that, matches_regexp

from pyadr.const import VALID_ADR_FILENAME_WITH_ID_REGEX


@given('an accepted adr file named "{filename}"')
def step_an_accepted_adr_file_named_filename(context, filename):
    path = Path(filename)
    assert_that(path.name, matches_regexp(VALID_ADR_FILENAME_WITH_ID_REGEX))

    title_slug = path.stem.split("-", 1)[1]
    title = " ".join([word.capitalize() for word in title_slug.split("-")])

    context.surrogate_text = f"""
# {title}

* Status: accepted
* Date: 2020-03-26

## Context and Problem Statement

Context and problem statement.

## Decision Outcome

Decision outcome.
"""
    step_a_file_named_filename_with(context, filename)


@given('a proposed adr file named "{filename}"')
def step_an_proposed_adr_file_named_filename(context, filename):
    path = Path(filename)
    assert_that(path.name, matches_regexp(r"^.*-[a-z0-9-]*\.md"))

    title_slug = path.stem.split("-", 1)[1]
    title = " ".join([word.capitalize() for word in title_slug.split("-")])

    context.surrogate_text = f"""
# {title}

* Status: proposed
* Date: 2020-03-26

## Context and Problem Statement

Context and problem statement.

## Decision Outcome

Decision outcome.
"""
    step_a_file_named_filename_with(context, filename)

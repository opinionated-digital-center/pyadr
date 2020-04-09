from behave import given, then
from behave4cli import command_util
from behave4cli.command_steps import step_a_new_working_directory
from git import Repo
from hamcrest import assert_that, calling, equal_to, has_item, has_items, not_, raises


@given("an empty git repo")
def step_an_empty_git_repo(context):
    step_a_new_working_directory(context)
    repo = Repo.init(context.workdir)
    command_util.ensure_context_attribute_exists(context, "repo", repo)


@then('git head should be on branch "{branch}"')
def step_head_should_be_on_branch(context, branch):
    assert_that(context.repo.head.ref, equal_to(context.repo.heads[branch]))


@then('there should be {count:d} commit between head and the branch "{branch}"')
def step_there_should_be_x_commit_between_head_and_branch(context, count, branch):
    assert_that(
        len(list(context.repo.iter_commits(f"HEAD...{branch}"))), equal_to(count)
    )


@then('there should be {count:d} commit in "{branch}"')
def step_there_should_be_x_commit_in_branch(context, count, branch):
    assert_that(len(list(context.repo.iter_commits(branch))), equal_to(count))


# @then('there should be {count:d} commit between git head and the branch "{branch}"')
# def step_there_should_be_x_commit_between_head_and_branch(context, count, branch):
#     assert_that(context.repo.head.ref, equal_to(context.repo.heads[branch]))


@then("the head commit message should be")
def step_current_commit_message_should_be(context):
    assert context.text is not None, "ENSURE: multiline text is provided."

    assert_that(context.repo.head.commit.message, equal_to(context.text))


def files_from_commit(commit):
    return [item for item in commit.tree.traverse() if item.type == "blob"]


@then("the head commit should contain {count:d} files")
def step_head_commit_should_contain_x_files(context, count):
    assert_that(len(files_from_commit(context.repo.head.commit)), equal_to(count))


@then('the head commit should contain the file "{filepath}"')
def step_current_commit_should_contain_file(context, filepath):
    files = files_from_commit(context.repo.head.commit)
    paths = [item.path for item in files]
    assert_that(paths, has_item(filepath))


@then("the head commit should contain the files")
def step_current_commit_should_contain_files(context):
    assert context.table is not None and context.table.has_column(
        "path"
    ), "ENSURE: a table with a 'path' column is provided."

    expected = [row["path"] for row in context.table]

    files = files_from_commit(context.repo.head.commit)
    paths = [item.path for item in files]
    assert_that(paths, has_items(*expected))


@given('I add the file "{filepath}" to the git index')
def step_add_file_to_index(context, filepath):
    context.repo.index.add(filepath)


@given('I commit the git index with message "{message}"')
def step_commit_index_with_message(context, message):
    context.repo.index.commit(message)


@given('I create the branch "{branch}"')
def step_create_the_branch(context, branch):
    context.repo.create_head(branch)
    assert_that(
        calling((lambda x: context.repo.heads[branch])).with_args(1),
        not_(raises(IndexError)),
    )


@then('the branch "{branch}" should exist')
def step_branch_should_exist(context, branch):
    refs = [ref.name for ref in context.repo.heads]
    assert_that(refs, has_item(branch))


@then('the head should be at branch "{branch}"')
def step_head_should_be_at_branch(context, branch):
    assert_that(context.repo.head.ref.name, equal_to(branch))

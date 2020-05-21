from behave import given
from behave4cli.command_steps import step_i_successfully_run_command
from behave4git.git_steps import step_a_starting_git_repo


@given("an initialised git adr repo")
def step_an_initialised_git_adr_repo(context):
    step_a_starting_git_repo(context)
    step_i_successfully_run_command(context, "git adr init")
    context.repo.heads.master.checkout()
    context.repo.git.merge("adr-init-repo")


@given("an initialised git adr only repo")
def step_an_initialised_git_adr_only_repo(context):
    step_a_starting_git_repo(context)
    step_i_successfully_run_command(context, "git adr init --adr-only-repo")
    context.repo.heads.master.checkout()
    context.repo.git.merge("adr-init-repo")

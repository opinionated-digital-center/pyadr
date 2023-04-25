from invoke import task

PACKAGE_DIR = "pyadr"


#################################################################
# setting up dev env
#################################################################


@task
def setup_pre_commit_hooks(context):
    context.run("pre-commit install --hook-type pre-commit")


@task
def setup_release_tools(context):
    context.run('npm install -g semantic-release@"^17.0.4"')
    context.run('npm install -g @semantic-release/changelog@"^5.0.1"')
    context.run('npm install -g @semantic-release/exec@"^5.0.0"')
    context.run('npm install -g @semantic-release/git@"^9.0.0"')
    context.run('npm install -g @semantic-release/github@"^7.0.5"')


#################################################################
# setting up ci-cd env
#################################################################


@task
def setup_cicd_common(context):
    context.run("pip install --upgrade pip")


@task(setup_cicd_common)
def setup_cicd_test_stage(context):
    context.run("git config --global user.name 'Foo Bar'")
    context.run("git config --global user.email 'foo@bar.com'")


@task(setup_cicd_common)
def setup_cicd_release_stage(context):
    pass


@task(setup_cicd_common)
def setup_cicd_publish_stage(context):
    pass


#################################################################
# cleaning
#################################################################


@task
def clean_build(context):
    context.run("rm -fr build/")
    context.run("rm -fr dist/")
    context.run("rm -fr .eggs/")
    context.run("find . -name '*.egg-info' -exec rm -fr {} +")
    context.run("find . -name '*.egg' -exec rm -f {} +")


@task
def clean_pyc(context):
    context.run("find . -name '*.pyc' -exec rm -f {} +")
    context.run("find . -name '*.pyo' -exec rm -f {} +")
    context.run("find . -name '*~' -exec rm -f {} +")
    context.run("find . -name '__pycache__' -exec rm -fr {} +")
    context.run("find . -name '.pytest_cache' -exec rm -fr {} +")


@task
def clean_test(context):
    context.run("rm -fr .tox/")
    context.run("rm -f .coverage")
    context.run("rm -fr htmlcov/")


@task
def clean_venv(context):
    # poetry env remove might not to work if `virtualenvs.in-project = true`
    # (see https://github.com/python-poetry/poetry/issues/2124)
    # so if not, remove whole `.venv` directory using https://unix.stackexchange.com/questions/153763  # noqa
    context.run(
        "poetry env remove $$(poetry env info -p)/bin/python && ([ $$? -eq 0 ]) "
        "|| rm -rf $$(poetry env info -p)"
    )


@task(clean_build, clean_pyc, clean_test)
def clean(context):
    pass


#################################################################
# linting
#################################################################


@task
def lint(context):
    context.run(f"poetry run flake8 {PACKAGE_DIR} tests features")


@task
def tox_lint(context):
    context.run("poetry run tox -e lint")


#################################################################
# formating
#################################################################


@task
def isort(context):
    context.run(f"poetry run isort --profile black {PACKAGE_DIR} tests features")


@task
def black(context):
    context.run(f"poetry run black {PACKAGE_DIR} tests features")


@task(isort, black)
def format(context):
    pass


@task
def format_check(context):
    context.run(f"poetry run isort -c --profile black {PACKAGE_DIR} tests features")
    context.run(f"poetry run black --check {PACKAGE_DIR} tests features")


@task
def tox_format(context):
    context.run("poetry run tox -e format")


#################################################################
# typing
#################################################################


@task
def type(context):
    context.run(f"poetry run mypy -p {PACKAGE_DIR} -p tests")


@task
def tox_type(context):
    context.run("poetry run tox -e type")


#################################################################
# unit testing
#################################################################


@task
def test(context):
    context.run(
        "poetry run pytest "
        f"--cov={PACKAGE_DIR} "
        "--cov-report=html "
        "--cov-report=term tests"
    )


@task(aliases=["tox-test-default-version", "tox-py"])
def tox_test(context):
    context.run("poetry run tox -e py")


@task(aliases=["tox-py311"])
def tox_test_py11(context):
    context.run("poetry run tox -e py311")


@task(aliases=["tox-py310"])
def tox_test_py310(context):
    context.run("poetry run tox -e py310")


@task(aliases=["tox-py39"])
def tox_test_py39(context):
    context.run("poetry run tox -e py39")


@task(aliases=["tox-py38"])
def tox_test_py38(context):
    context.run("poetry run tox -e py38")


@task(aliases=["tox-test-all-versions"])
def tox_test_all(context):
    context.run("poetry run tox -e py311,py310,py39,py38,py37")


#################################################################
# acceptance testing / bdd
#################################################################


@task
def bdd(context):
    context.run("poetry run behave features  --format=pretty --tags=~wip --tags=~skip")


@task(aliases=["tox_bdd_default-version"])
def tox_bdd(context):
    context.run("poetry run tox -e bdd")


@task
def tox_bdd_py310(context):
    context.run("poetry run tox -e bdd-py310")


@task
def tox_bdd_py311(context):
    context.run("poetry run tox -e bdd-py311")


@task
def tox_bdd_py39(context):
    context.run("poetry run tox -e bdd-py39")


@task
def tox_bdd_py38(context):
    context.run("poetry run tox -e bdd-py38")


@task(aliases=["tox-bdd-all-versions"])
def tox_bdd_all(context):
    context.run("poetry run tox -e bdd-py311,bdd-py310,bdd-py39,bdd-py38")


#################################################################
# releasing (full cycle)
#################################################################


@task
def cicd_release(context):
    context.run("npx semantic-release")


#################################################################
# git targets
#################################################################


@task
def prune_branches(context):
    context.run("git remote prune origin")
    context.run(
        "git branch -vv | "
        "grep ': gone]'| "
        "grep -v '\\*' | "
        "awk '{ print $$1; }' | "
        "xargs git branch -d"
    )


@task(aliases=["pbf"])
def prune_branches_force(context):
    context.run("git remote prune origin")
    context.run(
        "git branch -vv | "
        "grep ': gone]'| "
        "grep -v '\\*' | "
        "awk '{ print $$1; }' | "
        "xargs git branch -D"
    )


@task
def post_PR_merge_sync_step_1(context):
    context.run("git switch main")
    context.run("git pull")


@task(post_PR_merge_sync_step_1, prune_branches_force, aliases=["pms"])
def post_PR_merge_sync(context):
    pass

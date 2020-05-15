# file modified from https://gist.github.com/lumengxi/0ae4645124cd4066f676
.PHONY: *

#################################################################
# Shared variables
#################################################################

PACKAGE_DIR=pyadr

define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

#################################################################
# Shared functions
#################################################################

# Check that given variables are set and all have non-empty values,
# die with an error otherwise.
#
# Params:
#   1. Variable name(s) to test.
#   2. (optional) Error message to print.
# Details at https://stackoverflow.com/a/10858332/4374048
check_defined = \
    $(strip $(foreach 1,$1, \
        $(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
    $(if $(value $1),, \
      $(error Undefined $1$(if $2, ($2)): please pass as argument (see help target)))


#################################################################
# help
#################################################################

help:
	@echo "SETUP TARGETS:"
	@echo "\tsetup-dev-env-minimal - setup minimal dev environment for all make targets to work"
	@echo "\tsetup-dev-env-full - setup full dev environment to allow IDE completion"
	@echo "\tsetup-dev-host - setup host dev requirements"
	@echo "\tsetup-pre-commit-hooks - setup pre-commit hooks"
	@echo ""
	@echo "MAIN TARGETS:"
	@echo "\tclean - remove all build, test, coverage and Python artifacts"
	@echo "\ttest - run unit tests"
	@echo "\tbdd - run bdd tests"
	@echo "\tlint - check style with flake8"
	@echo "\tformat - enforce correct format with isort (after a seed-isort-config) and black"
	@echo "\tformat-check - check format for compliance with black and isort"
	@echo "\ttype - check Python typing"
	@echo "\ttox - run tox default targets, usually all tests and checks (see tox.ini)"
	@echo "\ttox-p - same as 'tox', but with parallel runs"
	@echo "\tdocs - generate Sphinx HTML documentation, including API docs"
	@echo "\tdocs-pdf - generate Sphinx PDF documentation, including API docs"
	@echo "\trepl - run the repl tool (bpython in our case)"
	@echo ""
	@echo "INDIVIDUAL TOX TARGETS:"
	@echo "\ttox-test-default-version|tox-test - run unit tests with the default Python"
	@echo "\ttox-test-all-versions|tox-test-all - run unit tests on each Python version declared"
	@echo "\ttox-test-py38 - run unit tests with Python 3.8"
	@echo "\ttox-test-py37 - run unit tests with Python 3.7"
	@echo "\ttox-test-py36 - run unit tests with Python 3.6"
	@echo "\ttox-bdd-default-version|tox-bdd - run bdd tests with the default Python"
	@echo "\ttox-bdd-all-versions|tox-bdd-all - run bdd tests on every Python version declared"
	@echo "\ttox-bdd-py38 - run bdd tests with Python 3.8"
	@echo "\ttox-bdd-py37 - run bdd tests with Python 3.7"
	@echo "\ttox-bdd-py36 - run bdd tests with Python 3.6"
	@echo "\ttox-lint - check style with flake8"
	@echo "\ttox-format - check format for correctness with isort and black"
	@echo "\ttox-type - checks Python typing"
	@echo "\ttox-docs - generate Sphinx HTML documentation, including API docs"
	@echo ""
	@echo "GIT TARGETS:"
	@echo "\tprune-branches - prune obsolete local tracking branches and local branches"
	@echo "\tprune-branches-force|pbf - as above but force delete local branches"
	@echo "\tpost-PR-merge-sync|pms - switch to master, pull and run pbf target"


#################################################################
# setting up dev env
#################################################################

setup-dev-env-minimal: clean
	poetry install --no-root -E format

setup-dev-env-full: clean
	poetry install --no-root -E test -E bdd -E type -E format -E lint -E repl

setup-dev-host:
	./scripts/install_pyenv.sh
	./scripts/install_poetry.sh
	@echo "Host setup correctly. Restart your shell or source your shell config file to be up and running :)"

setup-pre-commit-hooks:
	pre-commit install --hook-type pre-commit

setup-release-tools:
	npm install -g semantic-release@"^17.0.4"
	npm install -g @semantic-release/changelog@"^5.0.1"
	npm install -g @semantic-release/exec@"^5.0.0"
	npm install -g @semantic-release/git@"^9.0.0"
	npm install -g @semantic-release/github@"^7.0.5"

#################################################################
# setting dependencies for automation (tox, cicd)
#################################################################

install-test-dependencies :
	poetry install --no-dev --no-root -E test

install-bdd-dependencies:
	poetry install --no-dev -E bdd

install-format-dependencies:
	poetry install --no-dev --no-root -E format

install-lint-dependencies:
	poetry install --no-dev --no-root -E lint

install-type-dependencies:
	poetry install --no-dev --no-root -E type

install-docs-dependencies:
	poetry install --no-dev --no-root -E docs


#################################################################
# setting up ci-cd env
#################################################################

setup-cicd-common:
	pip install --upgrade pip

setup-cicd-test-stage: setup-cicd-common

setup-cicd-release-stage: setup-cicd-common

setup-cicd-publish-stage: setup-cicd-common


#################################################################
# cleaning
#################################################################

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

clean-venv:
	# poetry env remove might not to work if `virtualenvs.in-project = true`
	# (see https://github.com/python-poetry/poetry/issues/2124)
	# so if not, remove whole `.venv` directory using https://unix.stackexchange.com/questions/153763
	poetry env remove $$(poetry env info -p)/bin/python && ([ $$? -eq 0 ]) || rm -rf $$(poetry env info -p)


#################################################################
# all tests and checks
#################################################################

tox:
	poetry run tox

tox-p:
	poetry run tox -p auto

#################################################################
# repl
#################################################################

repl:
	poetry run bpython

#################################################################
# linting
#################################################################

lint:
	poetry run flake8 $(PACKAGE_DIR) tests features

tox-lint:
	poetry run tox -e lint

#################################################################
# formating
#################################################################

seed-isort:
	poetry run seed-isort-config

isort:
	poetry run isort -rc $(PACKAGE_DIR) tests features -vb

black:
	poetry run black $(PACKAGE_DIR) tests features

format: seed-isort isort black

format-check:
	poetry run isort -c -rc $(PACKAGE_DIR) tests features -vb
	poetry run black --check $(PACKAGE_DIR) tests features

tox-format:
	poetry run tox -e format

#################################################################
# typing
#################################################################

type:
	poetry run mypy -p $(PACKAGE_DIR) -p tests

tox-type:
	poetry run tox -e type

#################################################################
# unit testing
#################################################################

test:
	poetry run pytest --cov=$(PACKAGE_DIR) --cov-report=html --cov-report=term tests

tox-test-default-version: tox-py
tox-test: tox-py
tox-py:
	poetry run tox -e py

tox-test-py38: tox-py38
tox-py38:
	poetry run tox -e py38

tox-test-py37: tox-py37
tox-py37:
	poetry run tox -e py37

tox-test-py36: tox-py36
tox-py36:
	poetry run tox -e py36

tox-test-all-versions: tox-test-all
tox-test-all:
	poetry run tox -e py38,py37,py36


#################################################################
# acceptance testing / bdd
#################################################################

bdd:
	poetry run behave features  --format=pretty --tags=~wip --tags=~skip

tox-bdd-default-version: tox-bdd
tox-bdd:
	poetry run tox -e bdd

tox-bdd-py38:
	poetry run tox -e bdd-py38

tox-bdd-py37:
	poetry run tox -e bdd-py37

tox-bdd-py36:
	poetry run tox -e bdd-py36

tox-bdd-all-versions: tox-bdd-all
tox-bdd-all:
	poetry run tox -e bdd-py38,bdd-py37,bdd-py36

#################################################################
# coverage
#################################################################

# To use/adjust when we start using coverage. Encourage usage of tox.
#coverage:
#	coverage run --source leviathan_serving setup.py test
#	coverage report -m
#	coverage html
#	$(BROWSER) htmlcov/index.html

#################################################################
# docs
#################################################################

docs:
	poetry run sphinx-apidoc -o docs/ $(PACKAGE_DIR)
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

docs-pdf:
	$(MAKE) -C docs latexpdf

tox-docs:
	poetry run tox -e docs
	$(BROWSER) docs/_build/html/index.html

tox-docs-pdf:
	poetry run tox -e docs-pdf

# To use/adjust when we start using coverage. Encourage usage of tox.
#servedocs: docs
#	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

#################################################################
# releasing (full cycle)
#################################################################

cicd-release:
	npx semantic-release

# To use/adjust when we start using coverage. Use Poetry.
#release: clean
#	python setup.py sdist upload
#	python setup.py bdist_wheel upload

#################################################################
# releasing (steps)
#################################################################

# TODO make it more error proof, meaning:
#  - errors if file not found, if item in file not found
#  - use regex to find first item instead of using ${1}
bump:
	$(call check_defined, NEW_VERSION)
	poetry version $(NEW_VERSION)
	poetry run pip install toml
	poetry run python ./scripts/generate_version_file.py

# To use/adjust when we start using coverage. Use Poetry.
#dist: clean
#	python setup.py sdist
#	python setup.py bdist_wheel
#	ls -l dist

publish: clean
	poetry run python scripts/verify_pypi_env_variables.py
	[ -z $$PYPI_REPOSITORY_NAME ] || repo_arg="-r $$PYPI_REPOSITORY_NAME" && poetry publish --build $$repo_arg

#################################################################
# installing developed package/library
#################################################################

install: clean
	poetry install --no-dev

#################################################################
# git targets
#################################################################

prune-branches:
	git remote prune origin
	git branch -vv | grep ': gone]'|  grep -v "\*" | awk '{ print $$1; }' | xargs git branch -d


prune-branches-force:
	git remote prune origin
	git branch -vv | grep ': gone]'|  grep -v "\*" | awk '{ print $$1; }' | xargs git branch -D

pbf: prune-branches-force

post-PR-merge-sync-step-1:
	git switch master
	git pull

post-PR-merge-sync: post-PR-merge-sync-step-1 prune-branches-force

pms: post-PR-merge-sync

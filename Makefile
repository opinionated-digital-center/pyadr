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
	@echo "\tsetup-dev-host - setup dev requirements"
	@echo "\tsetup-pre-commit-hooks - setup pre-commit hooks"
	@echo "\tsetup-release-tools: - setup tools needed for releasing package"
	@echo "\tsetup-cicd-test-stage-github: - setup tools needed for CI/CD test stage (GitHub)"
	@echo "\tsetup-cicd-release-stage-github: - setup tools needed for CI/CD release stage (GitHub)"
	@echo "\tsetup-cicd-test-stage-gitlab: - setup tools needed for CI/CD test stage (GitLab)"
	@echo "\tsetup-cicd-release-stage-gitlab: - setup tools needed for CI/CD release stage (GitLab)"
	@echo ""
	@echo "MAIN TARGETS:"
	@echo "\tclean - remove all build, test, coverage and Python artifacts"
	@echo "\ttox - run tox default targets, usually all tests and checks (see tox.ini)"
	@echo "\ttox-p - same as 'tox', but with parallel runs"
	@echo "\trepl - run the repl tool (bpython in our case)"
	@echo "\tlint - check style with flake8 (uses tox)"
	@echo "\tformat-check - check format for correctness with isort and black (uses tox)"
	@echo "\tformat - enforce correct format with isort (after a seed-isort-config) and black (does not use tox)"
	@echo "\ttype - checks Python typing (uses tox)"
	@echo "\ttest - run tests quickly with the default Python (3.7 - uses tox)"
	@echo "\ttest-all - run tests on every Python version declared (uses tox)"
	@echo "\tbdd - run bdd tests (uses tox)"
	@echo "\tcoverage - [TO BE IMPLEMENTED] check code coverage quickly with the default Python"
	@echo "\tdocs - generate Sphinx HTML documentation, including API docs"
	@echo "\tdocs-pdf - generate Sphinx PDF documentation, including API docs"
	@echo "\tcicd-release - full release - through ci/cd"
	@echo "\trelease - [TO BE IMPLEMENTED] full release - from local (requires linux)"
	@echo "\tbump NEXT_VERSION=[next_version] - bump versions in all relevant files"
	@echo "\tpublish - publish package to pypi"
	@echo "\tdist - [TO BE IMPLEMENTED] package"
	@echo "\tinstall - install the package to the active Python's site-packages"
	@echo ""
	@echo "TOX TARGETS:"
	@echo "\ttox-lint - check style with flake8 (uses tox)"
	@echo "\ttox-format - check format for correctness with isort and black (uses tox)"
	@echo "\ttox-type - checks Python typing (uses tox)"
	@echo "\ttox-test - run tests quickly with the default Python (3.7 - uses tox)"
	@echo "\ttox-test-all - run tests on every Python version declared (uses tox)"
	@echo "\ttox-bdd - run bdd tests (uses tox)"
	@echo "\ttox-docs - generate Sphinx HTML documentation, including API docs"
	@echo "\ttox-docs-pdf - generate Sphinx PDF documentation, including API docs"
	@echo "SECONDARY TARGETS:"
	@echo "\tclean-build - remove build artifacts"
	@echo "\tclean-pyc - remove Python file artifacts"
	@echo "\tclean-test - remove test and coverage artifacts"
	@echo "\tclean-venv - remove poetry's virtualenv"
	@echo "\tpy36 - run tests quickly with the default Python 3.6 (uses tox)"
	@echo "\tpy37 - run tests quickly with the default Python 3.7 (uses tox)"
	@echo "\tpy38 - run tests quickly with the default Python 3.8 (uses tox)"
	@echo "\tseed-isort - run seed-isort-config (does not use tox)"
	@echo "\tisort - run isort to sort imports (does not use tox)"
	@echo "\tblack - run black the uncompromising code formatter (does not use tox)"
	@echo ""
	@echo "GIT TARGETS:"
	@echo "\tprune-branches - prune obsolete local tracking branches and local branches"
	@echo "\tprune-branches-force|pbf - as above but force delete local branches"
	@echo "\tpost-PR-merge-sync|pms - switch to master, pull and run pbf target"


#################################################################
# setting up dev env
#################################################################

dev-env-minimal = -E format
dev-env-full = $(dev-env-minimal) -E test -E bdd -E type -E format -E lint -E repl

setup-dev-env-minimal: clean
	poetry install --no-root $(dev-env-minimal)

setup-dev-env-full: clean
	poetry install --no-root $(dev-env-full)

setup-dev-host:
	./scripts/install_pyenv.sh
	./scripts/install_poetry.sh
	@echo "Host setup correctly. Restart your shell or source your shell config file to be up and running :)"

setup-pre-commit-hooks:
	pre-commit install --hook-type pre-commit

setup-release-tools-common:
	npm install -g semantic-release@"^17.0.4"
	npm install -g @semantic-release/changelog@"^5.0.1"
	npm install -g @semantic-release/exec@"^5.0.0"
	npm install -g @semantic-release/git@"^9.0.0"

setup-release-tools-gitlab: setup-release-tools-common
	npm install -g @semantic-release/gitlab@"^6.0.3"

setup-release-tools-github: setup-release-tools-common
	npm install -g @semantic-release/github@"^7.0.5"

#################################################################
# setting dependencies for automation (tox, cicd)
#################################################################

deps-test:
	poetry install --no-dev --no-root -E test

deps-bdd:
	poetry install --no-dev -E bdd

deps-format:
	poetry install --no-dev --no-root -E format

deps-lint:
	poetry install --no-dev --no-root -E lint

deps-type:
	poetry install --no-dev --no-root -E type

deps-docs:
	poetry install --no-dev --no-root -E docs


#################################################################
# setting up ci-cd env
#################################################################

setup-cicd-python3:
	update-alternatives --install /usr/bin/python python /usr/bin/python3 1
	curl -sSL  https://bootstrap.pypa.io/get-pip.py | python

setup-cicd-poetry:
	curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
	. $(HOME)/.poetry/env && poetry config virtualenvs.create false
	echo "WARNING: you still need to source $$HOME/.poetry/env to access poetry's executable"

setup-cicd-test-stage-gitlab: setup-cicd-poetry

setup-cicd-release-stage-gitlab: setup-cicd-python3 setup-cicd-poetry setup-release-tools-gitlab

setup-cicd-common-github:
	pip install --upgrade pip

setup-cicd-test-stage-github: setup-cicd-common-github

setup-cicd-release-stage-github: setup-cicd-common-github


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
	-poetry run seed-isort-config

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
	poetry run pytest --cov=pyadr --cov-report=html --cov-report=term tests

tox-test: py

tox-py:
	poetry run tox -e py

tox-py37:
	poetry run tox -e py37

tox-py36:
	poetry run tox -e py36

tox-py38:
	poetry run tox -e py38

tox-test-all:
	poetry run tox -e py37,py36,py38

#################################################################
# acceptance testing / bdd
#################################################################

bdd:
	poetry run behave features --format=pretty

tox-bdd:
	poetry run tox -e bdd

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

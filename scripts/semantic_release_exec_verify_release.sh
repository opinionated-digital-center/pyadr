#!/usr/bin/env bash

set -ex

BASEDIR=$(dirname "$0")

${BASEDIR}/verify_git_tags_one_version_tag_present.sh $1

python ${BASEDIR}/verify_pypi_env_variables.py

pip install toml
python ${BASEDIR}/verify_version_not_on_pypi.py $1

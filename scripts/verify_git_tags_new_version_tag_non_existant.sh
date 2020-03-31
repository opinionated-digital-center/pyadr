#!/bin/bash
set -e

if [[ $(git ls-remote --tags | grep "refs/tags/v${1}$") ]]; then
    echo "ERROR: Version '${1}' already exists on the remote repository."
    exit 1
fi

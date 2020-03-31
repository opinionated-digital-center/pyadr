#!/bin/bash
set -e

if [[ ! $(git tag -l | grep '^v') ]]; then
    echo "ERROR: No version tag found. Either initial version tag was not set (suggestion: v0.0.0) or did not fetch enough commits."
    exit 1
fi

#!/bin/bash

which poetry && ([ $? -eq 0 ]) || curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

colorize() {
  if [ -t 1 ]; then printf "\e[%sm%s\e[m" "$1" "$2"
  else echo -n "$2"
  fi
}

set -e

case "$SHELL" in
  /bin/bash )
    profile="$HOME/.bashrc"
    ;;
  /bin/zsh )
    profile="$HOME/.zshrc"
    ;;
  /bin/ksh )
    profile="$HOME/.profile"
    ;;
  /bin/fish )
    profile="$HOME/.config/fish/config.fish"
    ;;
  * )
    profile="your profile"
    ;;
  esac

# Add Poetry to path if necessary
if grep -ql '^# POETRY is installed$' $profile ; then
    echo "POETRY is already set in ${profile}"
else
  { colorize 1 "WARNING"
    echo ": seems you still have not added 'poetry' to the load path => adding the 'poetry' commands to ${profile}."
    echo ""
    echo "# POETRY is installed" >> ${profile}
    echo ". \$HOME/.poetry/env" >> ${profile}
  } >&2
fi

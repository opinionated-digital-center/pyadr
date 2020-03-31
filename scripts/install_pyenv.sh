#!/bin/bash

if [ -z "$PYENV_ROOT" ]; then
  PYENV_ROOT="${HOME}/.pyenv"
fi

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

if [[ ! -d $PYENV_ROOT ]]; then
  curl -s https://pyenv.run | bash
fi

# Add Pyenv to path if necessary
if grep -ql '^# PYENV is installed$' $profile ; then
    echo "PYENV is already set in ${profile}"
else
  { echo ""
    colorize 1 "WARNING"
    echo ": seems you still have not added 'pyenv' to the load path => adding the 'pyenv' commands to ${profile}."
    echo ""
    case "$SHELL" in
    /bin/fish )
      echo "# PYENV is installed" >> ${profile}
      echo "set -x PATH \"${PYENV_ROOT}/bin\" \$PATH" >> ${profile}
      echo 'status --is-interactive; and . (pyenv init -|psub)' >> ${profile}
      echo 'status --is-interactive; and . (pyenv virtualenv-init -|psub)' >> ${profile}
      ;;
    * )
      echo "# PYENV is installed" >> ${profile}
      echo "export PATH=\"${PYENV_ROOT}/bin:\$PATH\"" >> ${profile}
      echo "eval \"\$(pyenv init -)\"" >> ${profile}
      echo "eval \"\$(pyenv virtualenv-init -)\"" >> ${profile}
      ;;
    esac
  } >&2
fi

source $HOME/.bashrc

echo "Python environments installations. If there are missing dependencies, check https://github.com/pyenv/pyenv/wiki/common-build-problems"
LATEST_AVAILABLE_PYTHON_VERSION_38=$(pyenv install --list | grep -v - | grep -v b | grep 3.8 | tail -1)
LATEST_AVAILABLE_PYTHON_VERSION_37=$(pyenv install --list | grep -v - | grep -v b | grep 3.7 | tail -1)
LATEST_AVAILABLE_PYTHON_VERSION_36=$(pyenv install --list | grep -v - | grep -v b | grep 3.6 | tail -1)
pyenv install -s $LATEST_AVAILABLE_PYTHON_VERSION_38
pyenv install -s $LATEST_AVAILABLE_PYTHON_VERSION_37
pyenv install -s $LATEST_AVAILABLE_PYTHON_VERSION_36
echo "py37 is main version we will be working with, then py38 and py36"
pyenv global $LATEST_AVAILABLE_PYTHON_VERSION_37 $LATEST_AVAILABLE_PYTHON_VERSION_38 $LATEST_AVAILABLE_PYTHON_VERSION_36

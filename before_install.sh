#!/bin/bash
set -xeo pipefail

if [ "$TRAVIS_OS_NAME" == "osx" ]; then
    python3 --version
    python3 -m pip install --upgrade virtualenv
    virtualenv -p python3 "$HOME/ktk_venv"
    source "$HOME/ktk_venv/bin/activate"
    which python
    which pip
fi

# https://github.com/JDASoftwareGroup/kartothek/issues/94
which pip
pip install --upgrade pip==19.1.*
which pip
pip install pip-tools
which pip-compile
source compile_requirements.sh
which python
python setup.py bdist_wheel
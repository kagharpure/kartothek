#!/bin/bash
set -xeo pipefail

if [ "$TRAVIS_OS_NAME" == "osx" ]; then
    python3 --version
    python3 -m pip install --upgrade virtualenv
    virtualenv -p python3 "$HOME/ktk_venv"
    source "$HOME/ktk_venv/bin/activate"
fi

# https://github.com/JDASoftwareGroup/kartothek/issues/94
pip install --upgrade pip==19.1.*
pip install pip-tools
./ci/compile_requirements.sh
python setup.py bdist_wheel
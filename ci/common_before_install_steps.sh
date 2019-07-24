#!/bin/bash
set -xeo pipefail

# https://github.com/JDASoftwareGroup/kartothek/issues/94
which pip
pip install --upgrade pip==19.1.*
which pip
pip install pip-tools
which pip-compile
./ci/compile_requirements.sh
which python
python setup.py bdist_wheel

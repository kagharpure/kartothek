#!/bin/bash
set -xeo pipefail

which pip
pip install virtualenv
virtualenv -p python3 ~/kartothek_osx_test_env
source ~/kartothek_osx_test_env/bin/activate
which pip
pip install --upgrade pip!=19.2
pip install pip-tools
which pip
which pip-compile
./ci/compile_requirements.sh
which python
python setup.py bdist_wheel


#pyenv install --list

#!/bin/bash
set -xeo pipefail

which pip
pip install virtualenv
virtualenv -p python3 ~/kartothek_osx_test_env
source ~/kartothek_osx_test_env/bin/activate
which pip
#pyenv install --list

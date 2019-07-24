#!/bin/bash
set -xeo pipefail

#which pip
#pip install virtualenv
#virtualenv -p python3 ~/kartothek_osx_test_env
#source ~/kartothek_osx_test_env/bin/activate
#which pip
pip3 install --upgrade pip==19.1.*
pip3 install pip-tools
./ci/compile_requirements.sh
python3 setup.py bdist_wheel


#pyenv install --list

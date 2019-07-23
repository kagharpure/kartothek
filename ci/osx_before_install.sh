#!/bin/bash
set -xeo pipefail

#pip3 install virtualenv
#virtualenv -p python3 ~/kartothek_osx_test_env
#source ~/kartothek_osx_test_env/bin/activate
pyenv install --list
./ci/common_before_install.sh

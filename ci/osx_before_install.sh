#!/bin/bash
set -xeo pipefail

python3 --version
pip3 install virtualenv
virtualenv -p python3 ~/kartothek_osx_test_env
source ~/kartothek_osx_test_env/bin/activate
which python
python --version
./ci/common_before_install.sh

#!/bin/bash
set -xeo pipefail

pip3 install --upgrade pip!=19.2
pip3 install pip-tools
./ci/compile_requirements.sh
python3 setup.py bdist_wheel

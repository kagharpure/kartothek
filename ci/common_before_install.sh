#!/bin/bash
set -xeo pipefail

pip install --upgrade pip!=19.2
pip install pip-tools
./ci/compile_requirements.sh
python3 setup.py bdist_wheel

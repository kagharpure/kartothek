#!/bin/bash

#if [ "$TRAVIS_OS_NAME" = "osx" ]; then
#
#
#
#fi

pip install --upgrade pip
pip install pip-tools
./compile_requirements.sh
python setup.py bdist_wheel
if [ "$TRAVIS_PYTHON_VERSION" = $PY36V* ]; then
    echo "36 here"
fi
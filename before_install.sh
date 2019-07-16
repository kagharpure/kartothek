#!/bin/bash

if [ ${TRAVIS_PYTHON_VERSION:0:3} = $PY36V ]; then
    export PY36V
fi

if [ $TRAVIS_OS_NAME = "osx" ]; then
    echo "Got OSX"
    echo $PY36V

fi

pip install --upgrade pip
pip install pip-tools
./compile_requirements.sh
python setup.py bdist_wheel

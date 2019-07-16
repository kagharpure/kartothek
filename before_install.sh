#!/bin/bash

if [ ${TRAVIS_PYTHON_VERSION:0:3} = 3.6 ]; then
    export PY36V=$TRAVIS_PYTHON_VERSION
elif [ ${TRAVIS_PYTHON_VERSION:0:3} = 3.7 ]; then
    export PY37V=$TRAVIS_PYTHON_VERSION
fi

if [ $TRAVIS_OS_NAME = "osx" ]; then
    echo "Got OSX"
    echo $PY36V
    echo $PY37V

fi

pip install --upgrade pip
pip install pip-tools
./compile_requirements.sh
python setup.py bdist_wheel

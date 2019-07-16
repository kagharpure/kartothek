#!/bin/bash

if [ "$TRAVIS_PYTHON_VERSION" = 3.6 ]; then
    echo "$TRAVIS_PYTHON_VERSION" > ./python_versions/pyv3.6
    cat ./python_versions/pyv3.6
elif [ "$TRAVIS_PYTHON_VERSION" = 3.7 ]; then
    echo "$TRAVIS_PYTHON_VERSION" > ./python_versions/pyv3.7
    cat ./python_versions/pyv3.7
fi

if [ $TRAVIS_OS_NAME = "osx" ]; then
    echo "Got OSX"
    cat ./python_versions/pyv3.6
    cat ./python_versions/pyv3.7
fi

pip install --upgrade pip
pip install pip-tools
./compile_requirements.sh
python setup.py bdist_wheel

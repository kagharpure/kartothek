#!/bin/bash

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    #brew update
    #brew install pyenv
    #pyenv install
    #source venv/bin/activate
    which -a python
fi

#pip install --upgrade pip
#  - pip install pip-tools
#  - ./compile_requirements.sh
#  - python setup.py bdist_wheel
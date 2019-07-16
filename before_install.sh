#!/bin/bash

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    #brew update
    #brew install pyenv
    #pyenv install
    #source venv/bin/activate
    for p in $(which -a python); do
        eval $($p --version)
    done
fi
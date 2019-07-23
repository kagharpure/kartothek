#!/bin/bash
set -xeo pipefail

which pip
pip install --upgrade pip!=19.2
pip install pip-tools
which pip
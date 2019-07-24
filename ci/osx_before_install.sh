#!/bin/bash
set -xeo pipefail

python3 -m pip install --upgrade virtualenv
virtualenv -p python3 --system-site-packages "$HOME/venv"
source "$HOME/venv/bin/activate"

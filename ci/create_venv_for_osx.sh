#!/bin/bash
set -xeo pipefail

python3 -m pip install --upgrade virtualenv
virtualenv -p python3 --system-site-packages "$HOME/ktk_venv"
source "$HOME/ktk_venv/bin/activate"

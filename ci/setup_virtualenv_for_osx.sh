#!/bin/bash
set -xeo pipefail

[ ! -z "$(which python3)" ] && \
[[ $(python3 --version | cut -d ' ' -f2) != 3.* ]] && \
exit 1
python3 -m pip install --upgrade virtualenv
virtualenv -p python3 "$HOME/ktk_venv"
source "$HOME/ktk_venv/bin/activate"

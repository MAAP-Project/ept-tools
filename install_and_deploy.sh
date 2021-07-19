#!/bin/bash
set -Eeuo pipefail
# set -x # print each command before executing

echo "Installing aws cdk (npm)"
npm install -g aws-cdk
# Note: zsh users need to use ""
echo "Installing python packages (pip)"
pip install -e ".[deploy]"

cdk deploy --all --require-approval never
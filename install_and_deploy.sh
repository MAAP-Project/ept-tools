#!/bin/bash
set -Eeuo pipefail
set -x # print each command before executing

echo "Installing aws cdk (npm)"
npm install -g aws-cdk

echo "Installing python packages (pip)"
pip install -e ".[deploy]"

du -sm

echo "Deploying to AWS"
cdk deploy --all --require-approval never -vvv
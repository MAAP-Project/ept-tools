#!/bin/bash
set -Eeuo pipefail
set -x # print each command before executing

npm --version

npm pack --unsafe-perm

echo "Installing aws cdk (npm)"
npm install -g aws-cdk

echo "Installing python packages (pip)"
pip install -e ".[deploy]"


echo "Deploying to AWS"
cdk deploy --all --require-approval never -vvv
#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd ${DIR}/..

#./scripts/build-lambda-zip.sh

FUNCTION=${FUNCTION:="ept-serve-tiles"}
REGION=${REGION:="us-east-1"}
ROLE_ARN=${ROLE:="arn:aws:iam::532321095167:role/aimee-lambda-api-gateway"}

echo "Creating lambda function"
echo "  Function: ${FUNCTION}"
echo "  Region: ${REGION}"
echo "  Role: ${ROLE_ARN}"
echo "  Handler: lib/lambda.handler"

aws2 lambda create-function \
    --runtime "nodejs10.x" \
    --role ${ROLE} \
    --region ${REGION} \
    --function-name ${FUNCTION} \
    --zip-file fileb://package/lambda.zip \
    --handler "lib/lambda.handler" &&
echo "Done"

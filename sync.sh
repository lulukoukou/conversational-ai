#!/usr/bin/env bash
#===============================================================================
#
#          FILE: sync.sh
# 
#         USAGE: ./sync.sh 
# 
#   DESCRIPTION: 
# 
#         NOTES: ---
#        AUTHOR: Hao Fang, hfang@uw.edu
#       CREATED: 03/01/2017 17:19
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
set -e

if [[ -f lambdaFunc.zip ]]; then
  echo "lambdaFunc.zip already exists!"
  rm lambdaFunc.zip
fi

cd lambdaFunc/
zip -r ../lambdaFunc.zip *
cd ..

# NOTE: aws --version should be aws-cli/1.11.53
# upload via s3
/usr/local/bin/aws s3 cp lambdaFunc.zip s3://verifyfunction1/lambdaFunc.zip
# update the lambda to use the new code
/usr/local/bin/aws lambda update-function-code \
		    --function-name sayHello   \
		    --s3-bucket verifyfunction1 \
		    --s3-key lambdaFunc.zip

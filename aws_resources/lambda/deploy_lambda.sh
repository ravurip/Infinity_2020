#!/bin/bash

if [ $# -eq 1 ]; then
  functionName=$1
elif [ $# -eq 0 ]; then
  echo "Please input the function name to be deployed"
  exit 127
fi

basepath="/home/pradeepr/IdeaProjects/Infinity_2020"
lambdaZipFile=$functionName.zip

cd $basepath/aws_resources/lambda/$functionName

zip -r ../$lambdaZipFile *

if [ $? -ne 0 ]; then
  echo "Failed while zipping the function ${functionName}"
  exit 1
fi

aws lambda update-function-code --function-name $functionName --zip-file fileb://../$lambdaZipFile

if [ $? -ne 0 ]; then
  echo "Failed to deploy lambda function Please check the logs"
  exit 1
fi

echo "Deployed lambda function successfully"
exit 0
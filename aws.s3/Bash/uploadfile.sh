#!/bin/bash

if [ "$#" -ne 4 ]; then
	echo "Wrong Syntax!!"
    echo "Example: ./uploadfile userName password fileKey filePath"
    exit 1
fi

# Check if Bucket exist
result="$(aws s3 ls s3://ttttt456)"
if [[ $result = "" ]]; then 
	echo "Create Bucket";
	aws s3 mb s3://ttttt456

	# Create Account.txt, File.txt
	echo "{}" > Account.txt
	echo "{}" > File.txt

	# Upload Account.txt, File.txt
	aws s3 cp Account.txt s3://ttttt456/Account.txt
	aws s3 cp File.txt s3://ttttt456/File.txt
fi

# Download Files
aws s3 cp s3://ttttt456/Account.txt Account.txt
aws s3 cp s3://ttttt456/File.txt File.txt

# Check if account exist
cmd="jq \".$1\" Account.txt"
result=$(eval $cmd)
# echo $result
if [[ $result = null ]]; then 
	echo "Account Not Exist";
	exit 1
fi

# Check if password correct
cmd="jq \".$1.Password\" Account.txt"
result=$(eval $cmd)
# echo $result
# echo $2
if [[ $result != "\"$2\"" ]]; then 
	echo "Wrong Pasword";
	exit 1
fi

# Check if upload file exist
if [[ ! -f $4 ]]; then
    echo "File not found!"
fi

# Update File.txt
cmd="jq '. +={\"$1\":{ \"$3\":\"$4\" }}' File.txt"
output=$(eval $cmd)

# Write result to file
echo $output > File.txt

# Update s3
aws s3 cp File.txt s3://ttttt456/File.txt

# Start to Upload File
aws s3 cp $4 "s3://ttttt456/$1/$4"





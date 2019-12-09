#!/bin/bash

if [ "$#" -ne 3 ]; then
	echo "Wrong Syntax!!"
    echo "Example: ./deletefile userName password file-key"
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

# Check if 'file-key' exist
cmd="jq \".$1.$3\" File.txt"
result=$(eval $cmd)
# echo $result
if [[ $result = null ]]; then 
	echo "file-key Not Exist";
	exit 1
fi

# remove file-key from File.txt
cmd="jq \"del(.$1.$3)\" File.txt"
result=$(eval $cmd)

# Write result to file
echo $result > File.txt

# Update files
aws s3 cp File.txt s3://ttttt456/File.txt

#!/bin/bash

if [ "$#" -ne 3 ]; then
	echo "Wrong Syntax!!"
    echo "Example: ./createuser UserName Pawssord yourEmail@gmail.com"
    exit 1
fi

# echo "Pass"

# echo "$1" # UserName
# echo "$2" # Pawssord
# echo "$3" # yourEmail@gmail.com


# First time create user
result="$(aws s3 ls s3://ttttt456)"
if [[ $result = "" ]]; then 
	echo "First Time Create User";
	aws s3 mb s3://ttttt456

	# Create Account.txt, File.txt
	echo "{}" > Account.txt
	echo "{}" > File.txt
	
	# Add User to file
	cmd="jq '. +={\"$1\":{ \"Password\":\"$2\", \"Email\":\"$3\" }}' Account.txt"
	output=$(eval $cmd)

	# Write result to file
	echo $output > Account.txt
	
	# Upload Account file
	aws s3 cp Account.txt s3://ttttt456/Account.txt
	aws s3 cp File.txt s3://ttttt456/File.txt
else 
	echo "Not First time creating user";

	# Download Account file, File.txt
	aws s3 cp s3://ttttt456/Account.txt .
	aws s3 cp s3://ttttt456/File.txt .

	# Add User to file
	cmd="jq '. +={\"$1\":{ \"Password\":\"$2\", \"Email\":\"$3\" }}' Account.txt"
	output=$(eval $cmd)

	# Write result to file
	echo $output > Account.txt

	# Upload Account file
	aws s3 cp Account.txt s3://ttttt456/Account.txt

fi
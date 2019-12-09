#!/usr/bin/env python3

# [1] https://docs.aws.amazon.com/code-samples/latest/catalog/code-catalog-python-example_code-s3.html
import logging
import boto3
import sys
import json
from botocore.exceptions import ClientError

from CreateUser import get_object, s3_download_file, login

if __name__ == '__main__':
    # print('Argument List:', str(sys.argv))
    
    if len(sys.argv) != 3:
        print("Wrong Argument!!")
        print("Example: python3 ListFiles.py MrCat NiceCat")
        exit(0)

    bucket_name = 'ttttt99999'
    region = 'us-west-2'

    # get_object(bucket_name, "Account.txt")
    # get_object(bucket_name, "File.txt")
    s3_download_file(bucket_name, "Account.txt")
    s3_download_file(bucket_name, "File.txt")

    # Check Account & Password
    acc = sys.argv[1]
    pwd = sys.argv[2]
    login(acc, pwd)


    data = ''
    with open('./File.txt') as json_file:
        data = json.load(json_file)
        try:
            print(acc, "files")
            print('-----------------------------------')
            for key, value in data[acc].items():
                print(key)
        except:
            print('No Stored Files!!')



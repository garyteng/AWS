#!/usr/bin/env python3

# [1] https://docs.aws.amazon.com/code-samples/latest/catalog/code-catalog-python-example_code-s3.html
import logging
import boto3
import sys
import json
from botocore.exceptions import ClientError

from CreateUser import get_object, put_object, s3_download_file, login



if __name__ == '__main__':
    # print('Argument List:', str(sys.argv))
    
    if len(sys.argv) != 5:
        print("Wrong Argument!!")
        print("Example: python3 UploadFile.py MrCat NiceCat My-Favorite-Dog-Picture ./dog1.jpg")
        exit(0)

    bucket_name = 'ttttt99999'
    region = 'us-west-2'

    s3_download_file(bucket_name, "Account.txt")
    s3_download_file(bucket_name, "File.txt")

    acc = sys.argv[1]
    pwd = sys.argv[2]
    key = sys.argv[3]
    path = sys.argv[4]

    # Check account & password
    login(acc, pwd)

    data = ''
    with open('./File.txt') as json_file:
        data = json.load(json_file)

    with open('./File.txt', 'w') as json_file:

        try:
            # print(data[acc])
            data[acc][key] = path
        except:
            data[acc] = {}
            data[acc][key] = path
     
        json.dump(data, json_file)

    ret = put_object(bucket_name, key, path)
    if ret == False:
        print('File is not found!!')
    else:
        put_object(bucket_name, "File.txt", "./File.txt")
        print('Successfully Upload!')
    

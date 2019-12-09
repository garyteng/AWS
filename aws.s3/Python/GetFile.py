#!/usr/bin/env python3

# [1] https://docs.aws.amazon.com/code-samples/latest/catalog/code-catalog-python-example_code-s3.html
import logging
import boto3
import sys
import json
from botocore.exceptions import ClientError
import os

from CreateUser import get_object, s3_download_file, login


# def s3_download_file(BUCKET_NAME, KEY):
#     s3 = boto3.resource('s3')

#     try:
#         s3.Bucket(BUCKET_NAME).download_file(KEY, KEY)
#     except botocore.exceptions.ClientError as e:
#         if e.response['Error']['Code'] == "404":
#             print("The object does not exist.")
#         else:
#             raise



if __name__ == '__main__':
    # print('Argument List:', str(sys.argv))
    
    if len(sys.argv) != 5:
        print("Wrong Argument!!")
        print("Example: python3 GetFile.py MrCat NiceCat My-Favorite-Dog-Picture ./MyFavoriteDog")
        exit(0)

    bucket_name = 'ttttt99999'
    region = 'us-west-2'

    # get_object(bucket_name, "Account.txt")
    # get_object(bucket_name, "File.txt")
    s3_download_file(bucket_name, "Account.txt")
    s3_download_file(bucket_name, "File.txt")

    acc  = sys.argv[1]
    pwd  = sys.argv[2]
    key  = sys.argv[3]
    path = sys.argv[4]

    # Check Account & Password
    login(acc, pwd)

    data = ''
    file = ''
    with open('./File.txt') as json_file:
        data = json.load(json_file)
        if acc not in data:
            print('File is not found!')
            exit(0)
        elif key not in data[acc]:
            print('File is not found!')
            exit(0)

        file = data[acc][key]
        full_path = path+'/'+file
        print(full_path)


    os.makedirs(path, exist_ok=True)
    s3_download_file(bucket_name, key, full_path)
    print('Successfully download!!')

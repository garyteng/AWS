#!/usr/bin/env python3

# [1] https://docs.aws.amazon.com/code-samples/latest/catalog/code-catalog-python-example_code-s3.html
import logging
import boto3
import sys
import json
from botocore.exceptions import ClientError

from CreateUser import get_object, s3_download_file, login


# def s3_download_file(BUCKET_NAME, KEY, LOCATION = 'not set' ):
#     s3 = boto3.resource('s3')

#     try:
#         if LOCATION == 'not set':
#             LOCATION = KEY

#         s3.Bucket(BUCKET_NAME).download_file(KEY, LOCATION)
#     except botocore.exceptions.ClientError as e:
#         if e.response['Error']['Code'] == "404":
#             print("The object does not exist.")
#         else:
#             raise

def delete_object(bucket_name, object_name):
    """Delete an object from an S3 bucket

    :param bucket_name: string
    :param object_name: string
    :return: True if the referenced object was deleted, otherwise False
    """

    # Delete the object
    s3 = boto3.client('s3')
    try:
        s3.delete_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == '__main__':
    # print('Argument List:', str(sys.argv))
    
    if len(sys.argv) != 4:
        print("Wrong Argument!!")
        print("Example: python3 DeleteFile.py MrCat NiceCat My-Favorite-Dog-Picture")
        exit(0)

    bucket_name = 'ttttt99999'
    region = 'us-west-2'


    s3_download_file(bucket_name, "Account.txt")
    s3_download_file(bucket_name, "File.txt")

    acc  = sys.argv[1]
    pwd  = sys.argv[2]
    key  = sys.argv[3]

    # Check Account & Password
    acc = sys.argv[1]
    pwd = sys.argv[2]
    login(acc, pwd)

    data = ''
    # make sure that file is belonged to you!!
    with open('./File.txt') as json_file:
        data = json.load(json_file)
        if acc not in data:
            print('File is not found!')
            exit(0)
        elif key not in data[acc]:
            print('File is not found!')
            exit(0)


    delete_object(bucket_name, key)

    data[acc].pop(key, None)

    with open('File.txt', 'w') as data_file:
        data = json.dump(data, data_file)


#!/usr/bin/env python3

# [1] https://docs.aws.amazon.com/code-samples/latest/catalog/code-catalog-python-example_code-s3.html
import logging
import boto3
import sys
import json
from botocore.exceptions import ClientError

# Login Check
def login(acc, pwd):
    with open('./Account.txt') as json_file:
        data = json.load(json_file)

        if acc not in data:
            print('This user is not existed.')
            exit(0)
        elif pwd not in data[acc]['Password']:
            print('Wrong Password')
            exit(0)

# Check if bucket exists
def bucket_exists(bucket_name):
    """Determine whether bucket_name exists and the user has permission to access it

    :param bucket_name: string
    :return: True if the referenced bucket_name exists, otherwise False
    """

    s3 = boto3.client('s3')
    try:
        response = s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.debug(e)
        return False
    return True

def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
        
        # Add Account.txt & File.txt
        create_empty_json_file("Account.txt")
        create_empty_json_file("File.txt")
        put_object(bucket_name, "Account.txt", "./Account.txt")
        put_object(bucket_name, "File.txt"   , "./File.txt")

    except ClientError as e:
        logging.error(e)
        return False
    return True

def create_empty_json_file(file_json_name):
    f= open(file_json_name,"w+")
    f.write("{}")
    f.close()

def put_object(dest_bucket_name, dest_object_name, src_data):
    """Add an object to an Amazon S3 bucket

    The src_data argument must be of type bytes or a string that references
    a file specification.

    :param dest_bucket_name: string
    :param dest_object_name: string
    :param src_data: bytes of data or string reference to file spec
    :return: True if src_data was added to dest_bucket/dest_object, otherwise
    False
    """

    # Construct Body= parameter
    if isinstance(src_data, bytes):
        object_data = src_data
    elif isinstance(src_data, str):
        try:
            object_data = open(src_data, 'rb')
            # possible FileNotFoundError/IOError exception
        except Exception as e:
            # logging.error(e)
            return False
    else:
        logging.error('Type of ' + str(type(src_data)) +
                      ' for the argument \'src_data\' is not supported.')
        return False

    # Put the object
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=dest_bucket_name, Key=dest_object_name, Body=object_data)
    except ClientError as e:
        # AllAccessDisabled error == bucket not found
        # NoSuchKey or InvalidRequest error == (dest bucket/obj == src bucket/obj)
        logging.error(e)
        return False
    finally:
        if isinstance(src_data, str):
            object_data.close()
    return True

def get_object(bucket_name, object_name):
    """Retrieve an object from an Amazon S3 bucket

    :param bucket_name: string
    :param object_name: string
    :return: botocore.response.StreamingBody object. If error, return None.
    """

    # Retrieve the object
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        # AllAccessDisabled error == bucket or object not found
        logging.error(e)
        return None
    # Return an open StreamingBody object
    return response['Body']


def s3_download_file(bucket_name, key, location = 'not set'):
    s3 = boto3.resource('s3')

    if location == 'not set':
        location = key

    try:
        s3.Bucket(bucket_name).download_file(key, location)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

def add_user(user, pwd, email):
    # add user data to Account.txt
    data = ''
    with open('./Account.txt') as json_file:
        data = json.load(json_file)
        # data=json.load('./Account.txt')

        # data[user] = """{{ "Password": \"{}\", "Email": \"{}\" }}""".format(pwd, email)
        data[user] = {}
        data[user]["Password"] = pwd
        data[user]["Email"] = email
        # Check data is correct, for debugging
        # for key, value in data.items():
        #     print(key, " - ", value)

        # json.dump(data, json_file)

    with open('./Account.txt', 'w') as json_file:
        json.dump(data, json_file)

if __name__ == '__main__':

    # print('Argument List:', str(sys.argv))
    
    if len(sys.argv) != 4:
        print("Wrong Argument!!")
        print("Example: python3 CreateUser.py MrCat NiceCat cats@cats.com")
        exit(0)

    bucket_name = 'ttttt99999'
    region = 'us-west-2'
    if not bucket_exists(bucket_name):
        ret = create_bucket(bucket_name, region)

        if ret == False:
            print('Fail to create bucket')
            exit(0)

    # get_object(bucket_name, "Account.txt")
    # get_object(bucket_name, "File.txt")
    s3_download_file(bucket_name, "Account.txt")
    s3_download_file(bucket_name, "File.txt")

    add_user(sys.argv[1], sys.argv[2], sys.argv[3])
    put_object(bucket_name, "Account.txt", "./Account.txt")

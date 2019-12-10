#!/usr/bin/env python3

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object

from collections import OrderedDict
import boto3

ec2 = boto3.client('ec2')
response = ec2.describe_instances(
    Filters=[
        { 'Name':'instance-state-name', 'Values':['running'] }
    ]
)

print( len(response['Reservations']) )

ec2info = OrderedDict()

for instance in response['Reservations']:
	# print(instance['Instances']);
	# print(instance['Instances'][0]['InstanceId'])
	myInstance = instance['Instances'][0];

	ec2info[ myInstance['InstanceId'] ] = {
        'Instance ID' : myInstance['InstanceId'],
        'Name': myInstance['Tags'][0]['Value'],
        'Type': myInstance['InstanceType'],
        'Image ID' : myInstance['ImageId'],
        'State': myInstance['State']['Name'],
        'Key' : myInstance['KeyName'],
        'VPC ID' : myInstance['VpcId'],
        'Subnet ID' : myInstance['SubnetId'],
        'Security Group' : myInstance['SecurityGroups'],
        'Private IP': myInstance['PrivateIpAddress'],
        'private DNS Name' : myInstance['PrivateDnsName'],
        'Public IP': myInstance['PublicIpAddress'],
        'Public DNS Name' : myInstance['PublicDnsName']
        }

# Show results

for instance_id, instance in ec2info.items():
    for key, value in instance.items():
        print(key, ': ', value);
    print("-------------------------------------------------------")
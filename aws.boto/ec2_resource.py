#!/usr/bin/env python3

# [Reference] https://gist.github.com/dastergon/b4994c605f76d528d0c4

from collections import OrderedDict
import boto3

# Connect to EC2
ec2 = boto3.resource('ec2')

# Get information for all running instances
running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

ec2info = OrderedDict()
for instance in running_instances:

    print(instance);

    name = '';
    for tag in instance.tags:
        if 'Name'in tag['Key']:
            name = tag['Value']
    #         print(name)
    # Add instance info to a dictionary         
    ec2info[instance.id] = {
        'Instance ID' : instance.id,
        'Name': name,
        'Type': instance.instance_type,
        'Image ID' : instance.image_id,
        'State': instance.state['Name'],
        'Key' : instance.key_name,
        'VPC ID' : instance.vpc_id,
        'Subnet ID' : instance.subnet_id,
        'Security Group' : instance.security_groups,
        'Private IP': instance.private_ip_address,
        'private DNS Name' : instance.private_dns_name,
        'Public IP': instance.public_ip_address,
        'Public DNS Name' : instance.public_dns_name
        }

    # print(ec2info[instance.id]);

for instance_id, instance in ec2info.items():
    for key, value in instance.items():
        print(key, ': ', value);
    print("-------------------------------------------------------")
#!/usr/bin/env python3

import boto3

client = boto3.client('s3')

buckets = client.list_buckets()

for bucket in buckets['Buckets']:
	print('\n\n-------------------------------------------')
	print('-------------------Bucket------------------------')
	name = bucket['Name']

	response = client.list_objects(Bucket=name)
	# print('\n******', response, '\n******')


	# print(bucket)
	# print(bucket['CreationDate'])
	# print(bucket['Name'])
	# print('---------------------------')

	print('Bucket Name:', bucket['Name'])
	print('Creation Date:', bucket['CreationDate'])
	print('Owner:', buckets['Owner'])

	if 'Contents' not in client.list_objects(Bucket=name):
		continue

	for obj in client.list_objects(Bucket=name)['Contents']:
		print('*********** Object **************')
		print('Key:', obj['Key'])
		print('Size:', obj['Size'])
		print('Last Modified:', obj['LastModified'])
		print('Storage Class:', obj['StorageClass'])


print('-------------------------------------------')
print('-------------------------------------------------\n\n')		

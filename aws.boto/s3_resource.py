#!/usr/bin/env python3

import boto3

s3 = boto3.resource('s3')
myBucket = 0;
for bucket in s3.buckets.all():
	print('\n\n-------------------------------------------')
	print('-------------------Bucket------------------------')

	print('Name:', bucket.name)
	#	print('Creation Date:', bucket['CreationDate'])
	# print('Owner:', buckets['Owner'])

	for obj in bucket.objects.all():

		print('*********** Object **************')
		print('Key:', obj.key)
		print('Size:', obj.size)
		print('Last Modified:', obj.last_modified)
		print('Storage Class:', obj.storage_class)

		# print(bucket.name, ' * ',obj.key)
		# print(obj)
		# print(obj.last_modified)
		# print(s3.ObjectSummary(bucket.name, obj.key))
		# print(s3.Object(bucket.name, obj.key))
		# print(obj.load())
		# print(bucket.load())
		# print('-----------Response--------------')
		# response = client.get_object(
		# 	Bucket=bucket.name,
		# 	Key=obj.key
		# 	)
		# print(response)
		# print('-------------------------')
	# print(bucket)
	# print(bucket.name)
	# myBucket = bucket

print('-------------------------------------------')
print('-------------------------------------------------\n\n')	

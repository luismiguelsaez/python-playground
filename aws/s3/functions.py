import boto3
from sys import argv

key_id = argv[1]
key_sec = argv[2]
region = argv[3]
bucket_name = argv[4]

s = boto3.Session(
      aws_access_key_id=key_id,
      aws_secret_access_key=key_sec,
      region_name=region
    )

c = s.client('s3')

paginator = c.get_paginator('list_object_versions')
pagination_conf = {'MaxItems': 100, 'PageSize': 100}

iterator = paginator.paginate(
            Bucket=bucket_name,
            PaginationConfig=pagination_conf
          )

del_objects = {
  'Objects': []
}

del_batch_size = 100
count = 0
del_list = []

for batch in iterator:
  if count <= del_batch_size:
    if len(batch['KeyMarker']) > 0 and len(batch['VersionIdMarker']) > 0:
      object = {
        'Key': batch['KeyMarker'],
        'VersionId': batch['VersionIdMarker']
      }
      del_list.append(object)
  else:
    del_objects['Objects'] = del_list
    del_res = c.delete_objects(Bucket=bucket_name, Delete=del_objects)
    print(f"Deleted {count} objects: {del_res}")
    del_list = list()
    count = 0
  count += 1

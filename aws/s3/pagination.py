import boto3

s = boto3.Session(profile_name='lokalise-admin-live')
c = s.client("s3")

marker = None
bucket_name = 'lokalise-live-ota-mdn-bundles'
limit_date = '2022-02-17 00:00:00+00:00'
date_operator = '>='

while True:
  paginator = c.get_paginator('list_objects_v2')
  response_iterator = paginator.paginate(
          Bucket=bucket_name,
          PaginationConfig={
              'MaxItems': 100,
              'PageSize': 100,
              'StartingToken': marker})

  filtered_iterator = response_iterator.search(
      f"Contents[?to_string(LastModified){date_operator}'\"{limit_date}\"'].Key"
  )

  for key in filtered_iterator:
    bundle_project = key.split('/')[1]
    bundle_type = key.split('/')[2]
    bundle_filename = key.split('/')[3]
    response_object = c.get_object(Bucket=bucket_name, Key=key)

    obj_encoding = None if not 'ContentEncoding' in response_object else response_object['ContentEncoding']
    obj_type = response_object['ContentType']
    obj_lastmod = response_object['LastModified']
    obj_length = response_object['ContentLength']

    #print(f"{key} {obj_lastmod} {obj_type} {obj_encoding} {obj_length}")
    if obj_encoding is None:
      print(response_object['Body'].read())

  marker = response_iterator.resume_token

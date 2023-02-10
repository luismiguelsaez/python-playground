import boto3

with open('/tmp/s3-non-gzip.txt', 'r') as f:
  lines = [x.strip() for x in f.readlines()]

s = boto3.Session(profile_name='lokalise-admin-live')
c = s.client("s3")

marker = None
bucket_name = 'lokalise-live-ota-mdn-bundles'
limit_date = '2022-02-17 00:00:00+00:00'
date_operator = '>='

for l in lines:
  url = l.split('\t')[0]
  key = "/".join(url.split('/')[3:7])

  response_object = c.get_object(Bucket=bucket_name, Key=key)

  obj_encoding = 'N/A' if not 'ContentEncoding' in response_object else response_object['ContentEncoding']
  obj_type = response_object['ContentType']
  obj_lastmod = response_object['LastModified']
  obj_length = response_object['ContentLength']

  print(f"{key} {obj_lastmod} {obj_type} {obj_encoding} {obj_length}")

from boto3 import Session
from json import loads as json_loads

session = boto3.Session(profile_name="lokalise-admin-live")

s3_client = session.client("s3")

bucket_names = [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]

for bucket in bucket_names:
  bucket_policy = s3_client.get_bucket_policy(Bucket=bucket)
  bucket_policy_dict = json_loads.loads(bucket_policy)

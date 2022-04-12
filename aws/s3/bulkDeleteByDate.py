import boto3
from datetime import datetime, timezone
import argparse

parser = argparse.ArgumentParser(description='Remove objects from bucket, based on last modified date')
parser.add_argument('--bucket', required=True, action='store', help='Name of the bucket')
parser.add_argument('--year', required=True, action='store', help='Year')
parser.add_argument('--month', required=True, action='store', help='Month')
parser.add_argument('--day', required=True, action='store', help='Day')

args = vars(parser.parse_args())

bucket = args["bucket"]
year   = int(args["year"])
month  = int(args["month"])
day    = int(args["day"])

s3 = boto3.client("s3")

paginator = s3.get_paginator("list_objects_v2")
pages = paginator.paginate(Bucket=bucket)
date_check = datetime(year, month, day)

keys_to_delete = []
for page in pages:
    for object in page["Contents"]:
        if object["LastModified"] > date_check.replace(tzinfo=timezone.utc):
            print("Found object with date [{}]: {}".format(object["LastModified"], object["Key"]))
            keys_to_delete.append({"Key": object["Key"]})

#s3.delete_objects(Bucket=bucket, Delete={"Objects": keys_to_delete})
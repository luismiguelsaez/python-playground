import boto3
from datetime import datetime, timezone
import argparse
import re

parser = argparse.ArgumentParser(description='Remove objects from bucket, based on last modified date')
parser.add_argument('--bucket', required=True, action='store', help='Name of the bucket')
parser.add_argument('--prefix', required=True, action='store', help='Object name prefix')
parser.add_argument('--modified-before', required=True, action='store', help='Objects where created before this date ( %Y-%m-%d %H:%M:%S )')
parser.add_argument('--modified-after', required=True, action='store', help='Objects where created after this date ( %Y-%m-%d %H:%M:%S )')

args = vars(parser.parse_args())

bucket = args["bucket"]
namePrefix = args["prefix"]
modBefore = args["modified_before"]
modAfter  = args["modified_after"]


s3 = boto3.client("s3")

paginator = s3.get_paginator("list_objects_v2")
pages = paginator.paginate(Bucket=bucket)
dateBefore = datetime.utcnow().strptime(modBefore, '%Y-%m-%d %H:%M:%S')
dateAfter = datetime.utcnow().strptime(modAfter, '%Y-%m-%d %H:%M:%S')

keys_to_delete = []
for page in pages:
    for object in page["Contents"]:
        if object["LastModified"] > dateAfter.replace(tzinfo=timezone.utc) and object["LastModified"] < dateBefore.replace(tzinfo=timezone.utc):
            if re.search("^{}".format(namePrefix), object["Key"]):
                print("Found object with date [{}]: {}".format(object["LastModified"], object["Key"]))
                keys_to_delete.append({"Key": object["Key"]})

#s3.delete_objects(Bucket=bucket, Delete={"Objects": keys_to_delete})
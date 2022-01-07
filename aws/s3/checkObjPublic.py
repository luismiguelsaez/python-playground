from boto3 import session, s3
from sys import argv as sysArgs
from os import path as osPath

def checkPublicACL(s3Cli, bucket, key):
  isPublic = False

  obj_acl = s3Cli.get_object_acl(Bucket=bucket, Key=key)

  for grant in obj_acl["Grants"]:
    if grant["Grantee"]["Type"] == "Group" and grant["Grantee"]["URI"] == "http://acs.amazonaws.com/groups/global/AllUsers" and grant["Permission"] in ("FULL_CONTROL", "READ"):
      isPublic = True

  return isPublic


def main():

  if len(sysArgs) < 3:
    print("Usage: " + osPath.basename(__file__) + " profile bucket")
    exit(1)

  awsProfile = sysArgs[1]
  awsS3Bucket = sysArgs[2]

  sess = session.Session(profile_name=awsProfile)
  s3_cli = sess.client("s3")

  s3_objects = s3_cli.list_objects(Bucket=awsS3Bucket)

  for obj in s3_objects["Contents"]:
    if checkPublicACL(s3_cli, awsS3Bucket, obj["Key"]):
      print(obj["Key"])

if __name__ == "__main__":
  main()

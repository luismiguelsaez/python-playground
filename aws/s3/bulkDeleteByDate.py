from statistics import mode
import boto3
from datetime import datetime, timezone
import argparse
import re

parser = argparse.ArgumentParser(description='Remove objects from bucket, based on last modified date')
parser.add_argument('--mode', required=False, action='store', default="print", help='Mode [delete|rename|print]')
parser.add_argument('--bucket', required=True, action='store', help='Name of the bucket')
parser.add_argument('--prefix', required=True, action='store', help='Object name prefix')
parser.add_argument('--modified-before', required=True, action='store', help='Objects where created before this date ( %Y-%m-%d %H:%M:%S )')
parser.add_argument('--modified-after', required=True, action='store', help='Objects where created after this date ( %Y-%m-%d %H:%M:%S )')
parser.add_argument('--output', required=False, action='store', help='Optional file to write the deleted objects')
parser.add_argument('--stats', required=False, action='store_true', help='Print stats')

args = vars(parser.parse_args())

execMode = args["mode"]
bucket = args["bucket"]
namePrefix = args["prefix"]
modBefore = args["modified_before"]
modAfter  = args["modified_after"]
outputEnabled = False

s3 = boto3.client("s3")

paginator = s3.get_paginator("list_objects_v2")
paginator_params = {'Bucket': bucket, 'Prefix': namePrefix}
pages = paginator.paginate(**paginator_params)

if args["output"] != None:
    outputFile = open(args["output"], "a")
    outputEnabled = True

dateBefore = datetime.utcnow().strptime(modBefore, '%Y-%m-%d %H:%M:%S')
dateAfter = datetime.utcnow().strptime(modAfter, '%Y-%m-%d %H:%M:%S')

totalSize = 0
deletedSize = 0
deletedFiles = 0
processedFiles = 0
keysToDelete = []

for page in pages:
    for object in page["Contents"]:
        processedFiles += 1
        totalSize += object["Size"]
        if object["LastModified"] > dateAfter.replace(tzinfo=timezone.utc) and object["LastModified"] < dateBefore.replace(tzinfo=timezone.utc):
                if execMode == "delete":
                    s3.delete_objects(Bucket=bucket, Key=object["Key"])
                    if outputEnabled:
                        outputFile.write("{},{},{}\n".format(object["Key"], object["Size"], object["LastModified"]))
                    keysToDelete.append({"Key": object["Key"]})
                    deletedSize += object["Size"]
                    deletedFiles += 1
                elif execMode == "rename":
                    #print("{} > {}".format(object["Key"], object["Key"].replace(namePrefix, namePrefix + "backup/")))
                    s3.copy_object(
                        CopySource={'Bucket': bucket, 'Key': object["Key"]},
                        Bucket=bucket,
                        Key=object["Key"].replace(namePrefix, namePrefix + "backup/")
                    )
                    #s3.delete_object(Bucket=bucket, Key=object["Key"])
                    keysToDelete.append({"Key": object["Key"]})
                    deletedSize += object["Size"]
                    deletedFiles += 1

                    if outputEnabled:
                        outputFile.write("{}|{}\n".format(object["Key"], object["Key"].replace(namePrefix, namePrefix + "backup/")))
                else:
                    print("{}".format(object["Key"]))

        if len(keysToDelete) == 1000:
            s3.delete_objects(Bucket=bucket, Delete={"Objects": keysToDelete})

        if args["stats"] and processedFiles % 10000 == 0:
            print("Deleted files: {}/{} - Size {}/{}".format(deletedFiles, processedFiles, deletedSize, totalSize))

print("Total size: {} bytes", totalSize)
#s3.delete_objects(Bucket=bucket, Delete={"Objects": keysToDelete})

outputFile.close()

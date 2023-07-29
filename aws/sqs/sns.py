import boto3
import os
from time import sleep
from datetime import datetime

def sns_publish(topic_arn, message):
  response = sns.publish(
    TopicArn=topic_arn,
    Message=message
  )

# Read environment variable to check if localstack is running
localstack = os.environ.get('LOCALSTACK', 'true')
sqs_queue_name = os.environ.get('SQS_QUEUE_NAME', 'test-queue')
sns_topic_arn = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:eu-central-1:000000000000:test-topic')
endpoint_url = os.environ.get('ENDPOINT_URL', 'http://localhost:4566')

# Create Boto session and client using localstack endpoint
session = boto3.Session()
if localstack == 'true':
  print("Using localstack")
  sns = session.client('sns', endpoint_url=endpoint_url)
else:
  sns = session.client('sns')

# Create SNS topic
try:
    topic = sns.create_topic(Name='test-topic')
except sns.exceptions.TopicNameExists:
    print("Topic test-topic already exists")
else:
  print(topic['ResponseMetadata']['HTTPStatusCode'], topic['TopicArn'])

# Publish messages to the SNS topic
while True:
    
    # Get current date and time
    now = datetime.now()
    current_time = now.strftime("%Y%m%d:%H:%M:%S")

    # Publish a message to the SNS topic
    sns_publish(sns_topic_arn, "Hello world at " + current_time)

    # Sleep for 5 seconds
    sleep(1)

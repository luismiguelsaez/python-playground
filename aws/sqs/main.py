import boto3
import os
from time import sleep

def sns_publish(topic_arn, message):
  response = sns.publish(
    TopicArn=topic_arn,
    Message=message
  )

def sqs_read(queue_url):
  response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=1,
    WaitTimeSeconds=5
  )

  # Print the message body
  if 'Messages' in response:
    message = response['Messages'][0]['Body']
    print(message)
    # Delete the message
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=response['Messages'][0]['ReceiptHandle']
    )
  else:
    print("No messages in queue")

# Read environment variable to check if localstack is running
localstack = os.environ.get('LOCALSTACK')
sqs_queue_name = os.environ.get('SQS_QUEUE_NAME', 'test-queue')
sns_topic_arn = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:eu-central-1:000000000000:test-topic')

# Create Boto session and client using localstack endpoint
session = boto3.Session()
if localstack == 'true':
  print("Using localstack")
  sqs = session.client('sqs', endpoint_url='http://localhost:4566')
  sns = session.client('sns', endpoint_url='http://localhost:4566')
else:
  sqs = session.client('sqs')
  sns = session.client('sns')

# Create SQS queue
try:
    queue = sqs.create_queue(QueueName=sqs_queue_name)
except sqs.exceptions.QueueNameExists:
    print(f"Queue {sqs_queue_name} already exists")
else:
  print(queue['ResponseMetadata']['HTTPStatusCode'], queue['QueueUrl'])

# Create SNS topic
try:
    topic = sns.create_topic(Name='test-topic')
except sns.exceptions.TopicNameExists:
    print("Topic test-topic already exists")
else:
  print(topic['ResponseMetadata']['HTTPStatusCode'], topic['TopicArn'])

# Subscribe the queue to the SNS topic
queue_arn = sqs.get_queue_attributes(
    QueueUrl=queue['QueueUrl'],
    AttributeNames=['QueueArn']
)['Attributes']['QueueArn']

print(f"Subscribing {queue_arn} to {sns_topic_arn}")
subscription = sns.subscribe(
    TopicArn=sns_topic_arn,
    Protocol='sqs',
    Endpoint=queue_arn
)

# Poll the queue for messages
while True:
    
    # Publish a message to the SNS topic
    sns_publish(sns_topic_arn, "Hello world!")

    # Read the message from the queue
    sqs_read(queue['QueueUrl'])

    # Sleep for 5 seconds
    sleep(1)

import boto3
import json

def get_latest_logs(log_group_name):
    session = boto3.session.Session(profile_name='lokalise-admin-live')
    client = session.client('logs', region_name='eu-central-1')

    # Get list of log streams
    streams = client.describe_log_streams(
        logGroupName=log_group_name,
        #logStreamNamePrefix='kube-apiserver-audit',
        orderBy='LastEventTime',
        descending=True
    )

    # Get the name of the latest log stream
    latest_stream_name = streams['logStreams'][0]['logStreamName']

    # Get the logs from the latest log stream
    response = client.filter_log_events(
        logGroupName=log_group_name,
        logStreamNames=[latest_stream_name],
        limit=10,
        #filterPattern='ERROR'
    )

    events = response['events']
    for event in events:
        #print(f"{event['message']} at {event['timestamp']}")
        print(event['message'])

# Use the name of your log group
log_group_name = '/aws/eks/live-lok-k8s-main/cluster'
get_latest_logs(log_group_name)

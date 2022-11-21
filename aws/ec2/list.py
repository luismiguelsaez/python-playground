import boto3

s = boto3.Session()
c = s.client('ec2')
instances = c.describe_instances()

for i in instances['Reservations']:
  instance = i['Instances'][0]
  name = list(filter(lambda x: x['Key'] == 'Name', instance['Tags']))[0]['Value']
  print(instance['InstanceId'], name, instance['InstanceType'], instance['PrivateIpAddress'])

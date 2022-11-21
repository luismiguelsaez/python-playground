import boto3

s = boto3.Session()
c = s.client('ec2')
instances = c.describe_instances()

for i in instances['Reservations']:
  id = i['ReservationId']
  c = 1
  for instance in i['Instances']:
    name = list(filter(lambda x: x['Key'] == 'Name', instance['Tags']))[0]['Value']
    print("{}[{}]\t{}\t{}\t{}\t{}".format(id, c, instance['InstanceId'], instance['InstanceType'], instance['PrivateIpAddress'], name))
    c += 1

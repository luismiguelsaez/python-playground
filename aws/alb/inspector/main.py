import boto3
from os import environ as env

def main():
  # Get profile name from env
  profile = env.get('AWS_PROFILE','lokalise-admin-stage')

  # Create session
  session = boto3.Session(profile_name=profile)

  # Create elbv2 client
  elb = session.client('elbv2')

  elbs = [ elb['LoadBalancerArn'] for elb in elb.describe_load_balancers()['LoadBalancers'] ]

  # Iterate over elbs and get all target groups
  for e in elbs:
    target_groups = [ tg['TargetGroupArn'] for tg in elb.describe_target_groups(LoadBalancerArn=e)['TargetGroups'] ]
    for tg in target_groups:
      # Get all targets in target group
      targets = elb.describe_target_health(TargetGroupArn=tg)['TargetHealthDescriptions']
      for t in targets:
        # Get target id
        target_id = t['Target']['Id']
        # Get target health
        target_health = t['TargetHealth']['State']
        # Print target id and health
        print(f'{e} - {target_id} - {target_health}')

if __name__ == "__main__":
  main()

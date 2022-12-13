import boto3
from json import dumps as json_dumps
import argparse

# Parse arguments
parser = argparse.ArgumentParser(prog="maintenance.py", description="Set maintenance page in Application ALB")
parser.add_argument('-a', '--action',    action='store', choices=['update', 'delete'], required=True)
parser.add_argument('-c', '--component', action='store', choices=['app', 'api'], required=True)
parser.add_argument('-t', '--time',      action='store', required=False)
parser.add_argument('--lb-name',                   action='store', default=None, required=False)
parser.add_argument('--lb-region',                 action='store', default='eu-central-1', required=False)
parser.add_argument('--lb-listener-port',          action='store', default=443, required=False)
parser.add_argument('--lb-listener-rule-priority', action='store', default=1, required=False)
parser.add_argument('--lb-listener-rule-path',     action='store', default='/', required=False)
parser.add_argument('--content-base',              action='store', default='https://lokalise-stage-lok-app-main-assets.s3.eu-central-1.amazonaws.com', required=False)
group = parser.add_mutually_exclusive_group()
group.add_argument('-r', '--iam-role', action='store', required=False)
group.add_argument('-p', '--profile',  action='store', required=False)
args = parser.parse_args()

# Default messages
html_content_title = "We're under maintenance right now!"
html_content_custom_message_1 = "We're under maintenance right now!"

if args.time == None:
  html_content_custom_message_2 = "Sorry for the inconvenience! We're working on improving our system and expect to be back online soon."
  json_content_custom_message = f"Down for maintenance, expect to be back soon."
else:
  html_content_custom_message_2 = f"Sorry for the inconvenience! We're working on improving our system and expect to be back online by { args.time } UTC."
  json_content_custom_message = f"Down for maintenance, expect to be back by { args.time } UTC"

html_body = f"""
<html>
  <head>
    <title>{ html_content_title }</title>
    <meta content="{ html_content_title }" name=description>
    <link href="{ args.content_base }/error_static/css/main.css" rel=stylesheet>
  </head>
  <body>
    <div class=wrapper><div class=logo>
      <a href="{ args.content_base }">
        <picture width=100%>
          <source srcset="{ args.content_base }/error_static/img/logo.svg 2x">
          <img srcset="{ args.content_base }/error_static/img/logo.png">
        </picture>
      </a>
    </div>
    <div class=content>
      <picture>
        <img srcset="{ args.content_base }/error_static/img/error.png" id=main-pic>
      </picture>
      <h1>{ html_content_custom_message_1 }</h1>
      <p id=description>{ html_content_custom_message_2 }
    </div>
  </body>
</html>
"""

html_body_compact = ''.join(map(str.strip, html_body.splitlines()))
json_body = {"code": 503,"message": json_content_custom_message}

if args.lb_name == None:
  lb_name = f"lok-{args.component}-main"
else:
  lb_name = args.lb_name

if args.component == "app":
  message = html_body_compact
  content_type = "text/html"
else:
  message = json_dumps(json_body)
  content_type = "application/json"

message_size = len(message)
if message_size > 1024:
  raise ValueError(f"HTML code size greater than the limit of 1024 [{ message_size }]")

if args.iam_role != None:
  client = boto3.client('sts')
  creds = client.assume_role(RoleArn=args.iam_role, RoleSessionName='appMaintenance')
  s = boto3.Session(
      aws_access_key_id=creds['Credentials']['AccessKeyId'],
      aws_secret_access_key=creds['Credentials']['SecretAccessKey'],
      aws_session_token=creds['Credentials']['SessionToken'],
      region_name=args.lb_region)
elif args.profile != None:
  s = boto3.Session(profile_name=args.profile)
else:
  raise ValueError(f"You need to specify either an IAM role or AWS local profile")


c = s.client("elbv2")

lbs = c.describe_load_balancers()
lb = [l for l in lbs['LoadBalancers'] if l['LoadBalancerName'] == lb_name]
#lb = list(filter(lambda x:x['LoadBalancerName'] == lb_name, lbs['LoadBalancers']))

if not lb:
  raise ValueError(f"Load-balancer [{lb_name}] not found")
elif len(lb) > 1:
  raise ValueError(f"Found more that one load-balancer with the given name [{len(lb)}]")

listeners = c.describe_listeners(LoadBalancerArn=lb[0]['LoadBalancerArn'])
listener = [l for l in listeners['Listeners'] if l['Port'] == args.lb_listener_port]
#listener = list(filter(lambda x:x['Port'] == args.lb_listener_port, listeners['Listeners']))

if len(listener) < 1:
  raise ValueError(f"Listener with port [{str(args.lb_listener_port)}] not found")

listener_rules = c.describe_rules(ListenerArn=listener[0]['ListenerArn'])
listener_rule_exists = list(filter(lambda x:x['Priority'] in (str(args.lb_listener_rule_priority), str(args.lb_listener_rule_priority + 1) ), listener_rules['Rules']))

# Get target-group ARN from default rule
default_rule = [r for r in listener_rules['Rules'] if r['Priority'] == 'default']
if default_rule:
  forward_action = [a for a in default_rule[0]['Actions'] if a['Type'] == 'forward']
  if not forward_action:
    raise ValueError(f"Default rule hasn't any forward action, unable to get the target-group")
  else:
    target_group_arn = forward_action[0]['TargetGroupArn']


if args.action == "update":
  if len(listener_rule_exists) < 2:
    res_1 = c.create_rule(
      ListenerArn=listener[0]['ListenerArn'],
      Conditions=[
        {
          'Field': 'path-pattern',
          'PathPatternConfig': {
            'Values': [
                f"{args.lb_listener_rule_path}*"
            ]
          }
        },
        {
          'Field': 'http-header',
          'HttpHeaderConfig': {
            'HttpHeaderName': 'Cookie',
            'Values': [
                '*look_behind_the_curtain=true*'
            ]
          }
        }
      ],
      Priority=args.lb_listener_rule_priority,
      Actions=[{
        'Type': 'forward',
        'TargetGroupArn': target_group_arn
      }]
    )
    res_2 = c.create_rule(
      ListenerArn=listener[0]['ListenerArn'],
      Conditions=[
        {
          'Field': 'path-pattern',
          'PathPatternConfig': {
            'Values': [
                f"{args.lb_listener_rule_path}*"
            ]
          }
        }
      ],
      Priority=args.lb_listener_rule_priority + 1,
      Actions=[{
        'Type': 'fixed-response',
        'FixedResponseConfig': {
          'MessageBody': message,
          'StatusCode': '503',
          'ContentType': content_type
        }
      }]
    )
  else:
    res_1 = c.modify_rule(
      RuleArn=listener_rule_exists[0]['RuleArn'],
      Conditions=[
        {
          'Field': 'path-pattern',
          'PathPatternConfig': {
            'Values': [
                f"{args.lb_listener_rule_path}*"
            ]
          }
        },
        {
          'Field': 'http-header',
          'HttpHeaderConfig': {
            'HttpHeaderName': 'Cookie',
            'Values': [
                '*look_behind_the_curtain=true*'
            ]
          }
        }
      ],
      Actions=[{
        'Type': 'forward',
        'TargetGroupArn': target_group_arn
      }]
    )
    res_2 = c.modify_rule(
      RuleArn=listener_rule_exists[1]['RuleArn'],
      Conditions=[
        {
          'Field': 'path-pattern',
          'PathPatternConfig': {
            'Values': [
                f"{args.lb_listener_rule_path}*"
            ]
          }
        }
      ],
      Actions=[{
        'Type': 'fixed-response',
        'FixedResponseConfig': {
          'MessageBody': message,
          'StatusCode': '503',
          'ContentType': content_type
        }
      }]
    )
elif args.action == "delete":
  if listener_rule_exists and len(listener_rule_exists) > 0:
    for rule in listener_rule_exists:
      res = c.delete_rule(RuleArn=rule['RuleArn'])
  else:
    raise ValueError(f"No rules to delete")
else:
  raise ValueError(f"Action [{args.action}] not valid")

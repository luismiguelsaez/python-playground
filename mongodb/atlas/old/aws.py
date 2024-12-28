import boto3
import botocore
import json

def get_session_with_profile(profile_name: str) -> boto3.Session:
    return boto3.Session(profile_name=profile_name)

def get_parameter_by_path(path: str, aws_profile: str = "maroot") -> tuple[bool, str]:
    session = get_session_with_profile(aws_profile)
    ssm_client = session.client("ssm")
    ssm_res = ssm_client.get_parameter(Name=path, WithDecryption=True)
    if ssm_res["ResponseMetadata"]["HTTPStatusCode"] != 200:
        return False, ssm_res["ResponseMetadata"]
    return True, ssm_res["Parameter"]["Value"]

def create_s3_bucket(bucket_name: str, role_arn: str, region: str, aws_profile: str = "maroot") -> tuple[bool, str]:
    session = get_session_with_profile(aws_profile)
    s3_client = session.client("s3")

    s3_list = s3_client.list_buckets()
    for b in s3_list["Buckets"]:
        if b["Name"] == bucket_name:
            return True, b["Name"]

    s3_create = s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": region})
    if s3_create["ResponseMetadata"]["HTTPStatusCode"] != 200:
        return False, s3_create["ResponseMetadata"]

    s3_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": role_arn
                },
                "Action": [
                    "s3:ListBucket",
                    "s3:GetObject",
                    "s3:GetObjectVersion",
                    "s3:GetBucketLocation",
                    "s3:PutObject"
                ],
                "Resource": [
                    f"arn:aws:s3:::{bucket_name}/*"
                ]
            }
        ]
    }

    s3_put_policy = s3_client.put_bucket_policy(
        Bucket=bucket_name,
        Policy=json.dumps(s3_policy)
    )

    if s3_put_policy["ResponseMetadata"]["HTTPStatusCode"] != 204:
        return False, s3_put_policy["ResponseMetadata"]

    return True, bucket_name


def create_iam_role(role_name: str, trust_policy: dict, policy: dict, aws_profile: str = "maroot") -> tuple[bool, str]:
    session = get_session_with_profile(aws_profile)
    iam_client = session.client("iam")
    policy_arn = ""

    policies = iam_client.list_policies()
    for p in policies["Policies"]:
        if p["PolicyName"] == role_name:
            policy_arn = p["Arn"]
            break
    if policy_arn == "":
        policy = iam_client.create_policy(
            PolicyName=role_name,
            PolicyDocument=json.dumps(policy)
        )
        policy_arn = policy["Policy"]["Arn"]

    try:
        iam_res = iam_client.get_role(RoleName=role_name)
        return True, iam_res["Role"]["Arn"]
    except botocore.exceptions.ClientError as e:
        pass

    iam_res = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(trust_policy)
    )
    if iam_res["ResponseMetadata"]["HTTPStatusCode"] != 200:
        return False, iam_res["ResponseMetadata"]
    else:
        iam_res_attach = iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
        if iam_res_attach["ResponseMetadata"]["HTTPStatusCode"] != 200:
            return False, iam_res["ResponseMetadata"]

    return True, iam_res["Role"]["Arn"]
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

def create_iam_role(role_name: str, trust_policy: str, aws_profile: str = "maroot") -> tuple[bool, str]:
    session = get_session_with_profile(aws_profile)
    iam_client = session.client("iam")

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
    return True, iam_res["Role"]["Arn"]
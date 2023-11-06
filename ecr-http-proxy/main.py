import boto3
import requests
from fastapi import FastAPI, Request
from fastapi.responses import Response
from os import environ
from datetime import datetime
from pytz import timezone
import logging
from sys import stdout

aws_access_key_id = environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = environ.get('AWS_SECRET_ACCESS_KEY')
aws_account_id = environ.get('AWS_ACCOUNT_ID')
aws_region = environ.get('AWS_REGION')
logger_level = environ.get('LOG_LEVEL', 'INFO')

UPSTREAM_HOST = f'{aws_account_id}.dkr.ecr.{aws_region}.amazonaws.com'
UPSTREAM_PROTO = 'https'

logger = logging.getLogger(__name__)
logger.setLevel(logger_level)
logger.addHandler(logging.StreamHandler(stdout))

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

def get_ecr_token():
    
    client = session.client('ecr')

    auth = client.get_authorization_token()
    token = auth['authorizationData'][0]['authorizationToken']
    token_expiration = auth['authorizationData'][0]['expiresAt']
    
    return token, token_expiration

ecr_token, ecr_token_expiration = get_ecr_token()

app = FastAPI()

@app.api_route('/v2/{registry_path:path}', methods=['GET', 'HEAD'])
def registry_get(registry_path: str, request: Request, ecr_token=ecr_token, ecr_token_expiration=ecr_token_expiration):
    
    ecr_token_expiration_offset_aware = ecr_token_expiration.replace(tzinfo=timezone('UTC'))
    current_date = datetime.now(tz=timezone('UTC'))
    if ecr_token_expiration_offset_aware < current_date:
        logger.info(f"ECR token expired ({ecr_token_expiration_offset_aware} < {current_date}), getting new token")
        ecr_token, ecr_token_expiration = get_ecr_token()
    else:
        logger.debug(f"ECR token is still valid ({ecr_token_expiration_offset_aware} > {current_date})")

    upstream_request_headers = {}
    upstream_request_headers['Authorization'] = 'Basic ' + ecr_token
    upstream_request_headers['X-Forwarded-User'] = 'Basic ' + ecr_token
    upstream_request_headers['X-Real-IP'] = request.client.host
    upstream_request_headers['X-Forwarded-For'] = request.client.host
    upstream_request_headers['X-Forwarded-Proto'] = request.url.scheme

    upstream_response = requests.request(
        method=request.method,
        url=f'{UPSTREAM_PROTO}://{UPSTREAM_HOST}/v2/{registry_path}',
        headers=upstream_request_headers
    )
    
    if upstream_response.status_code == 200:
        logger.debug(f"Upstream response valid [{upstream_response.status_code}]")
    else:
        logger.error(f"Upstream response invalid [{upstream_response.status_code}]: {upstream_response.content}")

    return Response(status_code=upstream_response.status_code, content=upstream_response.content, headers=upstream_response.headers)

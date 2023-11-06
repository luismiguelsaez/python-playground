import boto3
import requests
from fastapi import FastAPI, Request
from fastapi.responses import Response
from os import environ
from datetime import datetime
from pytz import timezone

aws_access_key_id = environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = environ.get('AWS_SECRET_ACCESS_KEY')
aws_account_id = environ.get('AWS_ACCOUNT_ID')
aws_region = environ.get('AWS_REGION')

UPSTREAM_HOST = f'{aws_account_id}.dkr.ecr.{aws_region}.amazonaws.com'
UPSTREAM_PROTO = 'https'

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
    if ecr_token_expiration_offset_aware < datetime.now(tz=timezone('UTC')):
        ecr_token, ecr_token_expiration = get_ecr_token()

    print("Original request headers: ", request.headers)

    upstream_request_headers = {}
    upstream_request_headers['Authorization'] = 'Basic ' + ecr_token
    upstream_request_headers['X-Forwarded-User'] = 'Basic ' + ecr_token
    upstream_request_headers['X-Real-IP'] = request.client.host
    upstream_request_headers['X-Forwarded-For'] = request.client.host
    upstream_request_headers['X-Forwarded-Proto'] = request.url.scheme

    print("Upstream request headers: ", upstream_request_headers)

    upstream_response = requests.request(
        method=request.method,
        url=f'{UPSTREAM_PROTO}://{UPSTREAM_HOST}/v2/{registry_path}',
        headers=upstream_request_headers
    )

    print("Upstream response headers: ", upstream_response.headers)

    return Response(status_code=upstream_response.status_code, content=upstream_response.content, headers=upstream_response.headers)

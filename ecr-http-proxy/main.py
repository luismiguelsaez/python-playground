import os
import boto3
import requests
from fastapi import FastAPI, Request
from fastapi.responses import Response, StreamingResponse
from os import environ, remove, path
from datetime import datetime
from pytz import timezone
import logging
from sys import stdout

aws_access_key_id = environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = environ.get('AWS_SECRET_ACCESS_KEY')
aws_account_id = environ.get('AWS_ACCOUNT_ID')
aws_region = environ.get('AWS_REGION')
buffer_path = environ.get('BUFFER_PATH', '/tmp/')
logger_level = environ.get('LOG_LEVEL', 'INFO')

UPSTREAM_HOST = f'{aws_account_id}.dkr.ecr.{aws_region}.amazonaws.com'
UPSTREAM_PROTO = 'https'

logger = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(stdout)
stdout_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(stdout_formatter)
logger.setLevel(logger_level)
logger.addHandler(stdout_handler)

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

@app.api_route('/v2/{registry_path:path}', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
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

    logger.info(f"Upstream request: [{UPSTREAM_PROTO}://{UPSTREAM_HOST}] - {request.method} - /v2/{registry_path}")

    try:
        response = requests.request(
            method=request.method,
            url=f'{UPSTREAM_PROTO}://{UPSTREAM_HOST}/v2/{registry_path}',
            headers=upstream_request_headers,
            stream=True,
            verify=True
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Upstream request failed: [{UPSTREAM_PROTO}://{UPSTREAM_HOST}] - {request.method} - /v2/{registry_path}: {e}")
    except Exception as e:
        logger.error(f"General exception during upstream request: [{UPSTREAM_PROTO}://{UPSTREAM_HOST}] - {request.method} - /v2/{registry_path}: {e}")

    logger.info(f"Upstream response: [{UPSTREAM_PROTO}://{UPSTREAM_HOST}] - {response.status_code} - /v2/{registry_path}")

    def generate_content_stream():
        for chunk in response.iter_content(chunk_size=8192):
            yield chunk

    logger.debug(f"Streaming response to the client: [{request.client.host}] - {response.status_code} - /v2/{registry_path}")

    try:
        return StreamingResponse(
            status_code=response.status_code,
            content=generate_content_stream(),
            headers=response.headers
        )
    except Exception as e:
        logger.error(f"Error streaming response to client: [{request.client.host}] - {response.status_code} - /v2/{registry_path}: {e}")

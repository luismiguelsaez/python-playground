import os
import boto3
import requests
from fastapi import FastAPI, Request
from fastapi.responses import Response
from os import environ, remove, path
from datetime import datetime
from pytz import timezone
import logging
from sys import stdout
import hashlib
from random import randint

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

    logger.info(f"Upstream request: [{UPSTREAM_PROTO}://{UPSTREAM_HOST}] - {request.method} - /v2/{registry_path}")

    file_hash = hashlib.sha256()
    file_hash.update(str.encode(request.client.host))
    file_hash.update(str.encode(registry_path))
    file_hash.update(str.encode(request.method))
    file_hash.update(str(randint(0,10000000)).encode())
    file_name = file_hash.hexdigest()

    logger.info(f"Writing upstream response to file: {buffer_path}{file_name}")

    # Store response to disk
    try:
        with requests.request(method=request.method, url=f'{UPSTREAM_PROTO}://{UPSTREAM_HOST}/v2/{registry_path}', headers=upstream_request_headers, stream=True) as r:
            r.raise_for_status()
            with open(f"{buffer_path}{file_name}", 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    bytes=f.write(chunk)
    except Exception as e:
        logger.error(f"Error writing file: {buffer_path}{file_name}: {e}")

    #upstream_response = requests.request(
    #    method=request.method,
    #    url=f'{UPSTREAM_PROTO}://{UPSTREAM_HOST}/v2/{registry_path}',
    #    headers=upstream_request_headers
    #)

    #if upstream_response.status_code == 200:
    #    logger.debug(f"Upstream response valid [{upstream_response.status_code}]")
    #else:
    #    logger.error(f"Upstream response invalid [{upstream_response.status_code}]: {upstream_response.content}")

    logger.info(f"Reading client response from file: {buffer_path}{file_name}")

    # Retrieve response from disk
    try:
        with open(f"{buffer_path}{file_name}", 'rb') as f:
            file_content = f.read()
            if os.path.exists(f"{buffer_path}{file_name}"):
                logger.info(f"Removing file from disk: {buffer_path}{file_name}")
                remove(f"{buffer_path}{file_name}")
            else:
                logger.error(f"File not found: {buffer_path}{file_name}")
    except Exception as e:
        logger.error(f"Error reading file: {buffer_path}{file_name}: {e}")

    #return Response(status_code=upstream_response.status_code, content=upstream_response.content, headers=upstream_response.headers)
    return Response(status_code=r.status_code, content=file_content, headers=r.headers)

from sys import exit
from aws import (
    get_parameter_by_path,
    create_iam_role,
    create_s3_bucket
)
from atlas import (
    get_app_id,
    get_appservices_token,
    create_function,
    create_trigger,
    get_function_source_database,
    get_function_source_scheduled,
    create_data_federation_s3,
    get_service_id,
    get_function_id,
    create_application_datasource_links,
    create_app,
    create_cloud_provider_access_role,
    authorize_cloud_provider_access_role,
)
from prod import (
    triggers,
    functions,
    AWS_PROFILE,
    AWS_S3_BUCKET_NAME,
    AWS_REGION,
    AWS_SSM_PREFIX,
    MONGO_ATLAS_ORG_ID,
    MONGO_ATLAS_PROJECT_ID,
    MONGO_ATLAS_FEDERATION_NAME,
    MONGO_ATLAS_FEDERATED_DB_NAME,
)
import logging
import sys

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

privkey_res, privkey_out = get_parameter_by_path(path=f"{AWS_SSM_PREFIX}private-key", aws_profile=AWS_PROFILE)
pubkey_res, pubkey_out = get_parameter_by_path(path=f"{AWS_SSM_PREFIX}public-key", aws_profile=AWS_PROFILE)

if not privkey_res or not pubkey_res:
    print(f"Error getting AWS parameter store information")
    exit(1)
else:
    mdb_private_key = privkey_out
    mdb_public_key = pubkey_out

# Create cloud provider access role
res_access_role, output_access_role = create_cloud_provider_access_role(
    mdb_public_key=mdb_public_key,
    mdb_private_key=mdb_private_key,
    project_id=MONGO_ATLAS_PROJECT_ID,
)

if not res_access_role:
    logger.error(f"Error creating cloud provider access role: {output_access_role}")
    exit(1)
else:
    logger.info(f"Cloud provider access role created: {output_access_role}")
    external_id = output_access_role["external_id"]
    atlas_account_arn = output_access_role["atlas_account_arn"]

    aws_iam_role_trust_policy = {
        "Version":"2012-10-17",
        "Statement":[
            {
                "Effect":"Allow",
                "Principal":{
                    "AWS": atlas_account_arn
                },
                "Action":"sts:AssumeRole",
                "Condition":{
                    "StringEquals":{
                    "sts:ExternalId": external_id
                    }
                }
            }
        ]
    }

    aws_iam_role_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket",
                    "s3:GetObject",
                    "s3:GetObjectVersion",
                    "s3:GetBucketLocation",
                    "s3:PutObject"
                ],
                "Resource": [
                    f"arn:aws:s3:::{AWS_S3_BUCKET_NAME}",
                    f"arn:aws:s3:::{AWS_S3_BUCKET_NAME}/*"
                ]
            }
        ]
    }

res_create_role, output_create_role = create_iam_role(
    role_name="mongodb-atlas-dwh",
    trust_policy=aws_iam_role_trust_policy,
    aws_profile=AWS_PROFILE,
    policy=aws_iam_role_policy
)

if not res_create_role:
    logger.error(f"Error creating IAM role: {output_create_role}")
    exit(1)
else:
    logger.info(f"IAM role created: {output_create_role} - {output_access_role}")

logger.info(f"Authorizing IAM role: {output_create_role}")
res_authorize_role, output_authorize_role = authorize_cloud_provider_access_role(
    mdb_public_key=mdb_public_key,
    mdb_private_key=mdb_private_key,
    project_id=MONGO_ATLAS_PROJECT_ID,
    role_id=output_access_role["role_id"],
    role_arn=output_create_role
)

if not res_authorize_role:
    logger.error(f"Error authorizing IAM role: {output_authorize_role}")
    exit(1)
else:
    logger.info(f"IAM role authorized: {output_authorize_role}")

# Create S3 bucket
res_create_bucket, output_create_bucket = create_s3_bucket(
    bucket_name=AWS_S3_BUCKET_NAME,
    region=AWS_REGION,
    role_arn=output_create_role,
    aws_profile=AWS_PROFILE
)

if not res_create_bucket:
    logger.error(f"Error creating S3 bucket: {output_create_bucket}")
    exit(1)
else:
    logger.info(f"S3 bucket created: {output_create_bucket}")

# Create data federation
res_data_federation, output_data_federation = create_data_federation_s3(
    name=MONGO_ATLAS_FEDERATION_NAME,
    database_name=MONGO_ATLAS_FEDERATED_DB_NAME,
    project_id=MONGO_ATLAS_PROJECT_ID,
    mdb_public_key=mdb_public_key,
    mdb_private_key=mdb_private_key,
    aws_access_role_id=output_access_role["role_id"],
    aws_bucket_name=AWS_S3_BUCKET_NAME,
    aws_bucket_prefix="",
    aws_region=AWS_REGION
)

if not res_data_federation:
    logger.error(f"Error creating data federation: {output_data_federation}")
    exit(1)
else:
    logger.info(f"Data federation created: {output_data_federation}")

# Get appservices token
res, token = get_appservices_token(public_key=mdb_public_key, private_key=mdb_private_key)
if res:
    mdb_appservices_token = token
else:
    logger.error(f"Error getting appservices token: {token}")
    exit(1)

# Get triggers app ID
res, id = get_app_id(token=mdb_appservices_token, project_id=MONGO_ATLAS_PROJECT_ID, name="Triggers")
if res:
    mdb_appservices_triggers_app_id = id
else:
    # Create triggers app
    res, app_id = create_app(
            token=mdb_appservices_token,
            project_id=MONGO_ATLAS_PROJECT_ID,
            name="Trigers",
            federated_db_name=output_data_federation,
    )
    if res:
        mdb_appservices_triggers_app_id = app_id
    else:
        logger.error(f"Error creating app: {app_id}")
        exit(1)

exit(0)
# Link data sources
#res, output = create_application_datasource_links(
#    token=mdb_appservices_token,
#    project_id=MONGO_ATLAS_PROJECT_ID,
#    name=f"federated-{MONGO_ATLAS_FEDERATION_NAME}",
#    cluster_name=MONGO_ATLAS_FEDERATION_NAME,
#    app_id=mdb_appservices_triggers_app_id
#)
#if not res:
#    logger.error(f"Error creating application datasource link: {output}")
#    exit(1)
#else:
#    logger.info(f"Application datasource link created: {output}")

# Create appservices functions
for function in functions:
    if functions[function]["type"] == "DATABASE":
        source = get_function_source_database(
            service_name=functions[function]["service_name"],
            federated_db_name=functions[function]["federated_db_name"],
            federated_collection_name=functions[function]["federated_collection_name"]
        )
    elif functions[function]["type"] == "SCHEDULED":
        source = get_function_source_scheduled(
            federation_name=functions[function]["federation_name"],
            federated_database_name=functions[function]["federated_database_name"],
            federated_collection_name=functions[function]["federated_collection_name"],
            s3_bucket_name=AWS_S3_BUCKET_NAME,
            s3_bucket_region=AWS_REGION
        )

    res, output = create_function(
        token=mdb_appservices_token,
        project_id=MONGO_ATLAS_PROJECT_ID,
        name=function,
        app_id=mdb_appservices_triggers_app_id,
        source=source
    )

    if not res:
        logger.error(f"Error creating function {function}: {output}")
        exit(1)
    else:
        logger.info(f"Function {function} created: {output}")

# Create appservices triggers
for trigger in triggers:
    if triggers[trigger]["type"] == "DATABASE":
        res_service, output_service = get_service_id(token=mdb_appservices_token, project_id=MONGO_ATLAS_PROJECT_ID, app_id=mdb_appservices_triggers_app_id, name=triggers[trigger]["source"])
        if not res_service:
            logger.error(f"Error getting service ID: {output}")
            pass

    res_function, output_function = get_function_id(
        token=mdb_appservices_token, project_id=MONGO_ATLAS_PROJECT_ID, app_id=mdb_appservices_triggers_app_id, name=triggers[trigger]["function_name"]
    )
    if not res_function:
        logger.error(f"Error getting function ID: {output_function}")
        pass

    logger.info(f"Creating trigger {trigger}. function_id: {output_function}, service_id: {output_service}")

    if triggers[trigger]["type"] == "DATABASE":
        res_trigger, output_trigger = create_trigger(token=mdb_appservices_token,
                        project_id=MONGO_ATLAS_PROJECT_ID,
                        app_id=mdb_appservices_triggers_app_id,
                        name=triggers[trigger]["name"],
                        database=triggers[trigger]["database"],
                        collection=triggers[trigger]["collection"],
                        service_id=output_service,
                        function_id=output_function,
                        trigger_type="DATABASE",
                        op_types=triggers[trigger]["op_types"],
        )
    elif triggers[trigger]["type"] == "SCHEDULED":
        res_trigger, output_trigger = create_trigger(token=mdb_appservices_token,
                        project_id=MONGO_ATLAS_PROJECT_ID,
                        app_id=mdb_appservices_triggers_app_id,
                        name=triggers[trigger]["name"],
                        function_id=output_function,
                        trigger_type="SCHEDULED",
                        schedule=triggers[trigger]["schedule"],
        )

    if not res_trigger:
        logger.error(f"Error creating trigger '{trigger}': {output_trigger}")
    else:
        logger.info(f"Created trigger '{trigger}': {output_trigger}")
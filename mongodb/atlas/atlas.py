# API appservices: https://www.mongodb.com/docs/atlas/app-services/admin/api/v3
# API admin: https://www.mongodb.com/docs/atlas/reference/api-resources-spec/v2

import requests
from requests.auth import HTTPDigestAuth

MONGO_ATLAS_API_URL = "https://cloud.mongodb.com/api/atlas/v2"
MONGO_ATLAS_API_VERSION = "application/vnd.atlas.2024-11-13+json"
MONGO_ATLAS_APPSERVICES_API_URL = "https://services.cloud.mongodb.com/api/admin/v3.0"

def get_function_source_database(service_name: str, federated_db_name: str, federated_collection_name: str = "")-> str:
    source = f"""
        exports = async function(changeEvent) {{
            // Check if changeEvent is undefined
            if (!changeEvent || changeEvent["$undefined"]) {{
                console.log("Error: changeEvent is undefined.");
                return; // Exit if changeEvent is not defined
            }}

            // Access the _id of the changed document
            const docId = changeEvent.documentKey._id;

            // Specify your service name (your MongoDB cluster)
            const serviceName = "{service_name}"; 
            const federatedDbName = "{federated_db_name}";
            const federatedCollectionName = "{federated_collection_name}";

            // Log service and database details
            console.log(`Connecting to service: ${{serviceName}}`);
            console.log(`Targeting federated database: ${{federatedDbName}}`);
            console.log(`Targeting federated collection: ${{federatedCollectionName}}`);

            const federatedDb = context.services.get(serviceName).db(federatedDbName);
            const federatedCollection = federatedDb.collection(federatedCollectionName);
            
            try {{
                // Handle insert operation
                if (changeEvent.operationType === "insert") {{
                console.log("Upserting document:", JSON.stringify(changeEvent.fullDocument));
                await federatedCollection.updateOne(
                    {{ _id: docId }}, // Filter to find the document
                    {{ $set: changeEvent.fullDocument }}, // Set the fields to the latest data
                    {{ upsert: true }} // Insert if the document doesn't exist
                );
                }}
                // Handle update or replace operation
                else if (changeEvent.operationType === "update" || changeEvent.operationType === "replace") {{
                    console.log("Upserting updated document:", JSON.stringify(changeEvent.fullDocument));
                    await federatedCollection.updateOne(
                        {{ _id: docId }}, // Filter to find the document
                        {{ $set: changeEvent.fullDocument }}, // Update the document with the latest data
                        {{ upsert: true }} // Insert if the document doesn't exist
                    );
                }}
                // Handle delete operation
                else if (changeEvent.operationType === "delete") {{
                    console.log("Document deleted with _id:", docId);
                    await federatedCollection.updateOne(
                        {{ _id: docId }}, // Filter to find the document
                        {{ $set: {{ deleted: true }} }}, // Mark as deleted
                        {{ upsert: true }} // Insert if the document doesn't exist
                    );
                }}
            }} catch (err) {{
                console.log("Error performing operation: ", err.message);
            }}
        }};
    """
    return source


def get_function_source_scheduled(federation_name: str, federated_database_name: str, federated_collection_name: str, s3_bucket_name: str, s3_bucket_region: str)-> str:
    source = f"""
        exports = async function () {{
            const service = context.services.get("{federation_name}");
            const db = service.db("{federated_database_name}");
            const invoices = db.collection("{federated_collection_name}");
            const now = new Date();
            const datePart = `${{(now.getMonth() + 1).toString().padStart(2, '0')}}-${{now.getDate().toString().padStart(2, '0')}}-${{now.getFullYear()}}`;
            const hourPart = `${{now.getHours().toString().padStart(2, '0')}}-${{now.getMinutes().toString().padStart(2, '0')}}`;


            console.log("Starting export:", Date.now());
            const pipeline = [
                {{
                    $match: {{
                        Updated: {{
                        $gt: new Date(Date.now() - 1.1 * 60 * 60 * 1000), 
                        $lt: new Date() // current time
                        }}
                    }}
                }},
                {{
                    '$out': {{
                        's3': {{
                        'bucket': '{s3_bucket_name}',
                        'region': '{s3_bucket_region}',
                        'filename': `invoices/${{datePart}}/${{hourPart}}`,
                        'format': {{
                            'name': 'json',
                            'maxFileSize': '1GB'
                        }}
                        }}
                    }}
                }}
            ];

            try {{
                console.log("Executing aggregation pipeline...");
                const result = await invoices.aggregate(pipeline).toArray();
                console.log("Aggregation completed successfully");
            }} catch (err) {{
                console.error("Error during aggregation:", err.message);
            }}

            console.log("Export complete");
        }};
    """
    return source


def get_appservices_token(public_key: str, private_key: str)-> tuple[bool, str]:
    mdb_appservices_token_req = requests.post(
        url=f"{MONGO_ATLAS_APPSERVICES_API_URL}/auth/providers/mongodb-cloud/login",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        json={
            "username": public_key,
            "apiKey": private_key
        }
    )
    if mdb_appservices_token_req.status_code != 200:
        return False, f"Error getting MongoDB Atlas appservices token: {mdb_appservices_token_req.status_code}"
    else:
        return True, mdb_appservices_token_req.json()["access_token"]


def get_service_id(token: str, project_id: str, app_id: str, name)-> tuple[bool, str]:
    mdb_appservices_services_req = requests.get(
        url=f"{MONGO_ATLAS_APPSERVICES_API_URL}/groups/{project_id}/apps/{app_id}/services",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
    )

    services = list(filter(lambda x: x["name"] == name, mdb_appservices_services_req.json()))

    if mdb_appservices_services_req.status_code != 200:
        return False, f"Status code: {mdb_appservices_services_req.status_code}, Error: {mdb_appservices_services_req.text}"
    elif len(services) == 0:
        return False, f"Status code: {mdb_appservices_services_req.status_code}, Error: No services found with name '{name}'"
    else:
        return True, services[0]["_id"]


def get_function_id(token: str, project_id: str, app_id: str, name: str)-> tuple[bool, str]:
    mdb_appservices_functions_req = requests.get(
        url=f"{MONGO_ATLAS_APPSERVICES_API_URL}/groups/{project_id}/apps/{app_id}/functions",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
    )

    functions = list(filter(lambda x: x["name"] == name, mdb_appservices_functions_req.json()))

    if mdb_appservices_functions_req.status_code != 200:
        return False, f"status code: {mdb_appservices_functions_req.status_code}, error: {mdb_appservices_functions_req.text}"
    elif len(functions) == 0:
        return False, f"status code: {mdb_appservices_functions_req.status_code}, error: no functions found with name '{name}'"
    else:
        return True, functions[0]["_id"]


def create_app(
        token: str,
        project_id: str,
        name: str,
        federated_db_name: str,
        product: str = "atlas",
        template_id: str = "triggers",
        location: str = "US-OR",
        provider_region: str = "aws-us-east-2") -> tuple[bool, str]:

    mdb_appservices_apps_req = requests.post(
        url=f"{MONGO_ATLAS_APPSERVICES_API_URL}/groups/{project_id}/apps?product={product}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        },
        json={
            "name": name,
            "provider_region": provider_region,
            "location": location,
            "deployment_model": "LOCAL",
            "environment": "",
            # https://www.mongodb.com/docs/atlas/app-services/reference/template-apps/
            "template_id": template_id,
            #"data_source": {
            #    "name": federated_db_name,
            #    "type": "datalake",
            #    "config": {
            #        "dataLakeName": "federated-default"
            #    }
            #}
        }
    )

    if mdb_appservices_apps_req.status_code == 201:
        return True, mdb_appservices_apps_req.json()["_id"]
    else:
        return False, f"Status code: {mdb_appservices_apps_req.status_code}, Error: {mdb_appservices_apps_req.json()}"


def get_app_id(token: str, project_id: str, name: str = "Triggers", product: str = "atlas")-> tuple[bool, str]:
    mdb_appservices_apps_req = requests.get(
        url=f"{MONGO_ATLAS_APPSERVICES_API_URL}/groups/{project_id}/apps?product={product}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
    )

    if mdb_appservices_apps_req.status_code != 200:
        return False, f"Status code: {mdb_appservices_apps_req.status_code}, Error: {mdb_appservices_apps_req.text}"
    elif len(mdb_appservices_apps_req.json()) == 0:
        return False, f"Status code: {mdb_appservices_apps_req.status_code}, Error: No apps found with name '{name}'"
    else:
        app_id = list(filter(lambda x: x["name"] == name, mdb_appservices_apps_req.json()))[0]["_id"]
        return True, app_id


def create_function(token: str, project_id: str, name: str, app_id: str, source: str)-> tuple[bool, str]:
    mdb_appservices_functions_req = requests.get(
        url=f"{MONGO_ATLAS_APPSERVICES_API_URL}/groups/{project_id}/apps/{app_id}/functions",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
    )

    functions = list(filter(lambda x: x["name"] == name, mdb_appservices_functions_req.json()))

    if len(functions) > 0:
        return True, f"Function '{name}' already exists"

    mdb_appservices_function_req = requests.post(
        url=f"{MONGO_ATLAS_APPSERVICES_API_URL}/groups/{project_id}/apps/{app_id}/functions",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "name": name,
            "source": source,
            "run_as_system": True,
            "private": True
        }
    )

    if mdb_appservices_function_req.status_code != 201:
        return False, f"Status code: {mdb_appservices_function_req.status_code}, Error: {mdb_appservices_function_req.json()}"

    return True, f"Created function '{name}'"


def create_data_federation_s3(
        name: str,
        database_name: str,
        project_id: str,
        mdb_public_key: str,
        mdb_private_key: str,
        aws_access_role_id: str,
        aws_region: str,
        aws_bucket_name: str,
        aws_bucket_prefix: str = "",
        mdb_data_process_region: str = "OREGON_USA")-> tuple[bool, str]:

    mdb_data_federations_req = requests.get(
        url=f"{MONGO_ATLAS_API_URL}/groups/{project_id}/dataFederation",
        headers={
            "Accept": "application/vnd.atlas.2024-11-13+json"
        },
        auth=HTTPDigestAuth(mdb_public_key, mdb_private_key),
    )

    data_federations = list(filter(lambda x: x["name"] == name, mdb_data_federations_req.json()))
    if mdb_data_federations_req.status_code != 200:
        return False, f"Status code: {mdb_data_federations_req.status_code}, Error: {mdb_data_federations_req.json()}"
    elif len(data_federations) > 0:
        return True, data_federations[0]["name"]

    mdb_data_federation_req = requests.post(
        url=f"{MONGO_ATLAS_API_URL}/groups/{project_id}/dataFederation",
        headers={
            "Content-Type": "application/vnd.atlas.2024-11-13+json",
            "Accept": "application/vnd.atlas.2024-11-13+json"
        },
        auth=HTTPDigestAuth(mdb_public_key, mdb_private_key),
        json={
            "name": name,
            "cloudProviderConfig": {
                "aws": {
                    "roleId": aws_access_role_id,
                    "testS3Bucket": aws_bucket_name
                }
            },
            "dataProcessRegion": {
                "cloudProvider": "AWS",
                # https://www.mongodb.com/docs/atlas/reference/amazon-aws/#std-label-amazon-aws
                "region": mdb_data_process_region
            },
            "storage": {
                "databases": [
                    {
                        "name": database_name,
                        "collections": [
                            {
                            "name": "customers",
                            "dataSources": [
                                {
                                    "collection": "customer-updates",
                                    "database": "customers",
                                    "storeName": "dev2-infra"
                                }
                            ]
                            },
                            {
                            "name": "initial-customers",
                            "dataSources": [
                                {
                                    "collection": "Customer",
                                    "database": "customers",
                                    "storeName": "dev2-infra"
                                }
                            ]
                            },
                            {
                            "name": "initial-invoices",
                            "dataSources": [
                                {
                                    "collection": "Invoice",
                                    "database": "invoices",
                                    "storeName": "dev2-infra"
                                }
                            ]
                            },
                            {
                            "name": "initial-tenants",
                            "dataSources": [
                                {
                                    "collection": "TenantDashboard",
                                    "database": "identity",
                                    "storeName": "dev2-identity"
                                }
                            ]
                            },
                            {
                            "name": "initial-shops",
                            "dataSources": [
                                {
                                    "collection": "ShopDashboard",
                                    "database": "identity",
                                    "storeName": "dev2-identity"
                                }
                            ]
                            },
                            {
                            "name": "invoices",
                            "dataSources": [
                                {
                                    "collection": "invoice-updates",
                                    "database": "invoices",
                                    "storeName": "dev2-infra"
                                }
                            ]
                            },
                            {
                            "name": "shops",
                            "dataSources": [
                                {
                                    "collection": "shop-updates",
                                    "database": "identity",
                                    "storeName": "dev2-identity"
                                }
                            ]
                            },
                            {
                            "name": "tenants",
                            "dataSources": [
                                {
                                    "collection": "tenant-updates",
                                    "database": "identity",
                                    "storeName": "dev2-identity"
                                }
                            ]
                            },
                            {
                            "name": "initial-service-objects",
                            "dataSources": [
                                {
                                    "collection": "ServiceObject",
                                    "database": "service-objects",
                                    "storeName": "dev2-infra"
                                }
                            ]
                            },
                            {
                            "name": "service-objects",
                            "dataSources": [
                                {
                                    "collection": "service-object-updates",
                                    "database": "service-objects",
                                    "storeName": "dev2-infra"
                                }
                            ]
                            }
                        ],
                    }
                ],
                "stores": [
                    {
                        "name": "s3-dwh",
                        "provider": "s3",
                        "bucket": aws_bucket_name,
                        "region": aws_region,
                        "delimiter": "/",
                        "prefix": aws_bucket_prefix
                    },
                    {
                        "clusterName": "identity-dev2-mongo01",
                        "name": "dev2-identity",
                        "projectId": project_id,
                        "provider": "atlas",
                        "readPreference": {
                            "mode": "secondary"
                        }
                    },
                    {
                        "clusterName": "infra-dev2-mongo01",
                        "name": "dev2-infra",
                        "projectId": project_id,
                        "provider": "atlas",
                        "readPreference": {
                            "mode": "secondary"
                        }
                    },
                ]
            }
        }
    )

    if mdb_data_federation_req.status_code != 200:
        return False, f"Status code: {mdb_data_federation_req.status_code}, Error: {mdb_data_federation_req.json()}"
    else:
        return True, mdb_data_federation_req.json()["name"]


def create_trigger(token: str,
                   name: str,
                   function_id: str,
                   trigger_type: str,
                   project_id: str,
                   app_id: str,
                   schedule: str = "",
                   database: str = "",
                   collection: str =  "",
                   service_id: str = "",
                   op_types: list[str] = ["INSERT"]) -> tuple[bool, str]:

    mdb_appservices_triggers_req = requests.get(
        url=f"{MONGO_ATLAS_APPSERVICES_API_URL}/groups/{project_id}/apps/{app_id}/triggers",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
    )

    triggers = list(filter(lambda x: x["name"] == name, mdb_appservices_triggers_req.json()))
    if len(triggers) > 0:
        return True, f"Trigger '{name}' already exists"

    if trigger_type == "DATABASE":
        request_payload = {
            "name": name,
            "type": trigger_type,
            "function_id": function_id,
            "config": {
                "operation_types": op_types,
                "database": database,
                "collection": collection,
                "service_id": service_id,
                "match": {},
                "project": {},
                "full_document": True
            },
            "event_processors": {}
        }
    elif trigger_type == "SCHEDULED":
        request_payload = {
            "name": name,
            "type": trigger_type,
            "function_id": function_id,
            "config": {
                "schedule": schedule 
            }
        }
    else:
        return False, f"Invalid trigger type: {trigger_type}"

    mdb_appservices_trigger_req = requests.post(
        url=f"{MONGO_ATLAS_APPSERVICES_API_URL}/groups/{project_id}/apps/{app_id}/triggers",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json=request_payload
    )

    if mdb_appservices_trigger_req.status_code != 201:
        return False, f"Status code: {mdb_appservices_trigger_req.status_code}, Error: {mdb_appservices_trigger_req.json()}"
    return True, f"Created trigger '{name}'"


def create_application_datasource_links(token: str, project_id: str, name: str, cluster_name: str, app_id: str)-> tuple[bool, str]:

    mdb_appservices_datasource_links_req = requests.post(
        url=f"{MONGO_ATLAS_APPSERVICES_API_URL}/groups/{project_id}/apps/{app_id}/multi_data_sources",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json=[
            {
                "name": name,
                "type": "mongodb-atlas",
                "config": {
                    "clusterName": cluster_name
                }
            }
        ]
    )

    if mdb_appservices_datasource_links_req.status_code != 201:
        return False, f"Status code: {mdb_appservices_datasource_links_req.status_code}, Error: {mdb_appservices_datasource_links_req.json()}"
    return True, f"Created application datasource link '{name}'"


def create_cloud_provider_access_role(mdb_public_key: str, mdb_private_key: str, project_id: str) -> tuple[bool, str | dict]:
    mdb_cloud_provider_access_roles_req = requests.get(
        url=f"{MONGO_ATLAS_API_URL}/groups/{project_id}/cloudProviderAccess",
        headers={
            "Content-Type": "application/vnd.atlas.2024-11-13+json",
            "Accept": "application/vnd.atlas.2024-11-13+json"
        },
        auth=HTTPDigestAuth(mdb_public_key, mdb_private_key),
    )

    access_roles = mdb_cloud_provider_access_roles_req.json()["awsIamRoles"]
    if len(access_roles) > 0:
        return True, {
            "existing": True,
            "role_id": access_roles[0]["roleId"],
            "external_id": access_roles[0]["atlasAssumedRoleExternalId"],
            "atlas_account_arn": access_roles[0]["atlasAWSAccountArn"]
        }

    mdb_cloud_provider_access_roles_req = requests.post(
        url=f"{MONGO_ATLAS_API_URL}/groups/{project_id}/cloudProviderAccess",
        headers={
            "Content-Type": "application/vnd.atlas.2024-11-13+json",
            "Accept": "application/vnd.atlas.2024-11-13+json"
        },
        json={
            "providerName": "AWS",
        },
        auth=HTTPDigestAuth(mdb_public_key, mdb_private_key),
    )

    if mdb_cloud_provider_access_roles_req.status_code != 200:
        return False, f"Status code: {mdb_cloud_provider_access_roles_req.status_code}, Error: {mdb_cloud_provider_access_roles_req.json()}"
    else:
        return True, {
            "existing": False,
            "role_id": mdb_cloud_provider_access_roles_req.json()["roleId"],
            "external_id": mdb_cloud_provider_access_roles_req.json()["atlasAssumedRoleExternalId"],
            "atlas_account_arn": mdb_cloud_provider_access_roles_req.json()["atlasAWSAccountArn"]
        }

def authorize_cloud_provider_access_role(mdb_public_key: str, mdb_private_key: str, project_id: str, role_id: str, role_arn: str) -> tuple[bool, str | dict]:
    mdb_cloud_provider_auth_role_req = requests.patch(
        url=f"{MONGO_ATLAS_API_URL}/groups/{project_id}/cloudProviderAccess/{role_id}",
        headers={
            "Content-Type": "application/vnd.atlas.2024-11-13+json",
            "Accept": "application/vnd.atlas.2024-11-13+json"
        },
        auth=HTTPDigestAuth(mdb_public_key, mdb_private_key),
        json={
            "providerName": "AWS",
            "iamAssumedRoleArn": role_arn
        }
    )

    if mdb_cloud_provider_auth_role_req.status_code == 405:
        return True, f"Status code: {mdb_cloud_provider_auth_role_req.status_code}, Error: {mdb_cloud_provider_auth_role_req.text}"
    else:
        if mdb_cloud_provider_auth_role_req.status_code != 200:
            return False, f"Status code: {mdb_cloud_provider_auth_role_req.status_code}, Error: {mdb_cloud_provider_auth_role_req.text}"
        return True, mdb_cloud_provider_auth_role_req.json()
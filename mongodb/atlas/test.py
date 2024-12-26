import asyncio
import httpx
from sys import argv

class Admin():
    __api_endpoint = 'https://cloud.mongodb.com'
    __api_base_path = '/api/atlas/v2'
    __api_headers = {
        'Accept': 'application/vnd.atlas.2024-08-05+json',
        'Content-type': 'application/vnd.atlas.2024-08-05+json'
    }

    def __init__(self, public_key: str, private_key: str, project_id: str):
        self.__public_key = public_key
        self.__private_key = private_key
        self.__project_id = project_id
 
    # Base request
    async def __request(self, path: str, method: str = 'GET', json: dict | None = None, expected_status: int = 200) -> tuple[bool, dict]:
        async with httpx.AsyncClient() as client:
            r = await client.request(
                method=method,
                url=f'{self.__api_endpoint}{self.__api_base_path}/{path}',
                auth=httpx.DigestAuth(self.__public_key, self.__private_key),
                headers=self.__api_headers,
                json=json
            )
        if r.status_code == expected_status:
            return True, r.json()
        else:
            return False, { 'code': r.status_code, 'message': r.text }

    # Admin API methods
    async def get_clusters(self, name: None | str = None) -> tuple[bool, dict]:
        res, clusters = await self.__request(f'groups/{self.__project_id}/clusters')
        if name != None:
            return res, { 'results': list(filter(lambda x: x['name'] == name, clusters['results'])) }
        return res, clusters

    async def get_data_federations(self, name: None | str = None) -> tuple[bool, dict]:
        res, datafederations = await self.__request(f'groups/{self.__project_id}/dataFederation')
        if name != None:
            return res, { 'results': list(filter(lambda x: x['name'] == name, datafederations)) }
        return res, datafederations

    async def get_cloud_provider_access(self, provider_name: None | str = None) -> tuple[bool, dict]:
        res, providers = await self.__request(f'groups/{self.__project_id}/cloudProviderAccess')
        key = ''
        if provider_name == None:
            return res, providers
        elif provider_name not in ['AWS', 'AZURE']:
            return False, { 'message': 'Invalid provider name' }
        else:
            if provider_name == 'AWS': key = 'awsIamRoles'
            if provider_name == 'AZURE': key = 'azureServicePrincipals'
            return res, providers[key]

    async def create_data_federation(self, name: str, databases: list[dict], stores: list[dict], role_id: str, cloud_provider: str = 'AWS', test_bucket: str = '') -> tuple[bool, dict]:
        res_federations, out_federations =  await self.get_data_federations()
        filter_federations = list(filter(lambda x: x['name'] == name, out_federations))
        if res_federations and len(filter_federations) > 0:
            return True, filter_federations[0]
        if cloud_provider not in ['AWS']:
            return False, { 'message': 'Invalid or not implemented cloud provider' }
        cloud_provider_config = {}
        if cloud_provider == 'AWS':
            cloud_provider_config = {
                'aws': {
                    'roleId': role_id,
                    'testS3Bucket': test_bucket
                }
            }
        return await self.__request(
            f'groups/{self.__project_id}/dataFederation',
            method='POST',
            json={
                'name': name,
                'cloudProviderConfig': cloud_provider_config,
                'storage': {
                    'databases': databases,
                    'stores': stores
                },
            },
            expected_status=200
        )


class Appservices():
    __api_appservices_endpoint = 'https://services.cloud.mongodb.com'
    __api_appservices_base_path = '/api/admin/v3.0'
    __api_appservices_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    def __init__(self, public_key: str, private_key: str, project_id: str):
        self.__public_key = public_key
        self.__private_key = private_key
        self.__project_id = project_id
        self.__appservices_token = None
        self.__appservices_refresh_token = None

    # Base request
    async def __request(self, path: str, method: str = 'GET', json: dict | None = None, expected_status: int = 200) -> tuple[bool, dict]:
        async with httpx.AsyncClient() as client:
            r = await client.request(
                method=method,
                url=f'{self.__api_appservices_endpoint}{self.__api_appservices_base_path}/{path}',
                headers={
                    'Authorization': f'Bearer {self.__appservices_token}'
                },
                json=json,
                timeout=15
            )
        if r.status_code == expected_status:
            return True, r.json()
        else:
            return False, { 'code': r.status_code, 'message': r.text }

    async def get_appservices_token(self) -> None:
        async with httpx.AsyncClient() as client:
            if self.__appservices_token:
                r = await client.post(
                    url=f'{self.__api_appservices_endpoint}{self.__api_appservices_base_path}/auth/session',
                    headers={
                        'Authorization': f'Bearer {self.__appservices_refresh_token}'
                    },
                )
                if r.status_code == 200:
                    self.__appservices_token = r.json()["access_token"]
            else:
                r = await client.post(
                    url=f'{self.__api_appservices_endpoint}{self.__api_appservices_base_path}/auth/providers/mongodb-cloud/login',
                    json={
                        "username": self.__public_key,
                        "apiKey": self.__private_key
                    }
                )
                if r.status_code == 200:
                    self.__appservices_token = r.json()["access_token"]
                    self.__appservices_refresh_token = r.json()["refresh_token"]

    # Appservices API methods
    async def get_apps(self, product: str = 'atlas') -> tuple[bool, dict]:
        await self.get_appservices_token()
        return await self.__request(f'groups/{self.__project_id}/apps?product={product}')

    async def get_app_functions(self, app_id: str) -> tuple[bool, dict]:
        await self.get_appservices_token()
        return await self.__request(f'groups/{self.__project_id}/apps/{app_id}/functions')

    async def get_app_services(self, app_id: str) -> tuple[bool, dict]:
        await self.get_appservices_token()
        return await self.__request(f'groups/{self.__project_id}/apps/{app_id}/services')

    async def get_app_triggers(self, app_id: str) -> tuple[bool, dict]:
        await self.get_appservices_token()
        return await self.__request(f'groups/{self.__project_id}/apps/{app_id}/triggers')

    async def create_app_service(self, app_id: str, name: str, cluster_name: str = '', type: str = 'mongodb-atlas') -> tuple[bool, dict]:
        await self.get_appservices_token()
        res_services, out_services =  await self.get_app_services(app_id=app_id)
        filter_services = list(filter(lambda x: x['name'] == name, out_services))
        if res_services and len(filter_services) > 0:
            return True, filter_services[0]
        if type == 'mongodb-atlas':
            config = {
                'clusterName': cluster_name,
                'readPreference': 'primary',
                'wireProtocolEnabled': True
            }
        elif type == 'datalake':
            config = {
                'dataLakeName': cluster_name
            }
        else:
            return False, { 'message': 'Invalid service type' }
        return await self.__request(
            f'groups/{self.__project_id}/apps/{app_id}/services',
            method='POST',
            json={
                'name': name,
                'type': type,
                'config': config
            },
            expected_status=201
        )

    async def create_app_service_link(self, app_id: str, data_sources: list[dict]) -> tuple[bool, dict]:
        await self.get_appservices_token()
        res_services, out_services =  await self.get_app_services(app_id=app_id)
        filtered_data_sources = []
        for data_source in data_sources:
            found = False
            for service in out_services:
                if data_source['name'] == service['name']:
                    found = True
            if not found:
                filtered_data_sources.append(data_source)
        return await self.__request(
            f'groups/{self.__project_id}/apps/{app_id}/multi_data_sources',
            method='POST',
            json=filtered_data_sources,
            expected_status=201
        )

    async def create_app(self, app_name: str, cluster_name: str, product: str = 'atlas', template_id: str = 'triggers') -> tuple[bool, dict]:
        await self.get_appservices_token()
        res_apps, out_apps =  await self.get_apps()
        filter_apps = list(filter(lambda x: x['name'] == app_name, out_apps))
        if res_apps and len(filter_apps) > 0:
            return True, filter_apps[0]
        return await self.__request(
            f'groups/{self.__project_id}/apps?product={product}',
            method='POST',
            json={
                'name': app_name,
                'template_id': template_id,
                'data_source': {
                    'name': cluster_name,
                    'type': 'mongodb-atlas',
                    'config': {
                        'clusterName': cluster_name,
                        'readPreference': 'primary',
                        'wireProtocolEnabled': True
                    }
                }
            },
            expected_status=201
        )

    async def create_app_function(self, app_id: str, name: str, source: str) -> tuple[bool, dict]:
        await self.get_appservices_token()
        res_functions, out_functions =  await self.get_app_functions(app_id=app_id)
        filter_functions = list(filter(lambda x: x['name'] == name, out_functions))
        if res_functions and len(filter_functions) > 0:
            return True, filter_functions[0]
        return await self.__request(
            f'groups/{self.__project_id}/apps/{app_id}/functions',
            method='POST',
            json={
                'name': name,
                'source': source,
                'private': True,
                'run_as_system': True
            },
            expected_status=201
        )

    async def create_app_trigger(
            self,
            trigger_name: str,
            app_id: str,
            schedule: str = '',
            database: str = '',
            collection: str = '',
            service_id: str = '',
            function_id: str = '',
            type: str = 'DATABASE',
            operations: list[str] = ['INSERT']) -> tuple[bool, dict]:
        await self.get_appservices_token()
        res_triggers, out_triggers =  await self.get_app_triggers(app_id=app_id)
        filter_triggers = list(filter(lambda x: x['name'] == trigger_name, out_triggers))
        if res_triggers and len(filter_triggers) > 0:
            return True, filter_triggers[0]
        if type == 'DATABASE':
            config = {
                'database': database,
                'collection': collection,
                'service_id': service_id,
                'operation_types': operations
            }
        elif type == 'SCHEDULED':
            config = {
                'schedule': schedule
            }
        else:
            return False, { 'message': 'Invalid trigger type' }
        return await self.__request(
            f'groups/{self.__project_id}/apps/{app_id}/triggers',
            method='POST',
            json={
                'name': trigger_name,
                'type': type,
                'function_id': function_id,
                'config': config
            },
            expected_status=201
        )


async def main():
    public_key = argv[1]
    private_key = argv[2]
    project_id = argv[3]

    if not public_key or not private_key or not project_id:
        print("Usage: python test.py <public_key> <private_key> <project_id>")
        exit(1)

    atlas_admin = Admin(
            public_key=public_key,
            private_key=private_key,
            project_id=project_id
    )

    atlas_appservices = Appservices(
            public_key=public_key,
            private_key=private_key,
            project_id=project_id
    )

    services = {
        'infra-prod-mongo01': { 'type': 'mongodb-atlas', 'name': 'infra-prod-mongo01', 'cluster_name': 'infra-prod-mongo01' },
        'identity-prod-mongo01': { 'type': 'mongodb-atlas', 'name': 'identity-prod-mongo01', 'cluster_name': 'identity-prod-mongo01' },
        'prod-dwh': { 'type': 'datalake', 'name': 'prod-dwh', 'cluster_name': 'prod-dwh' },
    }

    # Each function name must match a trigger name
    functions = {
        'customer': { 'type': 'database', 'name': 'customer', 'source': 'exports = function() { return "hello world!"; }' },
        'invoice': { 'type': 'database', 'name': 'invoice', 'source': 'exports = function() { return "hello world!"; }' },
        'tenant': { 'type': 'database', 'name': 'invoice', 'source': 'exports = function() { return "hello world!"; }' },
        'shop': { 'type': 'database', 'name': 'shop', 'source': 'exports = function() { return "hello world!"; }' },
        'service_objects': { 'type': 'database', 'name': 'service_objects', 'source': 'exports = function() { return "hello world!"; }' },

        'customer-to-s3': { 'type': 'scheduled', 'name': 'customer', 'source': 'exports = function() { return "hello world!"; }' },
        'invoice-to-s3': { 'type': 'scheduled', 'name': 'invoice', 'source': 'exports = function() { return "hello world!"; }' },
        'tenant-to-s3': { 'type': 'scheduled', 'name': 'invoice', 'source': 'exports = function() { return "hello world!"; }' },
        'shop-to-s3': { 'type': 'scheduled', 'name': 'shop', 'source': 'exports = function() { return "hello world!"; }' },
        'service_objects-to-s3': { 'type': 'scheduled', 'name': 'service_objects', 'source': 'exports = function() { return "hello world!"; }' },
    }

    # Each function name must match a trigger name
    triggers = {
        'customer': { 'type': 'DATABASE', 'name': 'customer', 'operations': ["INSERT", "UPDATE", "DELETE", "REPLACE"], 'database': 'customers', 'collection': 'Customer', 'service': 'infra-prod-mongo01' },
        'invoice': { 'type': 'DATABASE', 'name': 'invoice', 'operations': ["INSERT", "UPDATE", "DELETE", "REPLACE"], 'database': 'invoices', 'collection': 'Invoice', 'service': 'infra-prod-mongo01' },
        'tenant': { 'type': 'DATABASE', 'name': 'tenant', 'operations': ["INSERT", "UPDATE", "DELETE", "REPLACE"], 'database': 'identity', 'collection': 'TenantDashboard', 'service': 'identity-prod-mongo01' },
        'shop': { 'type': 'DATABASE', 'name': 'shop', 'operations': ["INSERT", "UPDATE", "DELETE", "REPLACE"], 'database': 'identity', 'collection': 'ShopDashboard', 'service': 'identity-prod-mongo01' },
        'service_objects': { 'type': 'DATABASE', 'name': 'service_objects', 'operations': ["INSERT", "UPDATE", "DELETE", "REPLACE"], 'database': 'service-objects', 'collection': 'ServiceObject', 'service': 'infra-prod-mongo01' },

        'customer-to-s3': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'infra-prod-mongo01', 'schedule': '0 */1 * * *' },
        'invoice-to-s3': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'infra-prod-mongo01', 'schedule': '0 */1 * * *' },
        'tenant-to-s3': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'identity-prod-mongo01', 'schedule': '0 */1 * * *' },
        'shop-to-s3': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'identity-prod-mongo01', 'schedule': '0 */1 * * *' },
        'service_objects-to-s3': { 'type': 'SCHEDULED', 'name': 'customer', 'service': 'infra-prod-mongo01', 'schedule': '0 */1 * * *' },
    }

    federation_databases = [
        {
            "name": "prod-dwh",
            "views": [],
            "collections": [
                {
                    "name": "customers",
                    "dataSources": [
                        {
                            "collection": "customer-updates",
                            "database": "customers",
                            "storeName": "prod-infra"
                        }
                    ]
                },
                {
                    "name": "initial-customers",
                    "dataSources": [
                        {
                            "collection": "Customer",
                            "database": "customers",
                            "storeName": "prod-infra"
                        }
                    ]
                },
                {
                    "name": "initial-invoices",
                    "dataSources": [
                        {
                            "collection": "Invoice",
                            "database": "invoices",
                            "storeName": "prod-infra"
                        }
                    ]
                },
                {
                    "name": "initial-tenants",
                    "dataSources": [
                        {
                            "collection": "TenantDashboard",
                            "database": "identity",
                            "storeName": "prod-identity"
                        }
                    ]
                },
                {
                    "name": "initial-shops",
                    "dataSources": [
                        {
                            "collection": "ShopDashboard",
                            "database": "identity",
                            "storeName": "prod-identity"
                        }
                    ]
                },
                {
                    "name": "invoices",
                    "dataSources": [
                        {
                            "collection": "invoice-updates",
                            "database": "invoices",
                            "storeName": "prod-infra"
                        }
                    ]
                },
                {
                    "name": "shops",
                    "dataSources": [
                        {
                            "collection": "shop-updates",
                            "database": "identity",
                            "storeName": "prod-identity"
                        }
                    ]
                },
                {
                    "name": "tenants",
                    "dataSources": [
                        {
                            "collection": "tenant-updates",
                            "database": "identity",
                            "storeName": "prod-identity"
                        }
                    ]
                },
                {
                    "name": "initial-service-objects",
                    "dataSources": [
                        {
                            "collection": "ServiceObject",
                            "database": "service-objects",
                            "storeName": "prod-infra"
                        }
                    ]
                },
                {
                    "name": "service-objects",
                    "dataSources": [
                        {
                            "collection": "service-object-updates",
                            "database": "service-objects",
                            "storeName": "prod-infra"
                        }
                    ]
                }
            ],
        }
    ]
    federation_stores = [
        {
            "clusterName": "infra-prod-mongo01",
            "name": "prod-infra",
            "projectId": project_id,
            "provider": "atlas",
            "readPreference": {
                "mode": "secondary"
            }
        },
        {
            "clusterName": "identity-prod-mongo01",
            "name": "prod-identity",
            "projectId": project_id,
            "provider": "atlas",
            "readPreference": {
                "mode": "secondary"
            }
        },
        {
            "bucket": "s3-steer-dwh-prod",
            "delimiter": "/",
            "name": "s3-steer-dwh-prod",
            "provider": "s3",
            "region": "us-east-2"
        }
    ]

    # Get Cloud Providers
    res_providers, out_providers = await atlas_admin.get_cloud_provider_access(provider_name='AWS')
    print(f"Providers: {out_providers}")
    exit(1) if not res_providers else None

    res_data_federations, out_data_federations = await atlas_admin.create_data_federation(
        name='prod-dwh',
        databases=federation_databases,
        stores=federation_stores,
        role_id=out_providers[0]['roleId'],
        test_bucket='s3-steer-dwh-prod'
    )
    print(f"Data Federations: {out_data_federations}")
    exit(1) if not res_data_federations else None

    # Create App
    res_app, out_app = await atlas_appservices.create_app(app_name='Triggers', cluster_name='infra-prod-mongo01')
 
    print(f"App: {out_app}")
    exit(1) if not res_app else None

    # Create Services
    async with asyncio.TaskGroup() as tg:
        services_tasks = {
            service: tg.create_task(atlas_appservices.create_app_service(app_id=out_app['_id'], name=services[service]['name'], cluster_name=services[service]['cluster_name'], type=services[service]['type']))
            for service in services
        }

    for task in services_tasks:
        res_service, out_service = await services_tasks[task]
        print(f"Service: {out_service}")
        exit(1) if not res_service else None

    res_app_services, out_app_services = await atlas_appservices.get_app_services(app_id=out_app['_id'])
    print(f"App Services: {out_app_services}")
    exit(1) if not res_app_services else None

    # Link Data Sources
    data_sources = [
        {'name': services[service]['name'], 'type': services[service]['type'], 'config': {'clusterName': services[service]['cluster_name']}}
        for service in services
    ]

    res_link_serivces, out_link_services = await atlas_appservices.create_app_service_link(app_id=out_app['_id'], data_sources=data_sources)
    print(f"Link Services: {out_link_services}")
    exit(1) if not res_link_serivces else None

    # Create Functions
    async with asyncio.TaskGroup() as tg:
        tasks_functions = {
            function: tg.create_task(
                atlas_appservices.create_app_function(app_id=out_app['_id'], name=function, source=open('functions/' + functions[function]['type'] + '-' + functions[function]['name'] + '.js').read())
            )
            for function in functions
        }
    for task in tasks_functions:
        res_function, out_function = await tasks_functions[task]
        print(f"Function [{task}]: {out_function}")
        exit(1) if not res_function else None

    # Create Triggers
    async with asyncio.TaskGroup() as tg:
        tasks_triggers_database = {
            trigger: tg.create_task(atlas_appservices.create_app_trigger(
                trigger_name=trigger,
                app_id=out_app['_id'],
                operations=triggers[trigger]['operations'],
                database=triggers[trigger]['database'],
                collection=triggers[trigger]['collection'],
                service_id=services_tasks[triggers[trigger]['service']].result()[1]['_id'],
                function_id=tasks_functions[trigger].result()[1]['_id'],
                type=triggers[trigger]['type']
            ))
            for trigger in triggers if triggers[trigger]['type'] == 'DATABASE'
        }
        tasks_triggers_scheduled = {
                trigger: tg.create_task(atlas_appservices.create_app_trigger(
                    trigger_name=trigger,
                    app_id=out_app['_id'],
                    schedule=triggers[trigger]['schedule'],
                    function_id=tasks_functions[trigger].result()[1]['_id'],
                    type=triggers[trigger]['type']
                ))
                for trigger in triggers if triggers[trigger]['type'] == 'SCHEDULED'
        }
        tasks = {**tasks_triggers_database, **tasks_triggers_scheduled}
    for task in tasks:
        res_trigger, out_trigger = await tasks[task]
        print(f"Trigger [{task}]: {out_trigger}")
        exit(1) if not res_trigger else None

if __name__ == '__main__':
    asyncio.run(main())
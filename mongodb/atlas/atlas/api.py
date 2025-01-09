import httpx
from json import loads

# https://www.mongodb.com/docs/atlas/reference/api-resources-spec/v2
class Admin():
    __api_endpoint = 'https://cloud.mongodb.com'
    __api_base_path = '/api/atlas/v2'
    __api_timeout = 30
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
                json=json,
                timeout=self.__api_timeout,
            )
        if r.status_code == expected_status:
            try:
                loads(r.text)
            except ValueError:
                return True, { 'code': r.status_code, 'message': r.text }
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

# https://www.mongodb.com/docs/atlas/app-services/admin/api/v3
class Appservices():
    __api_appservices_endpoint = 'https://services.cloud.mongodb.com'
    __api_appservices_base_path = '/api/admin/v3.0'
    __api_appservices_timeout = 30

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
                timeout=self.__api_appservices_timeout,
            )
        if r.status_code == expected_status:
            try:
                loads(r.text)
            except ValueError:
                return True, { 'code': r.status_code, 'message': r.text }
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

    async def create_app_function(self, app_id: str, name: str, source: str, recreate: bool = False) -> tuple[bool, dict]:
        await self.get_appservices_token()
        exists = False
        function_id = None
        res_functions, out_functions =  await self.get_app_functions(app_id=app_id)
        filter_functions = list(filter(lambda x: x['name'] == name, out_functions))
        if res_functions and len(filter_functions) > 0:
            exists = True
            function_id = filter_functions[0]['_id']
            #return True, filter_functions[0]
        if not exists:
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
        else:
            # Update disabled as it doesn't return JSON and breaks the expected format
            res, out = await self.__request(
                f'groups/{self.__project_id}/apps/{app_id}/functions/{function_id}',
                method='PUT',
                json={
                    'name': name,
                    'source': source,
                    'private': True,
                    'run_as_system': True
                },
                expected_status=204
            )
            if res:
                out['_id'] = function_id
            return res, out

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
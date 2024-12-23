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

    # Admin API methods
    async def get_clusters(self) -> tuple[bool, dict]:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                url=f'{self.__api_endpoint}{self.__api_base_path}/groups/{self.__project_id}/clusters',
                auth=httpx.DigestAuth(self.__public_key, self.__private_key),
                headers=self.__api_headers
            )
        if r.status_code == 200:
            return True, r.json()
        else:
            return False, { 'code': r.status_code, 'message': r.text }

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

    # Appservices API methods
    async def get_apps(self) -> tuple[bool, dict]:
        await self.get_appservices_token()
        async with httpx.AsyncClient() as client:
            r = await client.get(
                url=f'{self.__api_appservices_endpoint}{self.__api_appservices_base_path}/groups/{self.__project_id}/apps',
                headers={
                    'Authorization': f'Bearer {self.__appservices_token}'
                }
            )
        if r.status_code == 200:
            return True, r.json()
        else:
            return False, { 'code': r.status_code, 'message': r.text }

    async def get_functions(self, app_id: str) -> tuple[bool, dict]:
        await self.get_appservices_token()
        async with httpx.AsyncClient() as client:
            r = await client.get(
                url=f'{self.__api_appservices_endpoint}{self.__api_appservices_base_path}/groups/{self.__project_id}/apps/{app_id}/functions',
                headers={
                    'Authorization': f'Bearer {self.__appservices_token}'
                }
            )
        if r.status_code == 200:
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


async def main():
    atlas_admin = Admin(
            public_key=argv[1],
            private_key=argv[2],
            project_id=argv[3]
    )

    atlas_appservices = Appservices(
            public_key=argv[1],
            private_key=argv[2],
            project_id=argv[3]
    )

    res_clusters, out_clusters = await atlas_admin.get_clusters()
    res_apps, out_apps = await atlas_appservices.get_apps()
    res_functions, out_functions = await atlas_appservices.get_functions(out_apps[0]["_id"])
    print(f"Clusters: {out_clusters}")
    print(f"Apps: {out_apps}")
    print(f"Functions: {out_functions}")

if __name__ == '__main__':
    asyncio.run(main())
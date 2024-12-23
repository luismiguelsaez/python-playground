import asyncio
import httpx
from sys import argv

class Atlas():
    __api_endpoint = 'https://cloud.mongodb.com'
    __api_base_path = '/api/atlas/v2'
    __api_appservices_endpoint = 'https://services.cloud.mongodb.com'
    __api_appservices_base_path = '/api/admin/v3.0'
    __api_headers = {
        'Accept': 'application/vnd.atlas.2024-08-05+json',
        'Content-type': 'application/vnd.atlas.2024-08-05+json'
    }
    _api_appservices_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    def __init__(self, public_key: str, private_key: str, project_id: str):
        self.__public_key = public_key
        self.__private_key = private_key
        self.__project_id = project_id
        self.__appservices_token = None
        self.__appservices_refresh_token = None

    # Admin API methods
    async def get_clusters(self):
        async with httpx.AsyncClient() as client:
            r = await client.get(
                url=f'{self.__api_endpoint}{self.__api_base_path}/groups/{self.__project_id}/clusters',
                auth=httpx.DigestAuth(self.__public_key, self.__private_key),
                headers=self.__api_headers
            )
            return r.json()

    # Appservices API methods
    async def get_appservices_apps(self):
        await self.get_appservices_token()
        async with httpx.AsyncClient() as client:
            r = await client.get(
                url=f'{self.__api_appservices_endpoint}{self.__api_appservices_base_path}/groups/{self.__project_id}/apps',
                headers={
                    'Authorization': f'Bearer {self.__appservices_token}'
                }
            )
            return r.json()

    async def get_appservices_token(self):
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
    atlas = Atlas(
            public_key=argv[1],
            private_key=argv[2],
            project_id=argv[3]
    )

    clusters = await atlas.get_clusters()
    apps = await atlas.get_appservices_apps()
    print(f"Clusters: {clusters}")
    print(f"Apps: {apps}")

if __name__ == '__main__':
    asyncio.run(main())
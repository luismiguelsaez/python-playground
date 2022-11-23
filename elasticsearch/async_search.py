from elasticsearch import AsyncElasticsearch as async_es
import asyncio

async def search(cli: async_es, idx: str, query: dict)->dict:
  res = await cli.search(body=query, index=idx)
  return res

data_hosts = ['10.18.11.189', '10.18.44.115', '10.18.74.95']
es_cli = async_es(hosts=data_hosts)

query = {
  "term": {
    "project_id": {
      "value": "13371795637ba7c4f0fa71.43201554"
    }
  }
}

async def main():
  L = await asyncio.gather(
    search(cli=es_cli, idx='lokalise-project-keys-2022-07-26', query={}),
    search(cli=es_cli, idx='lokalise-project-keys-2022-07-26', query={}),
    search(cli=es_cli, idx='lokalise-project-keys-2022-07-26', query={})
  )

  print(L)

if __name__ == "__main__":
  asyncio.run(main())

import elasticsearch
import asyncio
from random import randrange


master_nodes = ['10.18.34.36','10.18.8.71','10.18.84.184']
data_tm_nodes = ['10.18.78.149','10.18.60.81','10.18.7.144']

es_cli = elasticsearch.AsyncElasticsearch(master_nodes)

queries = [
  {"bool":{"must":[{"bool":{"should":[{"match":{"from_string":{"query":"Link your number to local SIM number through Roamer, no roaming fee and 100% reachable, high reliable and never miss important incoming calls.","operator":"OR","prefix_length":0,"max_expansions":50,"fuzzy_transpositions":True,"lenient":False,"zero_terms_query":"NONE","auto_generate_synonyms_phrase_query":True,"boost":1.0}}}],"adjust_pure_negative":True,"boost":1.0}}],"filter":[{"term":{"team_id":{"value":359626,"boost":1.0}}},{"term":{"file_id":{"value":0,"boost":1.0}}},{"terms":{"to_lang_id":[640,666,714,1056,673,766],"boost":1.0}},{"term":{"from_lang_id":{"value":640,"boost":1.0}}}],"adjust_pure_negative":True,"boost":1.0}},
]

async def es_search(queries: list):
  query = queries[randrange(len(queries))]
  resp = await es_cli.search(
    index='lokalise-translation-memory-2022-06-01',
    query=query,
    size=20)

  if len(resp['hits']['hits']) > 0:
    docs = [{"from": d['_source']['from_string'], "to": d['_source']['to_string']} for d in resp['hits']['hits']]
    return {"Result": docs}
  else:
    return {"Error": "No docs found"}


async def main():
  task = asyncio.create_task(es_search(queries))
  val = await task
  print(val)

asyncio.run(main())

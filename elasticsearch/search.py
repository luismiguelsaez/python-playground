import elasticsearch
import asyncio

master_nodes = ['10.18.34.36','10.18.8.71','10.18.84.184']
data_tm_nodes = ['10.18.78.149','10.18.60.81','10.18.7.144']

es_cli = elasticsearch.AsyncElasticsearch(master_nodes)

query = {
  "bool":{
    "must":[
      {
        "bool":{
          "should":[
            {
              "match":{
                "from_string":{
                  "query":"<xliff:g>%d</xliff:g> years ago",
                  "operator":"OR",
                  "prefix_length":0,
                  "max_expansions":50,
                  "fuzzy_transpositions":True,
                  "lenient":True,
                  "zero_terms_query":"NONE",
                  "auto_generate_synonyms_phrase_query":True,
                  "boost":1.0
                }
              }
            }
          ],
          "adjust_pure_negative":True,
          "boost":1.0
        }
      }
    ],
    "filter":[
      {
        "term":{
          "team_id":{
            "value":192627,
            "boost":1.0
          }
        }
      },
      {
        "terms":{
          "file_id":[703,0],
          "boost":1.0
        }
      },
      {
        "term":{
          "to_lang_id":{
            "value":610,
            "boost":1.0
          }
        }
      },
      {
        "term":{
          "from_lang_id":{
            "value":1055,
            "boost":1.0
          }
        }
      }
    ],
    "adjust_pure_negative":True,
    "boost":1.0
  }
}

async def main():
  resp = await es_cli.search(
    index='lokalise-translation-memory-2022-06-01',
    query=query,
    size=20)

  if len(resp['hits']['hits']) > 0:
    for doc in resp['hits']['hits']:
      print("{} -> {}".format(doc['_source']['from_string'],doc['_source']['to_string']))
  else:
    print("No docs found")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

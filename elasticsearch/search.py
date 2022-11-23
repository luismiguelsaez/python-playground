import elasticsearch
from time import sleep
from random import randrange
import threading


master_nodes = ['10.18.34.36','10.18.8.71','10.18.84.184']
data_tm_nodes = ['10.18.78.149','10.18.60.81','10.18.7.144']

es_cli = elasticsearch.Elasticsearch(master_nodes)

queries = [
  {"bool":{"must":[{"bool":{"should":[{"match":{"from_string":{"query":"Link your number to local SIM number through Roamer, no roaming fee and 100% reachable, high reliable and never miss important incoming calls.","operator":"OR","prefix_length":0,"max_expansions":50,"fuzzy_transpositions":True,"lenient":False,"zero_terms_query":"NONE","auto_generate_synonyms_phrase_query":True,"boost":1.0}}}],"adjust_pure_negative":True,"boost":1.0}}],"filter":[{"term":{"team_id":{"value":359626,"boost":1.0}}},{"term":{"file_id":{"value":0,"boost":1.0}}},{"terms":{"to_lang_id":[640,666,714,1056,673,766],"boost":1.0}},{"term":{"from_lang_id":{"value":640,"boost":1.0}}}],"adjust_pure_negative":True,"boost":1.0}},
  {"bool":{"must":[{"bool":{"should":[{"match":{"from_string":{"query":"Playback current message","operator":"OR","prefix_length":0,"max_expansions":50,"fuzzy_transpositions":True,"lenient":False,"zero_terms_query":"NONE","auto_generate_synonyms_phrase_query":True,"boost":1.0}}}],"adjust_pure_negative":True,"boost":1.0}}],"filter":[{"term":{"team_id":{"value":359626,"boost":1.0}}},{"term":{"file_id":{"value":0,"boost":1.0}}},{"terms":{"to_lang_id":[640,666,714,1056,673,766],"boost":1.0}},{"term":{"from_lang_id":{"value":640,"boost":1.0}}}],"adjust_pure_negative":True,"boost":1.0}},
  {"bool":{"must":[{"bool":{"should":[{"match":{"from_string":{"query":"TechСrunch, Engadget & Mashable all agree that Roamer is one of the best and cheapest ways to stay connected and avoid roaming charges abroad while keeping your own number.\n\nRoamer is the only calling app for travelers who would like to stay connected abroad with their regular numbers while avoiding roaming charges.\n\nSwap you sim for a local one to receive calls in Roamer with your regular number. Make international calls to mobile and landline numbers at unbeatable rates when abroad or from home.\n\nFEATURES\n\n- New unbeatable rates – check your favorite destinations for cheap deals, note the exciting rate and immediately place a call – first calls are on us!\n- Validate your regular number so your friends see it’s a call from you.\n- Will work either on any working SIM – data or voice, in roaming 3g or at home; or on WiFi as VOIP: you’re the master of choice.\n- Use Roamer on Wi-Fi or 3G for maximum savings and link a local SIM in Roamer for reliable calls when you go around.\n- Connect across the globe in more than 200 countries including US, UK, Europe & India.\n- Switch on receiving calls on your regular number in Roamer wherever and whenever (for users from over 50 countries around the world and most of the operators and plans; local rates may apply).\n- Enjoy dialing directly to local numbers without any additional calling codes.\n- Stay reachable with free voicemail to email. Return calls at your first convenience.\n- Transfer a Wi-Fi call to a regular call on the fly. A neat feature for varying Wi-Fi conditions.\n- Even without a linked SIM, push notifications will not let you miss a call if Roamer is off.\n- Purchase prepaid packages or top up your account\n\nRoamer does not bother you with ads. We keep your privacy.\n\nPRESS\n- \"A great app to keep your phone number without getting roaming fees.\" Huffington Post\n- \"Perhaps the app's best feature is that it allows travelers to use their own cell phone numbers instead of designating temporary alternatives\" Mashable\n- \"Roamer is a new iOS and Android app that forwards your regular number onto a local SIM card, ensuring that you'll pay native rates even when calling your loved ones.\" Engadget\n- \"The set-up is slick…Charges are well below standard roaming rates\" Telegraph\n- \"Roamer makes it easier to make calls from foreign climes\" Tech Crunch\n\nCONNECT WITH US\n- Facebook: https://www.facebook.com/RoamerApp\n- Twitter: https://twitter.com/roamerapp\n- Email: support@roamerapp.com","operator":"OR","prefix_length":0,"max_expansions":50,"fuzzy_transpositions":True,"lenient":False,"zero_terms_query":"NONE","auto_generate_synonyms_phrase_query":True,"boost":1.0}}}],"adjust_pure_negative":True,"boost":1.0}}],"filter":[{"term":{"team_id":{"value":359626,"boost":1.0}}},{"term":{"file_id":{"value":0,"boost":1.0}}},{"terms":{"to_lang_id":[640,666,714,1056,673,766],"boost":1.0}},{"term":{"from_lang_id":{"value":640,"boost":1.0}}}],"adjust_pure_negative":True,"boost":1.0}}
]

def es_search(queries: list, result: list, index: int, num: int):
  for _ in range(num):
    query = queries[randrange(len(queries))]
    resp = es_cli.search(
      index='lokalise-translation-memory-2022-06-01',
      query=query,
      size=20)

    if len(resp['hits']['hits']) > 0:
      docs = [{"from": d['_source']['from_string'], "to": d['_source']['to_string']} for d in resp['hits']['hits']]
      result[index] = {"Query": query, "Docs": len(docs)}
    else:
      result[index] = f"No docs retrieved"

    sleep(0.1)


def main():
  t_num = 10
  q_num = 1000
  threads = [None for _ in range(t_num)]
  results = [None for _ in range(t_num * q_num )]
  for i in range(len(threads)):
    threads[i] = threading.Thread(target=es_search, args=(queries, results, i, q_num))

  for i in range(len(threads)):
    threads[i].start()

  for i in range(len(threads)):
    threads[i].join()

  print(len(results))

main()


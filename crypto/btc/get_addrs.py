import pandas
from sys import argv

base_addr = 'https://blockchain.info/rawaddr/'
btc_addrs = [x for x in argv[1:]]

sum = 0
for addr in btc_addrs:
  df = pandas.read_json(base_addr + addr)
  transactions = df['txs']

  for transaction in transactions:
    n = list(filter(lambda x:x['addr'] == addr, transaction['out']))
    for t in n:
      sum += t['value']/100000000
      print("Address", addr, t['value']/100000000, "BTC")

print("Total", sum, "BTC")

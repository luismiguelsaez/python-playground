from requests import get as req_get
import json

ak = 'AIOUQOO4CK1M1WQ6'

from_cur = 'BTC'
to_cur = 'EUR'

# DOC: https://www.alphavantage.co/documentation/
res = req_get(f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_cur}&to_currency={to_cur}&apikey={ak}")
res_obj = json.dumps(res.json())

print(type(res_obj))

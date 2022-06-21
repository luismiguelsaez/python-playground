import logging
from flask import Flask
from flask import jsonify
from flask import request
import random
from prometheus_flask_exporter import PrometheusMetrics

logging.basicConfig(level=logging.INFO)
logging.info("Setting LOGLEVEL to INFO")

api = Flask(__name__)
metrics = PrometheusMetrics(api)

metrics.info("app_info", "", version="1.0.0")

byPathCounter = metrics.counter(
    'byPathCounter', 'Request count by request paths',
    labels={'path': lambda: request.path}
)

@api.route("/",methods=['GET'])
@byPathCounter
def root():
  msg, httpCode = randomResponse()
  return jsonify(msg), httpCode

def randomResponse():
  httpCodes = [200,500]
  httpResponseCode = random.choices(population=httpCodes,weights=(95,10),k=1)
  if httpResponseCode[0] == 200:
    return {"message": "success"}, httpResponseCode[0]
  elif httpResponseCode[0] == 500:
    return {"message": "error"}, httpResponseCode[0]

api.run(host='0.0.0.0', port=80)

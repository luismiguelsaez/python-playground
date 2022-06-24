import logging
from flask import Flask
from flask import jsonify
from flask import request
import random
from prometheus_flask_exporter import PrometheusMetrics

logging.basicConfig(level=logging.INFO)
logging.info("Setting LOGLEVEL to INFO")

api = Flask(__name__)

metrics = PrometheusMetrics(api, group_by='endpoint')
metrics.info("app_info", "", version="1.0.0")

byPathCounter = metrics.counter(
    'api_requests_count_by_path', 'Request count by request paths',
    labels={'path': lambda: request.path}
)
byStatusSummary = metrics.summary(
  'api_requests_latency_by_status', 'Request latencies by status',
  labels={'status': lambda r: r.status_code}
)
byStatusPathHistogram = metrics.histogram(
  'api_requests_latency_by_status_and_path', 'Request latencies by status and path',
  labels={'status': lambda r: r.status_code, 'path': lambda: request.path}
)

@api.route("/health",methods=['GET'])
@metrics.do_not_track()
def health():
  return jsonify({"healthy":"true"}), 200

@api.route("/",methods=['GET'])
@byPathCounter
@byStatusSummary
@byStatusPathHistogram
def root():
  msg, httpCode = randomResponse()
  return jsonify(msg), httpCode

def randomResponse():
  httpCodes = [200,500]
  httpResponseCode = random.choices(population=httpCodes,weights=(95,5),k=1)
  if httpResponseCode[0] == 200:
    return {"message": "success"}, httpResponseCode[0]
  elif httpResponseCode[0] == 500:
    return {"message": "error"}, httpResponseCode[0]

api.run(host='0.0.0.0', port=80)

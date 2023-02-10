from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def request_validate():
  json.dumps(request.body)

app.run(host='0.0.0.0', port='5000')
from flask import Flask, request
import json
import os

app = Flask(__name__)

LOG_FILE = 'logs.txt'

@app.route('/', methods=['POST'])
def log():
    data = request.json
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(data) + '\\n')
    print(f"Log received: {json.dumps(data)}")
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)

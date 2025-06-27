from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests
import os

app = Flask(__name__)
mongo_host = os.environ.get('MONGO_HOST', 'mongodb')
client = MongoClient(f'mongodb://{mongo_host}:27017/')
db = client.todo
collection = db.tasks

logger_url = os.environ.get('LOGGER_URL', 'http://logger:9000')

def log_event(action, data):
    payload = {
        'action': action,
        'data': data
    }
    try:
        requests.post(logger_url, json=payload)
    except Exception as e:
        print(f"Error logging: {e}")

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = list(collection.find({}, {'_id': 0}))
    log_event('GET /tasks', {'count': len(tasks)})
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    collection.insert_one(data)
    log_event('POST /tasks', data)
    return jsonify({'message': 'Task created'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

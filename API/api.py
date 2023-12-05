from flask import Flask, request, jsonify
import json
import logging
import secret_santas_functions as secret_santa
import os

logging.basicConfig(level=logging.INFO)

APP_ENV = os.getenv('APP_ENV')

app = Flask(__name__)

@app.route('/secret-santa/health', methods=['GET'])
def health():
    try:
        status = secret_santa.db_healthcheck()
        if not status:
            return "Unhealthy", 400
        return "Healthy", 200
    except Exception as e:
        return f"Error checking database health: {e}", 500


@app.route('/secret-santa/store_data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()
        group_name = data.get('group')  # Extract collection name from JSON
        if not group_name:
            return "Collection name not provided in the request", 400
        group = secret_santa.db[group_name]
        response = secret_santa.insert_user(group, data)
        return response , 200
    except Exception as e:
        return f"Error storing user data: {e}", 500

@app.route('/secret-santa/randomize_secret_santa', methods=['POST'])
def randomize_secret_santa():

    try:
        data = request.get_json()
        group_name = data.get('group')  # Extract collection name from JSON
        if not group_name:
            return "Collection name not provided in the request", 400
        
        if APP_ENV == "Test":
            print("Testing Mode")
            collection = secret_santa.db[group_name]  # Use the collection name dynamically
            cursor = collection.find()
            documents = list(cursor)
            json_documents = json.dumps(documents, default=str, indent=1)
            json_data = json.loads(json_documents)
            ids = [doc['_id'] for doc in json_data]
            assignments = secret_santa.secret_santa(ids)
            secret_santa_json = secret_santa.print_secret_santa(collection, assignments)
            return secret_santa_json, 200
        collection = secret_santa.db[group_name]  # Use the collection name dynamically
        cursor = collection.find()
        documents = list(cursor)
        json_documents = json.dumps(documents, default=str, indent=1)
        json_data = json.loads(json_documents)
        ids = [doc['_id'] for doc in json_data]
        assignments = secret_santa.secret_santa(ids)
        secret_santa.send_secret_santa(collection, assignments)
        return "Secret Santa assignments randomized and emails sent!"
    except Exception as e:
        return f"Error randomizing Secret Santa: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


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
            return jsonify({"status": "error", "message": "Unhealthy"}), 400
        return jsonify({"status": "success", "message": "Healthy"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error checking database health: {str(e)}"}), 500


@app.route('/secret-santa/store_data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()
        group_name = data.get('group')  # Extract collection name from JSON
        if not group_name:
            return jsonify({"status": "error", "message": "Collection name not provided in the request"}), 400
        group = secret_santa.db[group_name]
        response = secret_santa.insert_user(group, data)
        return jsonify({"status": "success", "message": response}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error storing user data: {str(e)}"}), 500


@app.route('/secret-santa/randomize_secret_santa', methods=['POST'])
def randomize_secret_santa():
    try:
        data = request.get_json()
        group_name = data.get('group')  # Extract collection name from JSON
        if not group_name:
            return jsonify({"status": "error", "message": "Collection name not provided in the request"}), 400
        
        collection = secret_santa.db[group_name]  # Use the collection name dynamically
        cursor = collection.find()
        documents = list(cursor)
        ids = [doc['_id'] for doc in documents]
        assignments = secret_santa.secret_santa(ids)
        
        if APP_ENV == "Test":
            print("Testing Mode")
            secret_santa_json = secret_santa.print_secret_santa(collection, assignments)
            return jsonify({"status": "success", "data": secret_santa_json}), 200
        
        secret_santa.send_secret_santa(collection, assignments)
        return jsonify({"status": "success", "message": "Secret Santa assignments randomized and emails sent!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error randomizing Secret Santa: {str(e)}"}), 500


@app.route('/secret-santa/get-rooms', methods=['POST'])
def get_rooms():
    try:
        data = request.get_json()
        object_id = data.get('object_id') if data else None  # Get the optional ObjectId parameter from the request
        rooms = secret_santa.get_rooms_with_object_ids(object_id=object_id)
        return jsonify({"status": "success", "data": rooms}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error getting rooms: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
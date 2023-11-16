from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://santaapp:test@10.10.10.29:27017/secret-santa')
db = client['secret-santa']
collection = db['participants']

@app.route('/store_data', methods=['POST'])
def store_data():
        data = request.get_json()
        result = collection.insert_one(data)
        if result.inserted_id:
                return 'Data stored in MongoDB successfully!'
        else:
                return 'Failed to store data in MongoDB.'
@app.route('/get_participants', methods=['GET'])
def get_data():
        result = collection.find()
        return result
if __name__ == '__main__':
    app.run(debug=True)


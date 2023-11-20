from flask import Flask, request
from pymongo import MongoClient
from bson import ObjectId
import json
import os
import re
import random
import smtplib
from email.message import EmailMessage
import logging

#from dotenv import load_dotenv

#load_dotenv()

logging.basicConfig(level=logging.INFO)

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = int(os.getenv('MONGO_PORT'))
MONGO_DB = os.getenv('MONGO_DB')
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASS = os.getenv('MONGO_PASS')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')

client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}")
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]



SENDER_EMAIL = os.getenv('SMTP_SENDER_EMAIL')
EMAIL_SUBJECT = os.getenv('SMTP_SUBJECT')
SMTP_SERVER = os.getenv('SMTP_URL')  # Replace with your SMTP server
SMTP_PORT = int(os.getenv('SMTP_PORT'))  # Replace with your SMTP server's port
SMTP_USERNAME = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASW')


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def insert_user(collection, user_data):
    try:
        if not validate_email(user_data["email"]):
            logging.info("Invalid email. Not inserting.")
            return "Invalid email. Not inserting."

        # Check for existing user with the same email
        existing_email = collection.find_one({"email": user_data["email"]})
        if existing_email:
            logging.info("User with this email already exists. Not inserting.")
            return "User with this email already exists. Not inserting."

        # Check for existing user with same details
        existing_user = collection.find_one({
            "Name": user_data["Name"],
            "Surname": user_data["Surname"],
            "email": user_data["email"]
        })

        if existing_user:
            logging.info("User with same name, surname, and email already exists. Not inserting.")
            return "User with same name, surname, and email already exists. Not inserting."

        result = collection.insert_one(user_data)
        if result.inserted_id:
            logging.info('Data stored in MongoDB successfully!')
            return "Data stored in MongoDB successfully!"
        else:
            logging.info('Failed to store data in MongoDB.')
            return "Failed to store data in MongoDB."
    except Exception as e:
        logging.info(f"Error inserting user data: {e}")
        return f"Error inserting user data: {e}"


def secret_santa(ids):
    shuffled_ids = list(ids)
    random.shuffle(shuffled_ids)
    assignments = {}

    for i in range(len(ids)):
        while True:
            recipient = random.choice(shuffled_ids)
            if recipient != ids[i]:
                break
        assignments[ids[i]] = recipient
        shuffled_ids.remove(recipient)

    return assignments

def print_secret_santa(collection, assignments):
    for santa, recipient in assignments.items():
        santa_id = ObjectId(santa)
        recipient_id = ObjectId(recipient)

        santa_details = collection.find_one({"_id": santa_id})
        recipient_details = collection.find_one({"_id": recipient_id})

        if santa_details and recipient_details:
            logging.info(f"{santa_details['Name']} {santa_details['Surname']} ({santa_details['email']}) "
                  f"is the Secret Santa for {recipient_details['Name']} {recipient_details['Surname']} "
                  f"({recipient_details['email']})")
        else:
            logging.info(f"Participant details not found for Santa ID: {santa}, Recipient ID: {recipient}")

def send_secret_santa(collection, assignments):
    for santa, recipient in assignments.items():
        santa_id = ObjectId(santa)
        recipient_id = ObjectId(recipient)

        santa_details = collection.find_one({"_id": santa_id})
        recipient_details = collection.find_one({"_id": recipient_id})

        if santa_details and recipient_details:
            receiver_email = f"{santa_details['email']}"
            email_body = f"Congratulations {santa_details['Name']} {santa_details['Surname']}, you are Secret Santa for {recipient_details['Name']} {recipient_details['Surname']}"
            logging.info(receiver_email)
            logging.info(email_body)
            send_email(SENDER_EMAIL, receiver_email, EMAIL_SUBJECT, email_body, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD)
        else:
            logging.info(f"Participant details not found for Santa ID: {santa}, Recipient ID: {recipient}")

def send_email(SENDER_EMAIL, receiver_email, subject, body, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#            server.connect()
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
#            server.close()
        logging.info("Email sent successfully!")
        return "Email sent successfully!"
    except Exception as e:
        logging.info(f"Error sending email: {e}")
        return f"Error sending email: {e}"


app = Flask(__name__)

@app.route('/secret-santa/store_data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()
        group_name = data.get('group')  # Extract collection name from JSON
        if not group_name:
            return "Collection name not provided in the request", 400
        group = db[group_name]
        response = insert_user(group, data)
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
        
        collection = db[group_name]  # Use the collection name dynamically
        cursor = collection.find()
        documents = list(cursor)
        json_documents = json.dumps(documents, default=str, indent=1)
        json_data = json.loads(json_documents)
        ids = [doc['_id'] for doc in json_data]
        assignments = secret_santa(ids)
        send_secret_santa(collection, assignments)
        return "Secret Santa assignments randomized and emails sent!"
    except Exception as e:
        return f"Error randomizing Secret Santa: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


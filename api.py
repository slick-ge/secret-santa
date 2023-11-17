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
logging.basicConfig(level=logging.INFO)

MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_PORT = int(os.environ.get('MONGO_PORT'))
MONGO_DB = os.environ.get('MONGO_DB')
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')
MONGO_COLLECTION = os.environ.get('MONGO_COLLECTION')

client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/")
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]



sender_email = os.environ.get('SMTP_SENDER_EMAIL')
email_subject = os.environ.get('SMTP_SUBJECT')
smtp_server = os.environ.get('SMTP_URL')  # Replace with your SMTP server
smtp_port = int(os.environ.get('SMTP_PORT'))  # Replace with your SMTP server's port
smtp_username = os.environ.get('SMTP_USER')
smtp_password = os.environ.get('SMTP_PASW')


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def insert_user(collection, user_data):
    try:
        if not validate_email(user_data["email"]):
            logging.info("Invalid email. Not inserting.")
            return

        # Check for existing user with the same email
        existing_email = collection.find_one({"email": user_data["email"]})
        if existing_email:
            logging.info("User with this email already exists. Not inserting.")
            return

        # Check for existing user with same details
        existing_user = collection.find_one({
            "Name": user_data["Name"],
            "Surname": user_data["Surname"],
            "email": user_data["email"]
        })

        if existing_user:
            logging.info("User with same name, surname, and email already exists. Not inserting.")
            return

        result = collection.insert_one(user_data)
        if result.inserted_id:
            logging.info('Data stored in MongoDB successfully!')
        else:
            logging.info('Failed to store data in MongoDB.')
    except Exception as e:
        logging.info(f"Error inserting user data: {e}")


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

def logging.info_secret_santa(collection, assignments):
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
            send_email(sender_email, receiver_email, email_subject, email_body, smtp_server, smtp_port, smtp_username, smtp_password)
        else:
            logging.info(f"Participant details not found for Santa ID: {santa}, Recipient ID: {recipient}")

def send_email(sender_email, receiver_email, subject, body, smtp_server, smtp_port, smtp_username, smtp_password):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        logging.info("Email sent successfully!")
    except Exception as e:
        logging.info("Error sending email:", e)


app = Flask(__name__)

@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()
        insert_user(collection, data)
        return "User data stored successfully!", 200
    except Exception as e:
        return f"Error storing user data: {e}", 500

@app.route('/randomize_secret_santa', methods=['GET'])
def randomize_secret_santa():
    cursor = collection.find()
    documents = list(cursor)
    json_documents = json.dumps(documents, default=str, indent=1)
    json_data = json.loads(json_documents)
    ids = [doc['_id'] for doc in json_data]
    assignments = secret_santa(ids)
    send_secret_santa(collection, assignments)
    
    return "Secret Santa assignments randomized and emails sent!"

if __name__ == '__main__':
    app.run(debug=True)


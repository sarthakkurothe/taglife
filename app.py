from flask import Flask, request, jsonify
from google.cloud import storage
from cryptography.fernet import Fernet
import os
import psycopg2
import config

app = Flask(__name__)

# Load Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.GOOGLE_APPLICATION_CREDENTIALS

# Initialize Google Cloud Storage client
client = storage.Client()
bucket = client.bucket(config.BUCKET_NAME)

# Generate a key for encryption
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=config.DB_HOST,
    database=config.DB_NAME,
    user=config.DB_USER,
    password=config.DB_PASS
)
cursor = conn.cursor()

# Create consent table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS consent (
        id SERIAL PRIMARY KEY,
        consent TEXT
    )
''')
conn.commit()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Encrypt file before uploading
    file_data = file.read()
    encrypted_data = cipher_suite.encrypt(file_data)

    blob = bucket.blob(file.filename)
    blob.upload_from_string(encrypted_data)

    return jsonify({"message": "File uploaded successfully"}), 200

@app.route('/consent', methods=['POST'])
def get_consent():
    data = request.get_json()
    if not data or 'parental_consent' not in data:
        return jsonify({"error": "Consent data is required"}), 400
    consent = data['parental_consent']

    # Save consent to PostgreSQL database
    cursor.execute("INSERT INTO consent (consent) VALUES (%s)", (consent,))
    conn.commit()

    return jsonify({"message": "Consent recorded successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)

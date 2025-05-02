from flask import Flask
from pymongo import MongoClient
from mongodb.config.connection_db import get_database
import os


app = Flask(__name__)

db = get_database()

@app.route('/')
def index():
    return 'Welcome to CloudSoft!'

# @app.route('/save', methods=['POST'])
# def save_data():
#     if db is None:
#         return jsonify({"error": "Database not connected"}), 500

#     data = request.json
#     result = db["uploads"].insert_one(data)
#     return jsonify({"message": "Data saved", "id": str(result.inserted_id)})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

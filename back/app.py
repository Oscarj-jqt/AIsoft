from flask import Flask
from flask_cors import CORS
from mongodb.config.connection_db import get_database
from api.routes.auth import auth_bp 
from api.routes.weapon import upload_bp, process_bp, identify_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY","dev")

CORS(app, supports_credentials=True)


db = get_database()

app.register_blueprint(auth_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(process_bp)
app.register_blueprint(identify_bp)


@app.route('/')
def index():
    return 'Welcome to AIsoft!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

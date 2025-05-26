from flask import Flask
from flask_cors import CORS
from mongodb.config.connection_db import get_database
from mongodb.config.initialize_db import initialize_collections
from mongodb.config.test_db import test_database
from api.routes.auth import auth_bp 
from api.routes.weapon import upload_bp, analyze_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY","dev")
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = False


CORS(app, supports_credentials=True, origins=["http://localhost:5173"])


db = get_database()

initialize_collections()
test_database()


app.register_blueprint(auth_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(analyze_bp)


@app.route('/')
def index():
    return 'Welcome to AIsoft!'

if __name__ == '__main__':
    print("Flask démarre...")
    app.run(host='0.0.0.0', port=5000, debug=True)

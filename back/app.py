from flask import Flask
from flask_cors import CORS
from mongodb.config.connection_db import get_database
from api.routes.auth import auth_bp 

app = Flask(__name__)

CORS(app)


db = get_database()

app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return 'Welcome to CloudSoft!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

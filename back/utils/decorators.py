from functools import wraps
from flask import session, jsonify
from bson.objectid import ObjectId
from mongodb.config.connection_db import get_database

db = get_database()
users_collection = db["Users"]

def login_required(f):
    """
    Permet de protéger les routes pour lesquelles l'utilisateur doit être connecté
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Authentification requise"}), 401

        user = users_collection.find_one({"_id": ObjectId(session["user_id"])})
        if not user:
            session.clear()
            return jsonify({"error": "Session invalide"}), 401
        
        return f(*args, **kwargs)
    return decorated_function
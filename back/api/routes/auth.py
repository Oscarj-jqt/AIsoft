from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.errors import DuplicateKeyError
from mongodb.config.connection_db import get_database



auth_bp = Blueprint('auth', __name__, template_folder='front/templates')

db = get_database()
users_collection = db["Users"]

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Aucune donnée reçue"}), 400

    pseudo = data.get("pseudo")
    password = data.get("password")

    if not pseudo or not password:
        return jsonify({"error": "Pseudo et mot de passe requis"}), 400

    try:
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        user_data = {
            "pseudo": pseudo,
            "password": hashed_password,
        }

        users_collection.insert_one(user_data)
        print(f"Nouvel utilisateur inscrit : {pseudo}")
        return jsonify({"message": "Inscription réussie"}), 201

    except DuplicateKeyError:
        print(f"Erreur : Le pseudo '{pseudo}' est déjà utilisé.")
        return jsonify({"error": "Le pseudo est déjà utilisé."}), 409


@auth_bp.route('/login', methods=['POST'])
def login():
    if request.method == 'GET':
        return jsonify({"message": "Veuillez envoyer un POST pour vous connecter"}), 200

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        pseudo = data.get('pseudo')
        password = data.get('password')

        if not pseudo or not password:
            return jsonify({"error": "Pseudo and password required"}), 400

        user = users_collection.find_one({'pseudo': pseudo})

        if user and user.get('password') and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['pseudo'] = user['pseudo']

            print("[DEBUG] Session après login :", dict(session))

            return jsonify({"message": "Connexion réussie"}), 200
        else:
            return jsonify({"error": "Pseudo ou mot de passe incorrect"}), 401

    

    

@auth_bp.route('/logout', methods=['POST'])
def logout():
    if 'pseudo' in session:
        print(f"Utilisateur déconnecté : {session['pseudo']}")
    session.clear()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('auth.login'))
from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.errors import DuplicateKeyError
from mongodb.config.connection_db import get_database



auth_bp = Blueprint('auth', __name__, template_folder='front/templates')

db = get_database()
users_collection = db["Users"]

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        pseudo = request.form['pseudo']
        password = request.form['password']
        

        try:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            user_data = {
                "pseudo": pseudo,
                "password": hashed_password,
            }

            users_collection.insert_one(user_data)
            print(f"Nouvel utilisateur inscrit : {pseudo}")
            flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('auth.login'))

        except DuplicateKeyError:
            print(f"Erreur : Le pseudo '{pseudo}' est déjà utilisé.")
            flash('Le pseudo est déjà utilisé. Veuillez en choisir un autre.', 'danger')

    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route pour la connexion des utilisateurs.
    """
    if request.method == 'POST':
        pseudo = request.form.get('pseudo')
        password = request.form.get('password')

        user = users_collection.find_one({'pseudo': pseudo})

        if user and user['password'] and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['pseudo'] = user['pseudo']
            flash("Connexion réussie !", "success")
            return redirect(url_for('home'))
        else:
            flash("Échec de la connexion. Vérifiez vos identifiants.", "danger")
            return redirect(url_for('auth.login'))
    
    return render_template('login.html')


@auth_bp.route('/logout', methods=['POST'])
def logout():
    if 'pseudo' in session:
        print(f"Utilisateur déconnecté : {session['pseudo']}")
    session.clear()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('auth.login'))
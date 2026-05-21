from flask import Blueprint, render_template, request, redirect, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

from extensions import limiter
from services.security_log_service import log_security_event


auth_routes = Blueprint('auth', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "user_id" not in session:
            return redirect("/auth/login")

        return f(*args, **kwargs)

    return decorated_function


@auth_routes.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Nom d'utilisateur et mot de passe obligatoires", 400

    password_hash = generate_password_hash(password)

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    c.execute("""
        INSERT INTO users (username, password)
        VALUES (?, ?)
    """, (username, password_hash))

    conn.commit()
    conn.close()

    return redirect("/auth/login")


@limiter.limit("5 per minute")
@auth_routes.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template("login.html")

    tentatives = session.get("login_attempts", 0)

    if tentatives >= 5:
        return "Trop de tentatives. Réessayez plus tard.", 429

    username = request.form.get("username")
    password = request.form.get("password")

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id, password
        FROM users
        WHERE username = ?
    """, (username,))

    user = c.fetchone()
    conn.close()

    print("USERNAME =", repr(username))
    print("PASSWORD =", repr(password))
    print("USER SQL =", user)

    if not user:

        session["login_attempts"] = tentatives + 1

        log_security_event(
            "LOGIN_FAILED",
            f"Utilisateur inconnu : {username}"
        )

        return "Identifiants incorrects", 401

    user_id, password_hash = user

    check = check_password_hash(password_hash, password)

    print("HASH SQL =", password_hash)
    print("CHECK =", check)

    if not check:

        session["login_attempts"] = tentatives + 1

        log_security_event(
            "LOGIN_FAILED",
            f"Mauvais mot de passe pour : {username}"
        )

        return "Identifiants incorrects", 401

    log_security_event(
        "LOGIN_SUCCESS",
        f"Connexion réussie : {username}"
    )

    session["login_attempts"] = 0
    session["user_id"] = user_id
    session["username"] = username

    return redirect("/ecritures/tableau-bord")


@auth_routes.route('/logout')
def logout():

    session.clear()

    return redirect("/auth/login")

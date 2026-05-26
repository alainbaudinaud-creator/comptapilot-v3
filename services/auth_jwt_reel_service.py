import base64
import hashlib
import json
import time
from functools import wraps
from flask import request, jsonify
from sqlalchemy import text
from database import engine


def initialiser_auth_jwt_reel():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS utilisateurs_jwt_reel_v3 (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role_utilisateur VARCHAR(100),
                actif BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS permissions_jwt_reel_v3 (
                id SERIAL PRIMARY KEY,
                role_utilisateur VARCHAR(100),
                module VARCHAR(100),
                lecture BOOLEAN DEFAULT TRUE,
                ecriture BOOLEAN DEFAULT FALSE,
                administration BOOLEAN DEFAULT FALSE
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS notifications_live_reel_v3 (
                id SERIAL PRIMARY KEY,
                utilisateur VARCHAR(255),
                message TEXT,
                niveau VARCHAR(50),
                statut VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        existing = conn.execute(text("""
            SELECT COUNT(*) FROM utilisateurs_jwt_reel_v3
        """)).scalar() or 0

        if existing == 0:
            password_hash = hashlib.sha256("demo".encode("utf-8")).hexdigest()

            conn.execute(text("""
                INSERT INTO utilisateurs_jwt_reel_v3
                (email, password_hash, role_utilisateur, actif)
                VALUES
                ('admin@comptapilot.local', :password_hash, 'SUPER_ADMIN', TRUE)
            """), {"password_hash": password_hash})

            conn.execute(text("""
                INSERT INTO permissions_jwt_reel_v3
                (role_utilisateur, module, lecture, ecriture, administration)
                VALUES
                ('SUPER_ADMIN', 'ALL', TRUE, TRUE, TRUE)
            """))

            conn.execute(text("""
                INSERT INTO notifications_live_reel_v3
                (utilisateur, message, niveau, statut)
                VALUES
                ('admin@comptapilot.local', 'Bienvenue dans ComptaPilot V3 temps réel', 'INFO', 'ACTIVE')
            """))


def generer_token(email, role):
    payload = {
        "email": email,
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time()) + 86400
    }

    raw = json.dumps(payload).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("utf-8")


def verifier_token(token):
    try:
        payload = json.loads(base64.urlsafe_b64decode(token.encode("utf-8")).decode("utf-8"))

        if payload.get("exp", 0) < int(time.time()):
            return None

        return payload

    except Exception:
        return None


def login_jwt(email, password):
    initialiser_auth_jwt_reel()

    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    with engine.connect() as conn:
        user = conn.execute(text("""
            SELECT email, role_utilisateur
            FROM utilisateurs_jwt_reel_v3
            WHERE email = :email
            AND password_hash = :password_hash
            AND actif = TRUE
            LIMIT 1
        """), {
            "email": email,
            "password_hash": password_hash,
        }).mappings().first()

    if not user:
        return None

    token = generer_token(user["email"], user["role_utilisateur"])

    return {
        "email": user["email"],
        "role": user["role_utilisateur"],
        "token": token,
    }


def require_api_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")

        if not header.startswith("Bearer "):
            return jsonify({
                "success": False,
                "error": "Token manquant"
            }), 401

        token = header.replace("Bearer ", "").strip()
        payload = verifier_token(token)

        if not payload:
            return jsonify({
                "success": False,
                "error": "Token invalide ou expiré"
            }), 401

        request.jwt_user = payload

        return fn(*args, **kwargs)

    return wrapper


def dashboard_auth_jwt():
    initialiser_auth_jwt_reel()

    stats = {}

    queries = {
        "utilisateurs": "SELECT COUNT(*) FROM utilisateurs_jwt_reel_v3",
        "permissions": "SELECT COUNT(*) FROM permissions_jwt_reel_v3",
        "notifications": "SELECT COUNT(*) FROM notifications_live_reel_v3",
    }

    with engine.connect() as conn:
        for key, query in queries.items():
            stats[key] = conn.execute(text(query)).scalar() or 0

    return stats


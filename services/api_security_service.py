import os

from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv

from services.audit_service import ajouter_log

load_dotenv()

API_KEY = os.getenv("API_KEY")


def api_key_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        provided_key = request.headers.get("X-API-KEY")

        if not provided_key:

            ajouter_log(
                "API_KEY_MANQUANTE",
                "Tentative accès API sans clé API"
            )

            return jsonify({
                "error": "Clé API manquante"
            }), 401

        if provided_key != API_KEY:

            ajouter_log(
                "API_KEY_INVALIDE",
                "Tentative accès API avec clé API invalide"
            )

            return jsonify({
                "error": "Clé API invalide"
            }), 403

        return f(*args, **kwargs)

    return decorated_function

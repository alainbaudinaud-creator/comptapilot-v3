from flask import Blueprint, jsonify, request
from services.auth_jwt_reel_service import (
    initialiser_auth_jwt_reel,
    login_jwt,
    dashboard_auth_jwt,
    require_api_auth,
)

bp_auth_jwt_reel = Blueprint("auth_jwt_reel", __name__)


@bp_auth_jwt_reel.route("/api/v3/auth/login", methods=["POST"])
def api_auth_login():
    initialiser_auth_jwt_reel()

    data = request.get_json(silent=True) or {}

    email = data.get("email", "")
    password = data.get("password", "")

    user = login_jwt(email, password)

    if not user:
        return jsonify({
            "success": False,
            "error": "Identifiants invalides"
        }), 401

    return jsonify({
        "success": True,
        "user": {
            "email": user["email"],
            "role": user["role"],
        },
        "token": user["token"],
    })


@bp_auth_jwt_reel.route("/api/v3/auth/me")
@require_api_auth
def api_auth_me():
    return jsonify({
        "success": True,
        "user": request.jwt_user,
    })


@bp_auth_jwt_reel.route("/api/v3/auth/dashboard")
def api_auth_dashboard():
    return jsonify({
        "success": True,
        "module": "auth_jwt_reel_v3",
        "stats": dashboard_auth_jwt(),
    })

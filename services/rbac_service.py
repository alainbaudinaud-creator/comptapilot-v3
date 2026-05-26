from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt
from services.audit_service import ajouter_log


def role_required(required_role):

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):

            claims = get_jwt()
            user_role = claims.get("role")

            if isinstance(required_role, list):
                allowed_roles = required_role
            else:
                allowed_roles = [required_role]

            if user_role not in allowed_roles:

                ajouter_log(
                    "ACCES_REFUSE",
                    f"Rôle {user_role} refusé. Rôles requis : {allowed_roles}"
                )

                return jsonify({
                    "error": "Accès interdit",
                    "required_role": allowed_roles
                }), 403

            return f(*args, **kwargs)

        return wrapper

    return decorator



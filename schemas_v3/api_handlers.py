from functools import wraps
from flask import jsonify

from schemas_v3.api_response import error_response


def api_safe(handler):

    @wraps(handler)
    def wrapper(*args, **kwargs):

        try:
            return handler(*args, **kwargs)

        except Exception as exc:
            return jsonify(
                error_response(
                    message="Erreur API V3",
                    code="API_V3_ERROR",
                    details={
                        "type": type(exc).__name__,
                        "message": str(exc)
                    }
                )
            ), 500

    return wrapper

from functools import wraps
from flask import jsonify

from logs_v3.logger import log_error, log_info
from schemas_v3.api_response import error_response


def api_safe(handler):

    @wraps(handler)
    def wrapper(*args, **kwargs):

        try:
            response = handler(*args, **kwargs)

            log_info(
                "api_v3",
                "Appel API V3 réussi",
                {
                    "handler": handler.__name__
                }
            )

            return response

        except Exception as exc:

            log_error(
                "api_v3",
                "Erreur API V3",
                {
                    "handler": handler.__name__,
                    "type": type(exc).__name__,
                    "message": str(exc)
                }
            )

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

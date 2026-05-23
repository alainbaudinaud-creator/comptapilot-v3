def success_response(data=None, message="ok"):

    return {
        "success": True,
        "message": message,
        "data": data or {}
    }


def error_response(message="error", code="UNKNOWN_ERROR", details=None):

    return {
        "success": False,
        "message": message,
        "error": {
            "code": code,
            "details": details or {}
        }
    }

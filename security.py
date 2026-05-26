from functools import wraps

from flask import session
from flask import abort


def require_role(*roles):

    def decorator(f):

        @wraps(f)
        def wrapper(*args, **kwargs):

            role = session.get("role")

            if role not in roles:
                abort(403)

            return f(*args, **kwargs)

        return wrapper

    return decorator


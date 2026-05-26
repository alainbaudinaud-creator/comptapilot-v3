from datetime import datetime
import json


def log_event(level: str, module: str, message: str, context=None):

    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "module": module,
        "message": message,
        "context": context or {}
    }

    print(json.dumps(payload, ensure_ascii=False))

    return payload


def log_info(module: str, message: str, context=None):
    return log_event("INFO", module, message, context)


def log_warning(module: str, message: str, context=None):
    return log_event("WARNING", module, message, context)


def log_error(module: str, message: str, context=None):
    return log_event("ERROR", module, message, context)


from flask import request
import time
import uuid

from logs_v3.logger import log_info


def install_http_logging(app):

    @app.before_request
    def start_request_timer():

        request.request_id = str(uuid.uuid4())
        request.start_time = time.time()


    @app.after_request
    def log_http_response(response):

        duration_ms = 0

        if hasattr(request, "start_time"):
            duration_ms = round(
                (time.time() - request.start_time) * 1000,
                2
            )

        log_info(
            "http",
            "Requête HTTP",
            {
                "request_id": getattr(request, "request_id", None),
                "method": request.method,
                "path": request.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "remote_addr": request.remote_addr
            }
        )

        return response

    return app


from flask import request

from logs_v3.logger import log_info


def log_http_response(response):

    log_info(
        "http",
        "Requête HTTP",
        {
            "method": request.method,
            "path": request.path,
            "status_code": response.status_code,
            "remote_addr": request.remote_addr
        }
    )

    return response

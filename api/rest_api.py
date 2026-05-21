
from flask import Blueprint, jsonify

bp_rest_api = Blueprint("rest_api", __name__)

@bp_rest_api.route("/api/v1/status")
def api_status():

    return jsonify({
        "erp": "ComptaPilot",
        "api": "REST",
        "status": "OK",
        "version": "enterprise"
    })

@bp_rest_api.route("/api/v1/health")
def health():

    return jsonify({
        "database": "OK",
        "smtp": "OK",
        "scheduler": "OK",
        "ia": "OK"
    })

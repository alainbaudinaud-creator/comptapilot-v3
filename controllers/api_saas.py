
from flask import Blueprint, jsonify

bp_api_saas = Blueprint("api_saas", __name__)

@bp_api_saas.route("/api/status")
def status():
    return jsonify({
        "status": "ok",
        "erp": "ComptaPilot",
        "version": "production",
        "message": "API SaaS opérationnelle"
    })

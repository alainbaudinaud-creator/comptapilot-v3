from flask import Blueprint, jsonify
from services.enterprise_grade_service import (
    initialiser_enterprise_grade,
    dashboard_enterprise,
    generer_backup_cloud,
    simulation_mfa,
    moteur_predictif,
)

bp_enterprise_grade = Blueprint("enterprise_grade", __name__)


@bp_enterprise_grade.route("/api/v3/enterprise/dashboard")
def api_enterprise_dashboard():

    try:

        initialiser_enterprise_grade()

        return jsonify({
            "success": True,
            "module": "enterprise_grade_v3",
            "data": dashboard_enterprise(),
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@bp_enterprise_grade.route("/api/v3/enterprise/mfa")
def api_enterprise_mfa():

    return jsonify({
        "success": True,
        "resultat": simulation_mfa(),
    })


@bp_enterprise_grade.route("/api/v3/enterprise/backup")
def api_enterprise_backup():

    return jsonify({
        "success": True,
        "resultat": generer_backup_cloud(),
    })


@bp_enterprise_grade.route("/api/v3/enterprise/predictif")
def api_enterprise_predictif():

    return jsonify({
        "success": True,
        "resultat": moteur_predictif(),
    })



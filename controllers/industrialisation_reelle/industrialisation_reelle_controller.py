from flask import Blueprint, jsonify, redirect, render_template, session
from services.industrialisation_reelle_service import (
    initialiser_industrialisation_reelle,
    dashboard_industrialisation_reelle,
)

bp_industrialisation_reelle = Blueprint("industrialisation_reelle", __name__)


@bp_industrialisation_reelle.route("/industrialisation-reelle")
def industrialisation_reelle_index():

    if not session.get("user_id"):
        return redirect("/login")

    initialiser_industrialisation_reelle()
    stats = dashboard_industrialisation_reelle()

    return render_template(
        "industrialisation_reelle_v3.html",
        stats=stats,
    )


@bp_industrialisation_reelle.route("/api/v3/dashboard")
def api_v3_dashboard():

    try:
        initialiser_industrialisation_reelle()
        stats = dashboard_industrialisation_reelle()

        return jsonify({
            "success": True,
            "module": "industrialisation_reelle_v3",
            "stats": stats,
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "module": "industrialisation_reelle_v3",
            "error": str(e),
        }), 500



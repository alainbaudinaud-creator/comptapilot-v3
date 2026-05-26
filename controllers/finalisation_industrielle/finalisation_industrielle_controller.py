from flask import Blueprint, jsonify, redirect, render_template, session
from services.finalisation_industrielle_service import (
    initialiser_finalisation_industrielle,
    dashboard_finalisation_industrielle,
)

bp_finalisation_industrielle = Blueprint("finalisation_industrielle", __name__)


@bp_finalisation_industrielle.route("/finalisation-industrielle")
def finalisation_industrielle_index():

    if not session.get("user_id"):
        return redirect("/login")

    initialiser_finalisation_industrielle()

    stats = dashboard_finalisation_industrielle()

    return render_template(
        "finalisation_industrielle_v3.html",
        stats=stats,
    )


@bp_finalisation_industrielle.route("/api/v3/finalisation")
def api_finalisation_industrielle():

    initialiser_finalisation_industrielle()

    stats = dashboard_finalisation_industrielle()

    return jsonify({
        "success": True,
        "module": "finalisation_industrielle_v3",
        "stats": stats,
    })



from flask import Blueprint, jsonify, redirect, render_template, session
from services.plateforme_reelle_service import (
    initialiser_plateforme_reelle,
    dashboard_plateforme_reelle,
)

bp_plateforme_reelle = Blueprint("plateforme_reelle", __name__)


@bp_plateforme_reelle.route("/plateforme-reelle")
def plateforme_reelle_index():

    if not session.get("user_id"):
        return redirect("/login")

    initialiser_plateforme_reelle()

    stats = dashboard_plateforme_reelle()

    return render_template(
        "plateforme_reelle_v3.html",
        stats=stats,
    )


@bp_plateforme_reelle.route("/api/v3/plateforme-reelle")
def api_plateforme_reelle():

    initialiser_plateforme_reelle()

    stats = dashboard_plateforme_reelle()

    return jsonify({
        "success": True,
        "module": "plateforme_reelle_v3",
        "stats": stats,
    })


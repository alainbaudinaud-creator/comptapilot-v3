from flask import Blueprint, jsonify, redirect, render_template, session
from services.experience_finale_service import (
    initialiser_experience_finale,
    dashboard_experience_finale,
)

bp_experience_finale = Blueprint("experience_finale", __name__)


@bp_experience_finale.route("/experience-finale")
def experience_finale_index():

    if not session.get("user_id"):
        return redirect("/login")

    initialiser_experience_finale()

    stats = dashboard_experience_finale()

    return render_template(
        "experience_finale_v3.html",
        stats=stats,
    )


@bp_experience_finale.route("/api/v3/experience-finale")
def api_experience_finale():

    initialiser_experience_finale()

    stats = dashboard_experience_finale()

    return jsonify({
        "success": True,
        "module": "experience_finale_v3",
        "stats": stats,
    })

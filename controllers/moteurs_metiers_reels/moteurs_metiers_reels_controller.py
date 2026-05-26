from flask import Blueprint, jsonify, redirect, render_template, session
from services.moteurs_metiers_reels_service import (
    initialiser_moteurs_metiers_reels,
    dashboard_moteurs_reels,
)

bp_moteurs_metiers_reels = Blueprint("moteurs_metiers_reels", __name__)


@bp_moteurs_metiers_reels.route("/moteurs-metiers-reels")
def moteurs_metiers_reels_index():

    if not session.get("user_id"):
        return redirect("/login")

    initialiser_moteurs_metiers_reels()

    stats = dashboard_moteurs_reels()

    return render_template(
        "moteurs_metiers_reels_v3.html",
        stats=stats,
    )


@bp_moteurs_metiers_reels.route("/api/v3/moteurs-reels")
def api_moteurs_reels():

    initialiser_moteurs_metiers_reels()

    stats = dashboard_moteurs_reels()

    return jsonify({
        "success": True,
        "module": "moteurs_metiers_reels_v3",
        "stats": stats,
    })


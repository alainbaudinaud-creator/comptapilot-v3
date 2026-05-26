from flask import Blueprint, jsonify, redirect, render_template, session
from services.automatisation_cabinet_service import (
    initialiser_automatisation_cabinet,
    dashboard_automatisation,
)

bp_automatisation_cabinet = Blueprint("automatisation_cabinet", __name__)


@bp_automatisation_cabinet.route("/automatisation-cabinet")
def automatisation_cabinet_index():

    if not session.get("user_id"):
        return redirect("/login")

    initialiser_automatisation_cabinet()

    stats = dashboard_automatisation()

    return render_template(
        "automatisation_cabinet_v3.html",
        stats=stats,
    )


@bp_automatisation_cabinet.route("/api/v3/automatisation")
def api_automatisation():

    initialiser_automatisation_cabinet()

    stats = dashboard_automatisation()

    return jsonify({
        "success": True,
        "module": "automatisation_cabinet_v3",
        "stats": stats,
    })


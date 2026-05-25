from flask import Blueprint, jsonify, redirect, render_template, session
from services.saas_realtime_service import (
    initialiser_saas_realtime,
    dashboard_saas_realtime,
)

bp_saas_realtime = Blueprint("saas_realtime", __name__)


@bp_saas_realtime.route("/saas-realtime")
def saas_realtime_index():

    if not session.get("user_id"):
        return redirect("/login")

    initialiser_saas_realtime()

    stats = dashboard_saas_realtime()

    return render_template(
        "saas_realtime_v3.html",
        stats=stats,
    )


@bp_saas_realtime.route("/api/v3/saas-realtime")
def api_saas_realtime():

    initialiser_saas_realtime()

    stats = dashboard_saas_realtime()

    return jsonify({
        "success": True,
        "module": "saas_realtime_v3",
        "stats": stats,
    })

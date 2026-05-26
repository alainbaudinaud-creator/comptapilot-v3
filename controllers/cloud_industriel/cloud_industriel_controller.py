from flask import Blueprint, jsonify, redirect, render_template, session
from services.cloud_industriel_service import (
    initialiser_cloud_industriel,
    dashboard_cloud_industriel,
)

bp_cloud_industriel = Blueprint("cloud_industriel", __name__)


@bp_cloud_industriel.route("/cloud-industriel")
def cloud_industriel_index():

    if not session.get("user_id"):
        return redirect("/login")

    initialiser_cloud_industriel()

    stats = dashboard_cloud_industriel()

    return render_template(
        "cloud_industriel_v3.html",
        stats=stats,
    )


@bp_cloud_industriel.route("/api/v3/cloud")
def api_cloud_industriel():

    initialiser_cloud_industriel()

    stats = dashboard_cloud_industriel()

    return jsonify({
        "success": True,
        "module": "cloud_industriel_v3",
        "stats": stats,
    })


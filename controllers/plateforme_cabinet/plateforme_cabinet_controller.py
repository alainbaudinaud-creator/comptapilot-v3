from flask import Blueprint, redirect, render_template, session
from services.plateforme_cabinet_service import dashboard_plateforme

bp_plateforme_cabinet = Blueprint("plateforme_cabinet", __name__)


@bp_plateforme_cabinet.route("/plateforme-cabinet")
def plateforme_cabinet_index():

    if not session.get("user_id"):
        return redirect("/login")

    stats = dashboard_plateforme()

    return render_template(
        "plateforme_cabinet_v3.html",
        stats=stats,
    )


from flask import Blueprint, jsonify, redirect, render_template, session
from services.commercialisation_saas_service import (
    initialiser_commercialisation_saas,
    dashboard_commercialisation,
)

bp_commercialisation_saas = Blueprint("commercialisation_saas", __name__)


@bp_commercialisation_saas.route("/commercialisation-saas")
def commercialisation_saas_index():

    if not session.get("user_id"):
        return redirect("/login")

    initialiser_commercialisation_saas()

    stats = dashboard_commercialisation()

    return render_template(
        "commercialisation_saas_v3.html",
        stats=stats,
    )


@bp_commercialisation_saas.route("/api/v3/commercialisation")
def api_commercialisation():

    initialiser_commercialisation_saas()

    stats = dashboard_commercialisation()

    return jsonify({
        "success": True,
        "module": "commercialisation_saas_v3",
        "stats": stats,
    })

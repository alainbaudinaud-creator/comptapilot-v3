from flask import Blueprint, jsonify, redirect, render_template, session
from services.produit_final_service import (
    initialiser_produit_final,
    dashboard_produit_final,
)

bp_produit_final = Blueprint("produit_final", __name__)


@bp_produit_final.route("/produit-final")
def produit_final_index():

    if not session.get("user_id"):
        return redirect("/login")

    initialiser_produit_final()
    stats = dashboard_produit_final()

    return render_template(
        "produit_final_v3.html",
        stats=stats,
    )


@bp_produit_final.route("/api/v3/produit-final")
def api_produit_final():

    initialiser_produit_final()
    stats = dashboard_produit_final()

    return jsonify({
        "success": True,
        "module": "produit_final_v3",
        "stats": stats,
    })


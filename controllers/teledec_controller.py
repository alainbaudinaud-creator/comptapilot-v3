
from flask import Blueprint, render_template, request, redirect, url_for

from services.teledec_gateway_service import (
    historique,
    preparer_dossier_teledec,
    envoyer_a_teledec_simulation,
    envoyer_client_simulation
)

bp_teledec = Blueprint("teledec", __name__)

@bp_teledec.route("/teledec")
def teledec_home():
    return render_template("teledec/index.html", rows=historique())

@bp_teledec.route("/teledec/preparer")
def teledec_preparer():
    preparer_dossier_teledec()
    return redirect(url_for("teledec.teledec_home"))

@bp_teledec.route("/teledec/envoyer")
def teledec_envoyer():
    envoyer_a_teledec_simulation()
    return redirect(url_for("teledec.teledec_home"))

@bp_teledec.route("/teledec/client", methods=["GET", "POST"])
def teledec_client():
    if request.method == "POST":
        email = request.form.get("email")
        message = request.form.get("message")
        envoyer_client_simulation(email, message)
        return redirect(url_for("teledec.teledec_home"))

    return render_template("teledec/client.html")



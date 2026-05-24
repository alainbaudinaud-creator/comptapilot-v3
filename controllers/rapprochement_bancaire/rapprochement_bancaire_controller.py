from flask import Blueprint, redirect, render_template, session

bp_rapprochement_bancaire = Blueprint("rapprochement_bancaire", __name__)


@bp_rapprochement_bancaire.route("/rapprochement-bancaire")
def rapprochement_bancaire_index():

    if not session.get("user_id"):
        return redirect("/login")

    return render_template("rapprochement_bancaire_v3.html")

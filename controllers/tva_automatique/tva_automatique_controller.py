from flask import Blueprint, redirect, render_template, session

bp_tva_automatique = Blueprint("tva_automatique", __name__)


@bp_tva_automatique.route("/tva-automatique")
def tva_automatique_index():

    if not session.get("user_id"):
        return redirect("/login")

    return render_template("tva_automatique_v3.html")



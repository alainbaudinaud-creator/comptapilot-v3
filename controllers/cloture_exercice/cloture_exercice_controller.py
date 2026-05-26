from flask import Blueprint, redirect, render_template, session

bp_cloture_exercice = Blueprint("cloture_exercice", __name__)


@bp_cloture_exercice.route("/cloture-exercice")
def cloture_exercice_index():

    if not session.get("user_id"):
        return redirect("/login")

    return render_template("cloture_exercice_v3.html")


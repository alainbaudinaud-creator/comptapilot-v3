from flask import Blueprint, redirect, render_template, session

bp_pre_ecritures_ia = Blueprint("pre_ecritures_ia", __name__)


@bp_pre_ecritures_ia.route("/pre-ecritures-ia")
def pre_ecritures_ia_index():

    if not session.get("user_id"):
        return redirect("/login")

    return render_template("pre_ecritures_ia_v3.html")



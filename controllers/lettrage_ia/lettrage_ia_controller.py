from flask import Blueprint, redirect, render_template, session

bp_lettrage_ia = Blueprint("lettrage_ia", __name__)


@bp_lettrage_ia.route("/lettrage-ia")
def lettrage_ia_index():

    if not session.get("user_id"):
        return redirect("/login")

    return render_template("lettrage_ia_v3.html")

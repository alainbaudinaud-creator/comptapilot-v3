from flask import Blueprint, redirect, render_template, session

bp_ocr_comptable = Blueprint("ocr_comptable", __name__)


@bp_ocr_comptable.route("/ocr-comptable")
def ocr_comptable_index():

    if not session.get("user_id"):
        return redirect("/login")

    return render_template("ocr_comptable_v3.html")

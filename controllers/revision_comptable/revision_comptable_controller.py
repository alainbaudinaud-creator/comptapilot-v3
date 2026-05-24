from flask import Blueprint, redirect, render_template, session

bp_revision_comptable = Blueprint("revision_comptable", __name__)


@bp_revision_comptable.route("/revision-comptable")
def revision_comptable_index():

    if not session.get("user_id"):
        return redirect("/login")

    return render_template("revision_comptable_v3.html")

from flask import Blueprint, redirect, render_template, session

bp_import_client = Blueprint("import_client", __name__)


@bp_import_client.route("/import-client")
def import_client_index():

    if not session.get("user_id"):
        return redirect("/login")

    return render_template("import_client_v3.html")



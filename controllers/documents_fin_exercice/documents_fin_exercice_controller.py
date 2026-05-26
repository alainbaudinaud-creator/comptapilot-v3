from flask import Blueprint, redirect, render_template, session

bp_documents_fin_exercice = Blueprint("documents_fin_exercice", __name__)


@bp_documents_fin_exercice.route("/documents-fin-exercice")
def documents_fin_exercice_index():

    if not session.get("user_id"):
        return redirect("/login")

    return render_template("documents_fin_exercice_v3.html")


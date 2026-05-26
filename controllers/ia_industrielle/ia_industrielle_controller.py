from flask import Blueprint, redirect, render_template, session
from services.ia_industrielle_service import dashboard_ia

bp_ia_industrielle = Blueprint("ia_industrielle", __name__)


@bp_ia_industrielle.route("/ia-industrielle")
def ia_industrielle_index():

    if not session.get("user_id"):
        return redirect("/login")

    stats = dashboard_ia()

    return render_template(
        "ia_industrielle_v3.html",
        stats=stats,
    )



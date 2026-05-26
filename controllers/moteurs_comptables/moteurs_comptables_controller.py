from flask import Blueprint, redirect, render_template, session
from services.moteurs_comptables_service import (
    stats_moteurs_comptables,
    generer_balance,
    generer_grand_livre,
    generer_tva_ca3,
    exporter_fec_demo,
)

bp_moteurs_comptables = Blueprint("moteurs_comptables", __name__)


@bp_moteurs_comptables.route("/moteurs-comptables")
def moteurs_comptables_index():

    if not session.get("user_id"):
        return redirect("/login")

    stats = stats_moteurs_comptables()
    balance = generer_balance()
    grand_livre = generer_grand_livre()
    tva = generer_tva_ca3()
    fec_path = exporter_fec_demo()

    return render_template(
        "moteurs_comptables_v3.html",
        stats=stats,
        balance=balance,
        grand_livre=grand_livre,
        tva=tva,
        fec_path=fec_path,
    )



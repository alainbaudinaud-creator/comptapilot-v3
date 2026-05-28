from flask import Blueprint, render_template
from sqlalchemy import text
from database import engine

bp_bilan = Blueprint("bilan_auto", __name__)

@bp_bilan.route("/bilan")
def bilan():

    rows = []

    try:
        with engine.begin() as conn:
            rows = conn.execute(text("""
                SELECT
                    numero,
                    libelle,
                    type,
                    solde
                FROM vue_bilan_postgres
                ORDER BY numero
            """)).fetchall()

    except Exception as e:
        print("BILAN WARNING:", e)

    return render_template(
        "comptabilite/bilan.html",
        rows=rows
    )

from flask import Blueprint, render_template
from sqlalchemy import text
from database import engine

bp_resultat = Blueprint("resultat_auto", __name__)

@bp_resultat.route("/compte-resultat")
def resultat():

    rows = []

    try:
        with engine.begin() as conn:
            rows = conn.execute(text("""
                SELECT
                    numero,
                    libelle,
                    type,
                    debit,
                    credit,
                    solde
                FROM vue_compte_resultat_postgres
                ORDER BY numero
            """)).fetchall()

    except Exception as e:
        print("COMPTE RESULTAT WARNING:", e)

    return render_template(
        "comptabilite/resultat.html",
        rows=rows
    )

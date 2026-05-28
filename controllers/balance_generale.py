from flask import Blueprint, render_template
from sqlalchemy import text
from database import engine

bp_balance = Blueprint("bp_balance", __name__)


@bp_balance.route("/balance")
def balance():

    rows = []

    try:
        with engine.begin() as conn:
            rows = conn.execute(text("""
                SELECT
                    numero AS compte,
                    libelle,
                    debit,
                    credit,
                    solde
                FROM vue_balance_postgres
                ORDER BY numero
            """)).fetchall()

    except Exception as e:
        print("BALANCE WARNING:", e)
        rows = []

    return render_template(
        "comptabilite/balance.html",
        rows=rows
    )

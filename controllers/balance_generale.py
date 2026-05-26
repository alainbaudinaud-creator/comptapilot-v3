from flask import Blueprint, render_template
import sqlite3

bp_balance = Blueprint("bp_balance", __name__)

@bp_balance.route("/balance")
def balance():

    rows = []

    try:
        conn = sqlite3.connect("db.sqlite")
        cur = conn.cursor()

        rows = cur.execute("""
            SELECT compte, libelle, debit, credit, solde
            FROM vue_balance
        """).fetchall()

        conn.close()

    except Exception as e:
        print("BALANCE WARNING:", e)
        rows = []

    return render_template(
        "comptabilite/balance.html",
        rows=rows
    )


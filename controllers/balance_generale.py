
from flask import Blueprint, render_template
import sqlite3

bp_balance = Blueprint("balance_generale", __name__)

@bp_balance.route("/balance")
def balance():
    con = sqlite3.connect("db.sqlite")
    cur = con.cursor()

    rows = cur.execute("""
        SELECT *
        FROM vue_balance
        ORDER BY numero
    """).fetchall()

    con.close()

    return render_template("comptabilite/balance.html", rows=rows)

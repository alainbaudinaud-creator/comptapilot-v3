from flask import Blueprint, render_template
import sqlite3

bp_bilan = Blueprint("bilan_auto", __name__)

@bp_bilan.route("/bilan")
def bilan():
    rows = []

    try:
        con = sqlite3.connect("db.sqlite")
        cur = con.cursor()
        rows = cur.execute("""
            SELECT *
            FROM vue_bilan
        """).fetchall()
        con.close()
    except Exception as e:
        print("BILAN WARNING:", e)
        rows = []

    return render_template("comptabilite/bilan.html", rows=rows)


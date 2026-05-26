from flask import Blueprint, render_template
import sqlite3

bp_gl = Blueprint("grand_livre_auto", __name__)

@bp_gl.route("/grand-livre")
def grand_livre():
    rows = []

    try:
        con = sqlite3.connect("db.sqlite")
        cur = con.cursor()

        rows = cur.execute("""
            SELECT *
            FROM vue_grand_livre
            ORDER BY date_ecriture
        """).fetchall()

        con.close()

    except Exception as e:
        print("GRAND LIVRE WARNING:", e)
        rows = []

    return render_template("comptabilite/grand_livre.html", rows=rows)


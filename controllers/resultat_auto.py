from flask import Blueprint, render_template
import sqlite3

bp_resultat = Blueprint("resultat_auto", __name__)

@bp_resultat.route("/compte-resultat")
def resultat():
    rows = []

    try:
        con = sqlite3.connect("db.sqlite")
        cur = con.cursor()
        rows = cur.execute("""
            SELECT *
            FROM vue_compte_resultat
            ORDER BY numero
        """).fetchall()
        con.close()
    except Exception as e:
        print("COMPTE RESULTAT WARNING:", e)
        rows = []

    return render_template("comptabilite/resultat.html", rows=rows)

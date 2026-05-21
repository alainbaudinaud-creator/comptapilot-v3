
from flask import Blueprint, render_template
import sqlite3

bp_resultat = Blueprint("resultat_auto", __name__)

@bp_resultat.route("/compte-resultat")
def resultat():
    con = sqlite3.connect("db.sqlite")
    cur = con.cursor()

    rows = cur.execute("""
        SELECT *
        FROM vue_compte_resultat
        ORDER BY numero
    """).fetchall()

    con.close()

    return render_template("comptabilite/resultat.html", rows=rows)

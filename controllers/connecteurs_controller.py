
import sqlite3
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for

bp_connecteurs = Blueprint("connecteurs", __name__)

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

@bp_connecteurs.route("/connecteurs", methods=["GET", "POST"])
def connecteurs():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    if request.method == "POST":
        cur.execute("""
        INSERT INTO connecteurs_externes
        (type_connecteur, nom, mode, url, identifiant, secret, actif)
        VALUES (?, ?, ?, ?, ?, ?, 1)
        """, (
            request.form.get("type_connecteur"),
            request.form.get("nom"),
            request.form.get("mode"),
            request.form.get("url"),
            request.form.get("identifiant"),
            request.form.get("secret"),
        ))
        con.commit()
        con.close()
        return redirect(url_for("connecteurs.connecteurs"))

    rows = cur.execute("""
        SELECT id, type_connecteur, nom, mode, url, identifiant, actif
        FROM connecteurs_externes
        ORDER BY id DESC
    """).fetchall()

    con.close()
    return render_template("connecteurs/index.html", rows=rows)



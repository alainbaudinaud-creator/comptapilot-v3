
import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

def analyser_risque_fiscal():

    con = sqlite3.connect(DB)
    cur = con.cursor()

    alertes = []

    rows = cur.execute("""
        SELECT numero, libelle
        FROM plan_comptable
    """).fetchall()

    if len(rows) < 100:
        alertes.append("Plan comptable incomplet")

    ecritures = cur.execute("""
        SELECT COUNT(*)
        FROM ecritures
    """).fetchone()[0]

    if ecritures == 0:
        alertes.append("Aucune écriture")

    con.close()

    return {
        "score": max(0, 100 - len(alertes)*15),
        "alertes": alertes
    }

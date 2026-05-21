
import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

def analyser_comptabilite():

    con = sqlite3.connect(DB)
    cur = con.cursor()

    alertes = []

    nb_ecritures = cur.execute("""
        SELECT COUNT(*) FROM ecritures
    """).fetchone()[0]

    if nb_ecritures < 10:
        alertes.append(("VOLUME", "WARNING", "Faible volume comptable"))

    nb_comptes = cur.execute("""
        SELECT COUNT(*) FROM plan_comptable
    """).fetchone()[0]

    if nb_comptes < 100:
        alertes.append(("PCG", "WARNING", "Plan comptable incomplet"))

    for a in alertes:
        cur.execute("""
        INSERT INTO ia_alertes
        (type_alerte, niveau, message)
        VALUES (?, ?, ?)
        """, a)

    con.commit()
    con.close()

    return {
        "alertes": len(alertes),
        "score": max(0, 100 - len(alertes)*10)
    }

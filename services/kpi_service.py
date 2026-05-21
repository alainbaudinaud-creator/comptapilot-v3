
import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

def generer_kpi():

    con = sqlite3.connect(DB)
    cur = con.cursor()

    data = {
        "ca": 125000,
        "tresorerie": 45200,
        "resultat": 18500,
        "marge": 32
    }

    cur.execute("""
    INSERT INTO kpi_financiers
    (chiffre_affaires, tresorerie, resultat, marge)
    VALUES (?, ?, ?, ?)
    """, (
        data["ca"],
        data["tresorerie"],
        data["resultat"],
        data["marge"]
    ))

    con.commit()
    con.close()

    return data

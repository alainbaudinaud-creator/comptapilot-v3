
import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

def generer_liasse():

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    INSERT INTO liasses_auto
    (
        dossier,
        exercice,
        statut,
        teledec
    )
    VALUES (?, ?, ?, ?)
    """, (
        "IFG SOLUTIONS",
        "2025",
        "GENEREE",
        0
    ))

    con.commit()
    con.close()

    return "OK"



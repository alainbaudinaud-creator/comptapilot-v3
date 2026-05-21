
import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

def generer_tva():

    con = sqlite3.connect(DB)
    cur = con.cursor()

    collectee = 24500
    deductible = 18200

    payer = collectee - deductible

    cur.execute("""
    INSERT INTO tva_auto
    (
        dossier,
        periode,
        tva_collectee,
        tva_deductible,
        tva_a_payer
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        "IFG SOLUTIONS",
        "05/2026",
        collectee,
        deductible,
        payer
    ))

    con.commit()
    con.close()

    return payer

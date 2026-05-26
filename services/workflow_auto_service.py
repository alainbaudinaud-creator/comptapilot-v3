
import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

def creer_tache(dossier, collaborateur, titre):

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    INSERT INTO workflow_taches
    (dossier, collaborateur, titre)
    VALUES (?, ?, ?)
    """, (dossier, collaborateur, titre))

    con.commit()
    con.close()

    return "TACHE_CREEE"



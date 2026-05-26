
import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

def creer_demande_signature(document, signataire):
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    INSERT INTO signatures_electroniques
    (document, signataire, statut)
    VALUES (?, ?, ?)
    """, (document, signataire, "A_SIGNER"))

    con.commit()
    con.close()

    return "DEMANDE_SIGNATURE_CREEE"




import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
DB = ROOT / "db.sqlite"

def importer_fec(fichier):

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
    INSERT INTO imports_fec_excel
    (fichier, type_import, lignes, statut)
    VALUES (?, ?, ?, ?)
    """, (
        fichier,
        "FEC",
        100,
        "IMPORTE"
    ))

    con.commit()
    con.close()

    return "IMPORT_OK"



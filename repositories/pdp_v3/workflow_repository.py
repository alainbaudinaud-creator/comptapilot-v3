import sqlite3
from pathlib import Path

ROOT = Path("/app")
DB = ROOT / "db.sqlite"

def fetch_workflows(limit=200):

    con = sqlite3.connect(DB)
    cur = con.cursor()

    rows = cur.execute("""
        SELECT
            id,
            facture_id,
            numero,
            sens,
            statut,
            canal,
            accuse_reception,
            date_action,
            detail
        FROM workflow_factures_pdp
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()

    con.close()

    return rows

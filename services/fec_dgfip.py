
import sqlite3
import csv
from datetime import datetime

def export_fec_dgfip(db="db.sqlite"):

    con = sqlite3.connect(db)
    cur = con.cursor()

    fichier = f"FEC_DGFIP_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    rows = cur.execute("""
        SELECT
            e.journal,
            e.date_ecriture,
            e.piece,
            e.libelle,
            pc.numero,
            pc.libelle,
            e.debit,
            e.credit
        FROM ecritures e
        LEFT JOIN plan_comptable pc
            ON pc.id = e.compte_id
        ORDER BY e.date_ecriture
    """).fetchall()

    with open(fichier, "w", newline="", encoding="utf-8") as f:

        w = csv.writer(f, delimiter="|")

        w.writerow([
            "JournalCode",
            "EcritureDate",
            "PieceRef",
            "EcritureLib",
            "CompteNum",
            "CompteLib",
            "Debit",
            "Credit"
        ])

        for r in rows:
            w.writerow(r)

    con.close()

    return fichier


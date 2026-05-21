
import sqlite3
import csv
from datetime import datetime

def export_fec(db_path="db.sqlite"):

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    fichier = f"FEC_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    rows = cur.execute("""
        SELECT
            e.date_ecriture,
            e.journal,
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
            "DateEcriture",
            "Journal",
            "Piece",
            "Libelle",
            "CompteNumero",
            "CompteLibelle",
            "Debit",
            "Credit"
        ])

        for r in rows:
            w.writerow(r)

    con.close()

    return fichier

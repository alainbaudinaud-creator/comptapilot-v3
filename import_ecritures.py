import sqlite3
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

sqlite_conn = sqlite3.connect("C:/Users/alain/mon-projet-agent/db.sqlite")
sqlite_cur = sqlite_conn.cursor()
sqlite_cur.execute("SELECT * FROM ecritures")
rows = sqlite_cur.fetchall()
sqlite_conn.close()

engine = create_engine(os.getenv("DATABASE_URL"))

with engine.begin() as conn:
    for row in rows:
        conn.execute(text("""
            INSERT INTO ecritures (
                id, date_ecriture, piece, libelle, debit, credit, societe_id, compte_id,
                rapproche, date_rapprochement, reference_banque, journal, lettrage,
                date_lettrage, rapproche_bancaire, exercice
            ) VALUES (
                :id, :date_ecriture, :piece, :libelle, :debit, :credit, :societe_id, :compte_id,
                :rapproche, :date_rapprochement, :reference_banque, :journal, :lettrage,
                :date_lettrage, :rapproche_bancaire, :exercice
            )
        """), {
            "id": row[0],
            "date_ecriture": row[1],
            "piece": row[2],
            "libelle": row[3],
            "debit": row[4],
            "credit": row[5],
            "societe_id": row[6],
            "compte_id": row[7],
            "rapproche": row[8],
            "date_rapprochement": row[9],
            "reference_banque": row[10],
            "journal": row[11],
            "lettrage": row[12],
            "date_lettrage": row[13],
            "rapproche_bancaire": row[14],
            "exercice": row[15],
        })

print(f"{len(rows)} écritures importées")




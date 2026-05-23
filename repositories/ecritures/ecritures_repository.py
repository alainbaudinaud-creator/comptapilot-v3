from sqlalchemy import text

from database import engine


def fetch_ecritures(limit=200):

    with engine.begin() as con:

        result = con.execute(text("""
            SELECT
                id,
                journal,
                date_ecriture,
                libelle,
                compte_id,
                debit,
                credit
            FROM ecritures
            ORDER BY id DESC
            LIMIT :limit
        """), {
            "limit": limit
        })

        return result.fetchall()


def fetch_stats_ecritures():

    with engine.begin() as con:

        result = con.execute(text("""
            SELECT
                COALESCE(SUM(debit), 0),
                COALESCE(SUM(credit), 0),
                COUNT(*)
            FROM ecritures
        """))

        row = result.fetchone()

        return {
            "total_debit": float(row[0] or 0),
            "total_credit": float(row[1] or 0),
            "nb_ecritures": int(row[2] or 0)
        }

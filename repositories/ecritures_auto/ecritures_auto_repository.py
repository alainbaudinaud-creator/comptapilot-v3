from sqlalchemy import text

from database import engine


def fetch_stats_ecritures_auto():

    with engine.begin() as con:

        result = con.execute(text("""
            SELECT
                COALESCE(SUM(debit), 0),
                COALESCE(SUM(credit), 0),
                COUNT(*)
            FROM ecritures_auto
        """))

        row = result.fetchone()

        return {
            "total_debit": float(row[0] or 0),
            "total_credit": float(row[1] or 0),
            "nb_ecritures_auto": int(row[2] or 0)
        }


def fetch_nombre_ecritures_auto():

    with engine.begin() as con:

        result = con.execute(text("""
            SELECT COUNT(*)
            FROM ecritures_auto
        """))

        return int(result.scalar() or 0)

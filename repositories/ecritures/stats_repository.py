from sqlalchemy import text

from database import engine


def fetch_global_stats():

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

def fetch_dashboard_financier_par_type():

    with engine.begin() as con:

        result = con.execute(text("""
            SELECT
                p.type,
                COALESCE(SUM(e.debit), 0),
                COALESCE(SUM(e.credit), 0)
            FROM ecritures e
            JOIN plan_comptable p
                ON e.compte_id = p.id
            GROUP BY p.type
        """))

        return result.fetchall()

def fetch_nombre_ecritures():

    with engine.begin() as con:

        result = con.execute(text("""
            SELECT COUNT(*)
            FROM ecritures
        """))

        return int(result.scalar() or 0)

def fetch_totaux_debit_credit():

    with engine.begin() as con:

        result = con.execute(text("""
            SELECT
                COALESCE(SUM(debit), 0),
                COALESCE(SUM(credit), 0)
            FROM ecritures
        """))

        row = result.fetchone()

        return {
            "total_debit": float(row[0] or 0),
            "total_credit": float(row[1] or 0)
        }

from sqlalchemy import text

from database import engine


def fetch_count(table_name: str) -> int:

    with engine.begin() as con:
        result = con.execute(text(f"""
            SELECT COUNT(*)
            FROM {table_name}
        """))

        return int(result.scalar() or 0)


def fetch_sum_debit_credit(table_name: str) -> dict:

    with engine.begin() as con:
        result = con.execute(text(f"""
            SELECT
                COALESCE(SUM(debit), 0),
                COALESCE(SUM(credit), 0),
                COUNT(*)
            FROM {table_name}
        """))

        row = result.fetchone()

        return {
            "total_debit": float(row[0] or 0),
            "total_credit": float(row[1] or 0),
            "count": int(row[2] or 0)
        }

def fetch_count_safe(table_name: str):

    try:
        return fetch_count(table_name)
    except Exception:
        return "table_absente"


from sqlalchemy import text

from database import engine


def fetch_societes():

    with engine.begin() as con:

        result = con.execute(text("""
            SELECT *
            FROM societes
            ORDER BY id
        """))

        return result.fetchall()


def fetch_societe_by_id(societe_id: int):

    with engine.begin() as con:

        result = con.execute(text("""
            SELECT *
            FROM societes
            WHERE id = :societe_id
            LIMIT 1
        """), {
            "societe_id": societe_id
        })

        return result.fetchone()



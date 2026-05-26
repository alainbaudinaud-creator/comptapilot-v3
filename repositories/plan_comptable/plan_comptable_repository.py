from sqlalchemy import text

from database import engine


def fetch_compte_by_numero(numero: str):

    with engine.begin() as con:

        result = con.execute(text("""
            SELECT
                id,
                numero,
                libelle,
                type
            FROM plan_comptable
            WHERE numero = :numero
            LIMIT 1
        """), {
            "numero": numero
        })

        return result.fetchone()


def create_compte_if_not_exists(numero: str, libelle: str, type_compte: str):

    compte = fetch_compte_by_numero(numero)

    if compte:
        return compte[0]

    with engine.begin() as con:

        result = con.execute(text("""
            INSERT INTO plan_comptable (
                numero,
                libelle,
                type
            )
            VALUES (
                :numero,
                :libelle,
                :type
            )
            RETURNING id
        """), {
            "numero": numero,
            "libelle": libelle,
            "type": type_compte
        })

        return result.scalar_one()


def fetch_plan_comptable():

    with engine.begin() as con:

        result = con.execute(text("""
            SELECT
                id,
                numero,
                libelle,
                type
            FROM plan_comptable
            ORDER BY numero
        """))

        return result.fetchall()



from services.db import get_connection


def lister_ecritures_bancaires():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT
            id,
            date_ecriture,
            piece,
            libelle,
            debit,
            credit,
            COALESCE(rapproche_bancaire, 0)
        FROM ecritures
        ORDER BY date_ecriture DESC
    """)

    ecritures = c.fetchall()
    conn.close()

    return ecritures


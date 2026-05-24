from db.postgres import get_connection


def create_client_onboarding(
    nom,
    siren,
    email,
    telephone
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO societes (
            nom,
            siren,
            email,
            telephone
        )
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """,
        (
            nom,
            siren,
            email,
            telephone
        )
    )

    societe_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return societe_id

from services.db_postgres import get_session
from sqlalchemy import text


def get_client_portal_summary(societe_id):

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                id,
                nom,
                siren,
                email,
                telephone
            FROM societes
            WHERE id = :societe_id
            """
        ),
        {
            "societe_id": societe_id
        }
    )

    row = result.fetchone()

    session.close()

    if not row:
        return None

    return {
        "societe_id": row[0],
        "nom": row[1],
        "siren": row[2],
        "email": row[3],
        "telephone": row[4]
    }



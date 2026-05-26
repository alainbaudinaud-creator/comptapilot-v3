from services.db_postgres import get_session
from sqlalchemy import text


def create_client_onboarding(
    nom,
    siren,
    email,
    telephone
):

    session = get_session()

    result = session.execute(
        text(
            """
            INSERT INTO societes (
                nom,
                siren,
                email,
                telephone
            )
            VALUES (
                :nom,
                :siren,
                :email,
                :telephone
            )
            RETURNING id
            """
        ),
        {
            "nom": nom,
            "siren": siren,
            "email": email,
            "telephone": telephone
        }
    )

    societe_id = result.fetchone()[0]

    session.commit()
    session.close()

    return societe_id



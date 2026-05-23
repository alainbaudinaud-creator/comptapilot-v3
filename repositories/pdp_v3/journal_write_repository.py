from sqlalchemy import text
from database import engine

def insert_journal_evenement(evenement: dict):
    with engine.begin() as con:
        result = con.execute(text("""
            INSERT INTO pdp_v3_journal_technique (
                type_evenement,
                reference,
                message,
                empreinte_sha256,
                date_evenement
            )
            VALUES (
                :type_evenement,
                :reference,
                :message,
                :empreinte_sha256,
                :date_evenement
            )
            RETURNING id
        """), {
            "type_evenement": evenement.get("type_evenement"),
            "reference": evenement.get("reference"),
            "message": evenement.get("message"),
            "empreinte_sha256": evenement.get("empreinte_sha256"),
            "date_evenement": evenement.get("date_evenement")
        })

        return result.scalar_one()

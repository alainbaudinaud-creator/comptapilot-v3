from sqlalchemy import text
from database import engine

def fetch_workflows(limit=200):

    with engine.begin() as con:

        result = con.execute(text("""
            SELECT
                id,
                facture_id,
                numero,
                sens,
                statut,
                canal,
                accuse_reception,
                date_action,
                detail
            FROM pdp_v3_workflows
            ORDER BY id DESC
            LIMIT :limit
        """), {
            "limit": limit
        })

        return result.fetchall()


from repositories.ecritures.stats_repository import (
    fetch_nombre_ecritures,
    fetch_totaux_debit_credit
)

from repositories.sql_stats_repository import fetch_count_safe
from sqlalchemy import text
from database import engine


def fetch_supervision_events(limit=100):

    with engine.begin() as con:

        result = con.execute(text("""
            SELECT
                date_event,
                module,
                statut,
                detail
            FROM supervision_systeme
            ORDER BY date_event DESC
            LIMIT :limit
        """), {
            "limit": limit
        })

        return result.fetchall()


def fetch_supervision_counts():

    return {
        "nb_ecritures": fetch_count_safe("ecritures"),
        "nb_precompta": fetch_count_safe("precompta_ia"),
        "nb_audit": fetch_count_safe("audit_actions")
    }


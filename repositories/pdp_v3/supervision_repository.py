from sqlalchemy import text
from database import engine

def fetch_supervision_stats():

    stats = {
        "workflows": 0,
        "archives": 0,
        "journal": 0
    }

    tables = {
        "workflows": "pdp_v3_workflows",
        "archives": "pdp_v3_archives",
        "journal": "pdp_v3_journal_technique"
    }

    with engine.begin() as con:

        for key, table in tables.items():

            try:
                result = con.execute(
                    text(f"SELECT COUNT(*) FROM {table}")
                )

                stats[key] = result.scalar()

            except Exception:
                stats[key] = 0

    return stats

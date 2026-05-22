from database.connection import get_sqlite_connection

def fetch_supervision_stats():

    stats = {
        "workflows": 0,
        "archives": 0,
        "journal": 0
    }

    con = get_sqlite_connection()
    cur = con.cursor()

    tables = {
        "workflows": "workflow_factures_pdp",
        "archives": "archives_probatoires",
        "journal": "journal_technique_pdp_v2"
    }

    for key, table in tables.items():
        try:
            stats[key] = cur.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]
        except Exception:
            stats[key] = 0

    con.close()

    return stats

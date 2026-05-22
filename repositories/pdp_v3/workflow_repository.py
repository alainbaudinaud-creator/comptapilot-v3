from database.connection import get_sqlite_connection

def fetch_workflows(limit=200):

    con = get_sqlite_connection()
    cur = con.cursor()

    rows = cur.execute("""
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
        FROM workflow_factures_pdp
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()

    con.close()

    return rows

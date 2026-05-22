from db_core.connection import get_sqlite_connection

def insert_workflow(workflow: dict):

    con = get_sqlite_connection()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS workflow_factures_pdp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facture_id INTEGER,
            numero TEXT,
            sens TEXT,
            statut TEXT,
            canal TEXT,
            accuse_reception TEXT,
            date_action TEXT,
            detail TEXT
        )
    """)

    cur.execute("""
        INSERT INTO workflow_factures_pdp (
            facture_id,
            numero,
            sens,
            statut,
            canal,
            accuse_reception,
            date_action,
            detail
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        workflow.get("facture_id"),
        workflow.get("numero"),
        workflow.get("sens"),
        workflow.get("statut"),
        workflow.get("canal"),
        workflow.get("accuse_reception"),
        workflow.get("date_action"),
        workflow.get("detail")
    ))

    workflow_id = cur.lastrowid

    con.commit()
    con.close()

    return workflow_id

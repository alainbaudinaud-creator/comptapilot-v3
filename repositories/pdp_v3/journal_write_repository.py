from db_core.connection import get_sqlite_connection

def insert_journal_evenement(evenement: dict):

    con = get_sqlite_connection()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS journal_technique_pdp_v3 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_evenement TEXT,
            reference TEXT,
            message TEXT,
            empreinte_sha256 TEXT,
            date_evenement TEXT
        )
    """)

    cur.execute("""
        INSERT INTO journal_technique_pdp_v3 (
            type_evenement,
            reference,
            message,
            empreinte_sha256,
            date_evenement
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        evenement.get("type_evenement"),
        evenement.get("reference"),
        evenement.get("message"),
        evenement.get("empreinte_sha256"),
        evenement.get("date_evenement")
    ))

    event_id = cur.lastrowid

    con.commit()
    con.close()

    return event_id

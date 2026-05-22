from db_core.connection import get_sqlite_connection

def insert_archive(archive: dict):

    con = get_sqlite_connection()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS archives_probatoires_pdp_v3 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_archive TEXT,
            empreinte_sha256 TEXT,
            date_archive TEXT,
            detail TEXT
        )
    """)

    cur.execute("""
        INSERT INTO archives_probatoires_pdp_v3 (
            nom_archive,
            empreinte_sha256,
            date_archive,
            detail
        )
        VALUES (?, ?, ?, ?)
    """, (
        archive.get("nom_archive"),
        archive.get("empreinte_sha256"),
        archive.get("date_archive"),
        archive.get("detail")
    ))

    archive_id = cur.lastrowid

    con.commit()
    con.close()

    return archive_id

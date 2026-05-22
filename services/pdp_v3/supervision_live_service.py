import sqlite3
from pathlib import Path

DB = Path("/app/db.sqlite")

def charger_supervision_temps_reel():

    data = {
        "workflows": [],
        "journal": [],
        "archives": [],
        "stats": {
            "workflows": 0,
            "journal": 0,
            "archives": 0
        }
    }

    try:

        con = sqlite3.connect(DB)
        con.row_factory = sqlite3.Row

        cur = con.cursor()

        workflows = cur.execute("""
            SELECT *
            FROM workflow_factures_pdp
            ORDER BY id DESC
            LIMIT 10
        """).fetchall()

        journal = cur.execute("""
            SELECT *
            FROM journal_technique_pdp_v3
            ORDER BY id DESC
            LIMIT 10
        """).fetchall()

        archives = cur.execute("""
            SELECT *
            FROM archives_probatoires_pdp_v3
            ORDER BY id DESC
            LIMIT 10
        """).fetchall()

        data["workflows"] = [dict(row) for row in workflows]
        data["journal"] = [dict(row) for row in journal]
        data["archives"] = [dict(row) for row in archives]

        data["stats"]["workflows"] = len(data["workflows"])
        data["stats"]["journal"] = len(data["journal"])
        data["stats"]["archives"] = len(data["archives"])

        con.close()

    except Exception as e:
        print("SUPERVISION TEMPS REEL WARNING:", e)

    return data

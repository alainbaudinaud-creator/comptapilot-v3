import sqlite3
from pathlib import Path
from dataclasses import asdict

from models.pdp_v3.workflow import WorkflowPDP

ROOT = Path("/app")
DB = ROOT / "db.sqlite"

def get_workflows(limit=200):
    workflows = []

    try:
        con = sqlite3.connect(DB)
        cur = con.cursor()

        rows = cur.execute("""
            SELECT id, facture_id, numero, sens, statut, canal, accuse_reception, date_action, detail
            FROM workflow_factures_pdp
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        for r in rows:
            workflow = WorkflowPDP(
                id=r[0],
                facture_id=r[1],
                numero=r[2],
                sens=r[3],
                statut=r[4],
                canal=r[5],
                accuse_reception=r[6],
                date_action=r[7],
                detail=r[8]
            )

            workflows.append(asdict(workflow))

        con.close()

    except Exception as e:
        print("PDP V3 SERVICE WORKFLOW WARNING:", e)

    return workflows

from dataclasses import asdict

from models.pdp_v3.workflow import WorkflowPDP
from repositories.pdp_v3.workflow_repository import fetch_workflows

def get_workflows(limit=200):
    workflows = []

    try:
        rows = fetch_workflows(limit=limit)

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

    except Exception as e:
        print("PDP V3 SERVICE WORKFLOW WARNING:", e)

    return workflows

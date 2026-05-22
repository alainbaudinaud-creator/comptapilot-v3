from datetime import datetime
import hashlib

from repositories.pdp_v3.archive_write_repository import insert_archive

def archiver_workflow_probatoire(workflow: dict):

    payload = str(workflow)

    empreinte = hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()

    archive = {
        "nom_archive": f"workflow_{workflow.get('id')}",
        "empreinte_sha256": empreinte,
        "date_archive": datetime.utcnow().isoformat(),
        "detail": f"Archive probatoire workflow {workflow.get('id')}"
    }

    archive_id = insert_archive(archive)

    archive["id"] = archive_id

    return archive

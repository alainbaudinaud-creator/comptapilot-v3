from datetime import datetime
import hashlib

from repositories.pdp_v3.journal_write_repository import insert_journal_evenement

def journaliser_evenement_pdp(
    type_evenement: str,
    reference: str,
    message: str
):

    payload = f"{type_evenement}|{reference}|{message}"

    empreinte = hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()

    evenement = {
        "type_evenement": type_evenement,
        "reference": reference,
        "message": message,
        "empreinte_sha256": empreinte,
        "date_evenement": datetime.utcnow().isoformat()
    }

    event_id = insert_journal_evenement(evenement)

    evenement["id"] = event_id

    return evenement


from datetime import datetime

from domain.pdp_v3.statuts import STATUT_DEPOT_EN_ATTENTE
from domain.pdp_v3.canaux import CANAL_TEST

def construire_workflow_facture(facture_id: int):

    return {
        "facture_id": facture_id,
        "numero": f"FACT-{facture_id}",
        "sens": "EMISSION",
        "statut": STATUT_DEPOT_EN_ATTENTE,
        "canal": CANAL_TEST,
        "accuse_reception": None,
        "date_action": datetime.utcnow().isoformat(),
        "detail": "Workflow PDP V3 initialisé"
    }

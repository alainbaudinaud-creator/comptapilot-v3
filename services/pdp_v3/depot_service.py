from services.factures.facture_service import charger_facture_metier

from services.pdp_v3.workflow_builder_service import construire_workflow_facture
from repositories.pdp_v3.workflow_write_repository import insert_workflow

from services.pdp_v3.journal_service import journaliser_evenement_pdp
from services.pdp_v3.archive_service import archiver_workflow_probatoire

def deposer_facture_pdp(facture_id: int):

    facture = charger_facture_metier(facture_id)

    if facture.get("statut") != "VALIDE":
        return {
            "success": False,
            "message": "Facture non valide pour dépôt PDP",
            "facture": facture
        }

    workflow = construire_workflow_facture(facture["id"])
    workflow["facture"] = facture

    workflow_id = insert_workflow(workflow)
    workflow["id"] = workflow_id

    journal = journaliser_evenement_pdp(
        type_evenement="DEPOT_PDP_CONTROLE",
        reference=str(workflow_id),
        message=f"Dépôt PDP contrôlé facture {facture['numero']}"
    )

    archive = archiver_workflow_probatoire(workflow)

    workflow["journal"] = journal
    workflow["archive"] = archive

    return {
        "success": True,
        "message": "Facture déposée dans le workflow PDP V3",
        "workflow": workflow
    }

def simuler_depot_facture(facture_id: int):
    return deposer_facture_pdp(facture_id)

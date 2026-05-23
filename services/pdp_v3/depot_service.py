from services.factures.facture_service import charger_facture_metier

from services.pdp_v3.workflow_builder_service import construire_workflow_facture
from repositories.pdp_v3.workflow_write_repository import insert_workflow

from services.pdp_v3.journal_service import journaliser_evenement_pdp
from services.pdp_v3.archive_service import archiver_workflow_probatoire

def simuler_depot_facture(facture_id: int):

    facture = charger_facture_metier(facture_id)

    workflow = construire_workflow_facture(
        facture["id"]
    )

    workflow["facture"] = facture

    workflow_id = insert_workflow(workflow)

    workflow["id"] = workflow_id

    journal = journaliser_evenement_pdp(
        type_evenement="DEPOT_PDP",
        reference=str(workflow_id),
        message=f"Dépôt PDP facture métier {facture['numero']}"
    )

    archive = archiver_workflow_probatoire(workflow)

    workflow["journal"] = journal
    workflow["archive"] = archive

    return workflow

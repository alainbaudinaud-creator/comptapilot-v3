from services.pdp_v3.workflow_builder_service import construire_workflow_facture
from repositories.pdp_v3.workflow_write_repository import insert_workflow

def simuler_depot_facture(facture_id: int):

    workflow = construire_workflow_facture(facture_id)

    workflow_id = insert_workflow(workflow)

    workflow["id"] = workflow_id

    return workflow

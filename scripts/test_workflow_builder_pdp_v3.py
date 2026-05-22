from services.pdp_v3.workflow_builder_service import construire_workflow_facture

workflow = construire_workflow_facture(123)

print("=== TEST WORKFLOW PDP V3 ===")
print(workflow)

required = [
    "facture_id",
    "numero",
    "statut",
    "canal"
]

for key in required:
    if key not in workflow:
        raise Exception(f"Champ manquant: {key}")

print("Workflow PDP V3 OK")

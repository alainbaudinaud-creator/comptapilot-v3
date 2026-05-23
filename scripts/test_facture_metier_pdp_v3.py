from services.pdp_v3.depot_service import simuler_depot_facture

workflow = simuler_depot_facture(9001)

print("=== TEST FACTURE METIER PDP V3 ===")
print(workflow)

if "facture" not in workflow:
    raise Exception("Facture métier absente")

if workflow["facture"]["numero"] != "FAC-9001":
    raise Exception("Numéro facture invalide")

print("Workflow facture métier OK")

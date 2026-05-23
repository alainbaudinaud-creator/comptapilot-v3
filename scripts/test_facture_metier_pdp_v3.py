from services.pdp_v3.depot_service import simuler_depot_facture

result = simuler_depot_facture(9001)

print("=== TEST FACTURE METIER PDP V3 ===")
print(result)

if not result.get("success"):
    raise Exception("Dépôt PDP métier échoué")

workflow = result.get("workflow")

if not workflow:
    raise Exception("Workflow absent")

if "facture" not in workflow:
    raise Exception("Facture métier absente")

if workflow["facture"]["numero"] != "FAC-9001":
    raise Exception("Numéro facture invalide")

print("Workflow facture métier OK")

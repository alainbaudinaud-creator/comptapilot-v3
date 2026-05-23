from services.factures.facture_service import charger_facture_metier

facture = charger_facture_metier(9101)

print("=== TEST FACTURE BASE PDP V3 ===")
print(facture)

if facture["numero"] != "FAC-9101":
    raise Exception("Numéro facture base invalide")

if facture["statut"] != "VALIDE":
    raise Exception("Statut facture invalide")

print("Facture base PDP V3 OK")

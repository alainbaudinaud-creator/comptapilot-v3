from app_refonte.services.pdp_premium_service import (
    creer_facture_electronique,
    valider_facture_pdp,
    changer_statut_facture,
    generer_evenement_pdp,
    preparer_e_reporting,
)

facture = creer_facture_electronique(
    numero="F2026-001",
    date_facture="2026-05-28",
    emetteur_siret="12345678901234",
    client_siret="98765432109876",
    montant_ht=1000,
    montant_tva=200,
)

assert facture["montant_ttc"] == 1200.0
assert facture["statut"] == "BROUILLON"

validation = valider_facture_pdp(facture)
assert validation["valide"] is True

facture = changer_statut_facture(facture, "TRANSMISE_PDP")
assert facture["statut"] == "TRANSMISE_PDP"

event = generer_evenement_pdp(facture, "TRANSMISSION")
assert event["facture_numero"] == "F2026-001"
assert event["action"] == "TRANSMISSION"

reporting = preparer_e_reporting([facture])
assert reporting["nombre_factures"] == 1
assert reporting["total_ttc"] == 1200.0

print("TESTS PDP PREMIUM OK")

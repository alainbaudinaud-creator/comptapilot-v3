from app_refonte.services.rapprochement_bancaire_service import (
    scorer_rapprochement,
    proposer_rapprochements,
    generer_ecriture_banque_si_absente,
)

operation = {
    "date_operation": "2026-05-28",
    "libelle": "VIREMENT CLIENT DEMO SAS",
    "montant": 1200,
}

ecriture = {
    "date_ecriture": "2026-05-28",
    "libelle": "Client Demo SAS",
    "debit": 1200,
    "credit": 0,
}

score = scorer_rapprochement(operation, ecriture)
assert score >= 70

props = proposer_rapprochements([operation], [ecriture])
assert props[0]["statut"] == "PROPOSE"
assert props[0]["score"] >= 70

ecriture_auto = generer_ecriture_banque_si_absente({
    "date_operation": "2026-05-28",
    "libelle": "Frais bancaires",
    "montant": -25.50,
})

assert ecriture_auto["journal"] == "BQ"
assert len(ecriture_auto["lignes"]) == 2
assert ecriture_auto["lignes"][0]["compte"] == "471000"
assert ecriture_auto["lignes"][1]["compte"] == "512000"

print("TESTS RAPPROCHEMENT BANCAIRE OK")

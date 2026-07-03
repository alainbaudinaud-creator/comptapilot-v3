from app_refonte.services.emprunts_premium_service import (
    calcul_mensualite,
    generer_tableau_emprunt,
    generer_ecritures_emprunt,
)

mensualite = calcul_mensualite(
    capital=100000,
    taux_annuel=4,
    duree_mois=240,
)

assert mensualite > 0

tableau = generer_tableau_emprunt(
    capital=100000,
    taux_annuel=4,
    duree_mois=240,
)

assert len(tableau["tableau"]) == 240

premiere = tableau["tableau"][0]

assert premiere["interets"] > 0
assert premiere["remboursement_capital"] > 0

derniere = tableau["tableau"][-1]

assert round(derniere["capital_restant_du"], 2) == 0

ecritures = generer_ecritures_emprunt(tableau)

assert len(ecritures) == 240
assert len(ecritures[0]["lignes"]) == 3

print("TESTS EMPRUNTS PREMIUM OK")

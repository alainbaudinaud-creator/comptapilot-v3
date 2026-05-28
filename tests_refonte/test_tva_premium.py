from app_refonte.services.tva_premium_service import (
    calcul_tva,
    calcul_declaration_ca3,
    generer_ecriture_tva,
)

calc = calcul_tva(1000, "20")

assert calc["tva"] == 200.0
assert calc["ttc"] == 1200.0

ca3 = calcul_declaration_ca3([
    {"type": "COLLECTEE", "montant": 3000},
    {"type": "DEDUCTIBLE", "montant": 1200},
])

assert ca3["tva_collectee"] == 3000.0
assert ca3["tva_deductible"] == 1200.0
assert ca3["tva_nette"] == 1800.0
assert ca3["a_payer"] == 1800.0

ecriture = generer_ecriture_tva(ca3["tva_nette"])

assert ecriture["journal"] == "OD"
assert len(ecriture["lignes"]) == 2

print("TESTS TVA PREMIUM OK")

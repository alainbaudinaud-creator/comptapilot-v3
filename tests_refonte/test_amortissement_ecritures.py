from app_refonte.services.amortissement_ecritures_service import (
    generer_plan_amortissement,
    generer_ecritures_amortissement,
)

plan = generer_plan_amortissement(
    designation="Ordinateur portable",
    valeur_origine=2400,
    duree_mois=24,
)

assert plan["success"] is True
assert len(plan["plan"]) == 24

premiere = plan["plan"][0]
assert premiere["dotation"] == 100.0

derniere = plan["plan"][-1]
assert round(derniere["vnc"], 2) == 0

ecritures = generer_ecritures_amortissement(plan)

assert len(ecritures) == 24

premiere_ecriture = ecritures[0]

assert premiere_ecriture["journal"] == "OD"
assert len(premiere_ecriture["lignes"]) == 2

assert premiere_ecriture["lignes"][0]["debit"] == 100.0
assert premiere_ecriture["lignes"][1]["credit"] == 100.0

print("TESTS AMORTISSEMENTS OK")

from datetime import datetime, timedelta

from app_refonte.services.workflow_cabinet_service import (
    creer_tache,
    changer_statut,
    calculer_score_priorite,
    detecter_retards,
    generer_resume_cabinet,
)

tache = creer_tache(
    titre="Validation TVA client",
    collaborateur="Alice",
    priorite="CRITIQUE",
)

assert tache["statut"] == "A_FAIRE"

tache = changer_statut(tache, "EN_COURS")

assert tache["statut"] == "EN_COURS"

score = calculer_score_priorite(tache)

assert score == 100

retard = creer_tache(
    titre="Retard dossier",
    collaborateur="Bob",
    priorite="HAUTE",
    echeance=(datetime.utcnow() - timedelta(days=1)).isoformat(),
)

retards = detecter_retards([retard])

assert len(retards) == 1

resume = generer_resume_cabinet([
    tache,
    retard,
])

assert resume["total_taches"] == 2
assert resume["taches_en_retard"] == 1

print("TESTS WORKFLOW CABINET OK")

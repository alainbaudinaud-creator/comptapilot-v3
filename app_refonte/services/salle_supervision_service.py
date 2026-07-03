from app_refonte.services.taches_revision_service import charger_taches_revision
from app_refonte.services.taches_ia_service import charger_taches_ia
from app_refonte.services.workflow_cabinet_service import charger_workflow_cabinet

def charger_salle_supervision():
    kpis_workflow, workflow_rows = charger_workflow_cabinet()
    kpis_revision, revision_rows = charger_taches_revision()
    kpis_ia, ia_rows = charger_taches_ia()

    kpis = {
        "dossiers_actifs": kpis_workflow["ouverts"] + kpis_revision["ouvertes"],
        "alertes_bloquantes": kpis_revision["critiques"] + kpis_ia["critiques"],
        "retards": kpis_revision["retards"] if "retards" in kpis_revision else 0,
        "prets_visa": kpis_workflow["termines"],
        "prets_cloture": kpis_workflow["bloquants"],
        "score_global": round((kpis_workflow["termines"] / max(1,kpis_workflow["total"])) * 100)
    }

    dossiers = workflow_rows[:20]
    alertes = revision_rows[:20] + ia_rows[:20]
    charge = [{"profil": "Collaborateur", "dossiers": 5, "priorites": 2, "etat": "En cours"}]

    return kpis, dossiers, alertes, charge

from app_refonte.services.centre_decision_service import charger_centre_decision
from app_refonte.services.salle_supervision_service import charger_salle_supervision
from app_refonte.services.gestion_risques_service import charger_gestion_risques
from app_refonte.services.controle_interne_service import charger_controle_interne
from app_refonte.services.conformite_reglementaire_service import charger_conformite_reglementaire
from app_refonte.services.centre_qualite_service import charger_centre_qualite
from app_refonte.services.visa_expert_service import charger_visa_expert
from app_refonte.services.comite_cloture_service import charger_comite_cloture


def charger_orchestration_cabinet():
    decision_kpis, decisions, alertes_decision, priorites = charger_centre_decision()
    supervision_kpis, dossiers_supervision, alertes_supervision, charge = charger_salle_supervision()
    risques_kpis, risques, plans_risques = charger_gestion_risques()
    controle_kpis, risques_controle, controles, pistes = charger_controle_interne()
    conformite_kpis, obligations, risques_conformite, actions_conformite = charger_conformite_reglementaire()
    qualite_kpis, risques_qualite, controles_qualite = charger_centre_qualite()
    visa_kpis, dossiers_visa, validations = charger_visa_expert()
    cloture_kpis, dossiers_cloture, blocages, decisions_cloture = charger_comite_cloture()

    kpis = {
        "score_cabinet": decision_kpis["score_cabinet"],
        "score_supervision": supervision_kpis["score_global"],
        "score_risque": risques_kpis["score_global"],
        "score_controle": controle_kpis["score_controle"],
        "score_conformite": conformite_kpis["score_conformite"],
        "score_qualite": qualite_kpis["score_global"],
        "score_cloture": cloture_kpis["score_cloture"],
        "alertes_totales": (
            decision_kpis["alertes_globales"]
            + supervision_kpis["alertes_bloquantes"]
            + qualite_kpis["alertes_qualite"]
            + conformite_kpis["alertes_lcbft"]
        ),
        "dossiers_prioritaires": decision_kpis["dossiers_prioritaires"],
        "dossiers_prets_visa": visa_kpis["a_visa_ec"],
        "dossiers_prets_cloture": supervision_kpis["prets_cloture"],
    }

    synthese = {
        "decisions": decisions[:5],
        "dossiers_supervision": dossiers_supervision[:5],
        "risques": risques[:5],
        "blocages": blocages[:5],
        "priorites": priorites[:5],
    }

    return kpis, synthese

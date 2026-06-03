import os
from sqlalchemy import create_engine, text
from app_refonte.services.plan_action_ia_service import generer_plan_action_ia


def db_url():
    return os.getenv(
        "DATABASE_URL",
        "postgresql://comptapilot:comptapilot@postgres:5432/comptapilot"
    )


def generer_taches_depuis_plan_ia():
    plan = generer_plan_action_ia()
    actions = plan.get("actions", [])

    resultat = {
        "success": True,
        "nb_actions": len(actions),
        "nb_taches_creees": 0,
        "taches": []
    }

    engine = create_engine(db_url(), pool_pre_ping=True)

    with engine.begin() as conn:
        for action in actions:
            titre = "[IA] " + action.get("action", "Action IA à traiter")
            priorite = action.get("priorite", "NORMALE")

            row = conn.execute(text("""
                INSERT INTO taches_cabinet_v3
                (
                    client_id,
                    titre,
                    priorite,
                    statut,
                    echeance,
                    created_at
                )
                SELECT
                    1,
                    :titre,
                    :priorite,
                    'A_FAIRE',
                    CURRENT_DATE,
                    NOW()
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM taches_cabinet_v3
                    WHERE titre = :titre
                )
                RETURNING id, client_id, titre, priorite, statut, echeance, created_at
            """), {
                "titre": titre,
                "priorite": priorite
            }).mappings().first()

            if row:
                resultat["nb_taches_creees"] += 1
                resultat["taches"].append(dict(row))

    return resultat

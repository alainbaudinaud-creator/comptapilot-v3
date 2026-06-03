import os
from sqlalchemy import create_engine, text


def _database_url():
    return os.getenv(
        "DATABASE_URL",
        "postgresql://comptapilot:comptapilot@postgres:5432/comptapilot"
    )


VISAS_ATTENDUS = ["COLLABORATEUR", "CHEF_MISSION", "EXPERT_COMPTABLE"]


def charger_visas_cabinet(societe_id=1, exercice="2025"):
    data = {
        "societe_id": societe_id,
        "exercice": exercice,
        "visas_attendus": VISAS_ATTENDUS,
        "visas_valides": [],
        "nb_visas": 0,
        "nb_attendus": 3,
        "cloture_autorisee": False,
        "statut": "BLOQUE",
        "historique": []
    }

    try:
        engine = create_engine(_database_url(), pool_pre_ping=True)

        with engine.connect() as conn:
            rows = conn.execute(text("""
                SELECT
                    id,
                    type_visa,
                    utilisateur,
                    commentaire,
                    valide,
                    created_at
                FROM cabinet_visas
                WHERE societe_id = :societe_id
                  AND exercice = :exercice
                  AND valide = TRUE
                ORDER BY created_at ASC
            """), {
                "societe_id": societe_id,
                "exercice": exercice
            }).mappings().all()

        historique = []
        visas_valides = []

        for r in rows:
            type_visa = r["type_visa"]
            if type_visa in VISAS_ATTENDUS and type_visa not in visas_valides:
                visas_valides.append(type_visa)

            historique.append({
                "id": r["id"],
                "type_visa": type_visa,
                "utilisateur": r["utilisateur"],
                "commentaire": r["commentaire"],
                "created_at": str(r["created_at"])
            })

        data["visas_valides"] = visas_valides
        data["nb_visas"] = len(visas_valides)
        data["historique"] = historique
        data["cloture_autorisee"] = len(visas_valides) == len(VISAS_ATTENDUS)

        if data["cloture_autorisee"]:
            data["statut"] = "CLOTURE_AUTORISEE"
        elif data["nb_visas"] == 2:
            data["statut"] = "VISA_EC_REQUIS"
        elif data["nb_visas"] == 1:
            data["statut"] = "CHEF_MISSION_REQUIS"
        else:
            data["statut"] = "REVISION_A_FINALISER"

    except Exception as e:
        data["erreur"] = str(e)

    return data

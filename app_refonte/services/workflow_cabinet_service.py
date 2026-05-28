from datetime import datetime


STATUTS = [
    "A_FAIRE",
    "EN_COURS",
    "EN_VALIDATION",
    "TERMINE",
]

PRIORITES = [
    "BASSE",
    "NORMALE",
    "HAUTE",
    "CRITIQUE",
]


def creer_tache(
    titre,
    collaborateur,
    priorite="NORMALE",
    echeance=None,
):
    return {
        "titre": titre,
        "collaborateur": collaborateur,
        "priorite": priorite,
        "statut": "A_FAIRE",
        "date_creation": datetime.utcnow().isoformat(),
        "echeance": echeance,
    }


def changer_statut(tache, nouveau_statut):
    if nouveau_statut not in STATUTS:
        raise ValueError("Statut invalide")

    tache["statut"] = nouveau_statut

    return tache


def calculer_score_priorite(tache):
    mapping = {
        "BASSE": 10,
        "NORMALE": 30,
        "HAUTE": 70,
        "CRITIQUE": 100,
    }

    return mapping.get(tache.get("priorite"), 0)


def detecter_retards(taches):
    now = datetime.utcnow()

    retards = []

    for tache in taches:

        echeance = tache.get("echeance")

        if not echeance:
            continue

        dt = datetime.fromisoformat(echeance)

        if dt < now and tache.get("statut") != "TERMINE":
            retards.append(tache)

    return retards


def generer_resume_cabinet(taches):
    total = len(taches)

    terminees = len([
        t for t in taches
        if t["statut"] == "TERMINE"
    ])

    critiques = len([
        t for t in taches
        if t["priorite"] == "CRITIQUE"
    ])

    retards = len(detecter_retards(taches))

    return {
        "total_taches": total,
        "taches_terminees": terminees,
        "taches_critiques": critiques,
        "taches_en_retard": retards,
    }

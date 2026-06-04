from sqlalchemy import text
from database import engine


def verifier_autorisation_fiscale():
    with engine.connect() as conn:
        stats = conn.execute(text("""
            SELECT
                (SELECT COUNT(*) FROM exercices_v3) AS exercices,
                (SELECT COUNT(*) FROM teletransmissions_fiscales_v3) AS teletransmissions,
                (SELECT COUNT(*) FROM cabinet_visas WHERE valide IS TRUE) AS visas,
                (SELECT COUNT(*) FROM pieces_v3 WHERE statut_validation <> 'VALIDEE') AS pieces_a_valider,
                (SELECT COUNT(*) FROM taches_cabinet_v3
                 WHERE UPPER(COALESCE(priorite,'')) IN ('CRITIQUE','HAUTE','URGENT')
                 AND UPPER(COALESCE(statut,'')) NOT IN ('TERMINE','TERMINEE','VALIDEE','VALIDÉE','OK')) AS points_bloquants
        """)).mappings().first()

    pieces = int(stats["pieces_a_valider"] or 0)
    bloquants = int(stats["points_bloquants"] or 0)
    visas = int(stats["visas"] or 0)

    autorise = pieces == 0 and bloquants == 0 and visas > 0

    return {
        "success": True,
        "autorise": autorise,
        "statut": "AUTORISE" if autorise else "BLOQUE",
        "controles": {
            "exercices": int(stats["exercices"] or 0),
            "teletransmissions": int(stats["teletransmissions"] or 0),
            "visas_valides": visas,
            "pieces_a_valider": pieces,
            "points_bloquants": bloquants,
        },
        "message": "Autorisation fiscale validée" if autorise else "Autorisation fiscale bloquée par contrôles métier",
    }

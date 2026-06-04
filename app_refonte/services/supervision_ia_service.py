from sqlalchemy import text
from database import engine


def charger_supervision_ia():
    with engine.connect() as conn:
        k = conn.execute(text("""
            SELECT
                COUNT(*) AS pieces,
                COUNT(*) FILTER (WHERE statut_ocr = 'TRAITE') AS ocr_traite,
                COUNT(*) FILTER (WHERE statut_validation <> 'VALIDEE') AS a_valider,
                COUNT(*) FILTER (WHERE analyse_ia IS NOT NULL) AS analyses_ia
            FROM pieces_v3
        """)).mappings().first()

        rows = conn.execute(text("""
            SELECT
                COALESCE(c.raison_sociale, 'Client non identifié') AS client,
                COALESCE(p.nom_fichier, 'Pièce') AS fichier,
                COALESCE(p.type_piece, 'NON_CLASSE') AS type_piece,
                COALESCE(p.statut_ocr, 'A_TRAITER') AS statut_ocr,
                COALESCE(p.statut_validation, 'A_VALIDER') AS statut_validation
            FROM pieces_v3 p
            LEFT JOIN clients_v3 c ON c.id = p.client_id
            ORDER BY p.created_at DESC, p.id DESC
            LIMIT 20
        """)).mappings().all()

    pieces = int(k["pieces"] or 0)
    a_valider = int(k["a_valider"] or 0)

    kpis = {
        "pieces": pieces,
        "ocr_traite": int(k["ocr_traite"] or 0),
        "a_valider": a_valider,
        "analyses_ia": int(k["analyses_ia"] or 0),
        "score_ia": 100 if pieces == 0 else round(((pieces - a_valider) / pieces) * 100),
    }

    controles = [
        [r["client"], r["fichier"], r["type_piece"], r["statut_ocr"], r["statut_validation"]]
        for r in rows
    ]

    return kpis, controles

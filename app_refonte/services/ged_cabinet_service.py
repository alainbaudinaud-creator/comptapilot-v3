from sqlalchemy import text

from database import engine


def charger_ged_cabinet():
    with engine.connect() as conn:
        stats = conn.execute(text("""
            SELECT
                COUNT(*) AS documents,
                COUNT(*) FILTER (WHERE statut_ocr = 'TRAITE') AS ocr,
                COUNT(*) FILTER (WHERE statut_validation = 'A_VALIDER') AS a_valider,
                COUNT(*) FILTER (WHERE statut_validation <> 'VALIDEE') AS manquants
            FROM pieces_v3
        """)).mappings().first()

        dossiers_rows = conn.execute(text("""
            SELECT
                COALESCE(type_piece, 'NON_CLASSE') AS type_piece,
                COUNT(*) AS documents,
                COUNT(*) FILTER (WHERE statut_validation <> 'VALIDEE') AS alertes
            FROM pieces_v3
            GROUP BY COALESCE(type_piece, 'NON_CLASSE')
            ORDER BY COUNT(*) DESC
        """)).mappings().all()

        pieces_rows = conn.execute(text("""
            SELECT
                p.nom_fichier,
                COALESCE(p.type_piece, 'NON_CLASSE') AS type_piece,
                COALESCE(p.statut_validation, 'A_VALIDER') AS statut_validation,
                COALESCE(p.statut_ocr, 'A_TRAITER') AS statut_ocr,
                COALESCE(c.raison_sociale, 'Client non identifié') AS client,
                COALESCE(p.analyse_ia->>'controle', 'Contrôle à réaliser') AS controle,
                COALESCE(p.analyse_ia->>'score', '-') AS score_ia
            FROM pieces_v3 p
            LEFT JOIN clients_v3 c ON c.id = p.client_id
            ORDER BY p.created_at DESC, p.id DESC
            LIMIT 10
        """)).mappings().all()

    documents = int(stats["documents"] or 0)
    ocr = int(stats["ocr"] or 0)
    a_valider = int(stats["a_valider"] or 0)
    manquants = int(stats["manquants"] or 0)
    score = 100 if documents == 0 else max(0, min(100, round(((documents - manquants) / documents) * 100)))

    kpis = {
        "documents": documents,
        "ocr": ocr,
        "manquants": manquants,
        "a_valider": a_valider,
        "score": score,
    }

    dossiers = []
    for row in dossiers_rows:
        alertes = int(row["alertes"] or 0)
        dossiers.append({
            "nom": row["type_piece"],
            "description": "Classement documentaire réel issu de pieces_v3.",
            "documents": int(row["documents"] or 0),
            "alertes": alertes,
            "statut": "OK" if alertes == 0 else "À valider",
        })

    pieces = []
    for row in pieces_rows:
        pieces.append({
            "nom": row["nom_fichier"],
            "cycle": row["type_piece"],
            "compte": row["client"],
            "statut": row["statut_validation"],
            "controle": f"{row['statut_ocr']} · {row['controle']} · score {row['score_ia']}",
        })

    return kpis, dossiers, pieces

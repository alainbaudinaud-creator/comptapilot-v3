from services.db_postgres import get_session
from sqlalchemy import text


def get_production_metrics():

    session = get_session()

    metrics = {}

    metrics["documents_total"] = session.execute(
        text("SELECT COUNT(*) FROM documents")
    ).scalar() or 0

    metrics["ocr_en_attente"] = session.execute(
        text(
            "SELECT COUNT(*) FROM documents WHERE statut_ocr = 'en_attente'"
        )
    ).scalar() or 0

    metrics["ocr_termine"] = session.execute(
        text(
            "SELECT COUNT(*) FROM documents WHERE statut_ocr = 'termine'"
        )
    ).scalar() or 0

    metrics["ocr_erreur"] = session.execute(
        text(
            "SELECT COUNT(*) FROM documents WHERE statut_ocr = 'erreur'"
        )
    ).scalar() or 0

    metrics["precompta_total"] = session.execute(
        text(
            "SELECT COUNT(*) FROM precompta_documents"
        )
    ).scalar() or 0

    metrics["precompta_a_valider"] = session.execute(
        text(
            "SELECT COUNT(*) FROM precompta_documents WHERE statut_validation = 'a_valider'"
        )
    ).scalar() or 0

    metrics["precompta_validee"] = session.execute(
        text(
            "SELECT COUNT(*) FROM precompta_documents WHERE statut_validation = 'validee'"
        )
    ).scalar() or 0

    metrics["precompta_rejetee"] = session.execute(
        text(
            "SELECT COUNT(*) FROM precompta_documents WHERE statut_validation = 'rejetee'"
        )
    ).scalar() or 0

    metrics["ecritures_total"] = session.execute(
        text(
            "SELECT COUNT(*) FROM ecritures_v3"
        )
    ).scalar() or 0

    metrics["clients_total"] = session.execute(
        text(
            "SELECT COUNT(*) FROM societes"
        )
    ).scalar() or 0

    session.close()

    return metrics


def get_recent_production_items():

    session = get_session()

    result = session.execute(
        text(
            """
            SELECT
                d.id,
                d.societe_id,
                d.original_filename,
                d.statut_ocr,
                d.statut_precompta,
                d.created_at
            FROM documents d
            ORDER BY d.created_at DESC
            LIMIT 20
            """
        )
    )

    rows = result.fetchall()

    session.close()

    return [
        {
            "document_id": row[0],
            "societe_id": row[1],
            "filename": row[2],
            "statut_ocr": row[3],
            "statut_precompta": row[4],
            "created_at": str(row[5])
        }
        for row in rows
    ]



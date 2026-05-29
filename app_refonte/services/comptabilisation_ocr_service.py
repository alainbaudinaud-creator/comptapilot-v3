from datetime import date

from sqlalchemy import text

from database import engine


def comptabiliser_ecriture_ocr(ecriture, client_id=1):

    lignes = ecriture.get("lignes", [])

    with engine.begin() as conn:

        ecriture_id = conn.execute(text("""
            INSERT INTO ecritures_v3
            (
                client_id,
                date_ecriture,
                piece,
                libelle,
                statut,
                source
            )
            VALUES
            (
                :client_id,
                CURRENT_DATE,
                :piece,
                :libelle,
                'VALIDE',
                'OCR_IA'
            )
            RETURNING id
        """), {
            "client_id": client_id,
            "piece": f"OCR-{date.today()}",
            "libelle": ecriture.get("libelle", "OCR IA"),
        }).scalar()

        for ligne in lignes:

            conn.execute(text("""
                INSERT INTO lignes_ecritures_v3
                (
                    ecriture_id,
                    compte,
                    libelle,
                    debit,
                    credit
                )
                VALUES
                (
                    :ecriture_id,
                    :compte,
                    :libelle,
                    :debit,
                    :credit
                )
            """), {
                "ecriture_id": ecriture_id,
                "compte": ligne["compte"],
                "libelle": ecriture.get("libelle", ""),
                "debit": ligne.get("debit", 0),
                "credit": ligne.get("credit", 0),
            })

    return {
        "success": True,
        "ecriture_id": ecriture_id,
    }

from datetime import datetime
from sqlalchemy import text
from database import engine


def enregistrer_piece(client_id, nom_fichier, chemin_stockage):

    with engine.begin() as conn:

        piece_id = conn.execute(text("""
            INSERT INTO pieces_v3
            (
                client_id,
                nom_fichier,
                type_piece,
                chemin_stockage,
                statut_ocr,
                created_at
            )
            VALUES
            (
                :client_id,
                :nom_fichier,
                'FACTURE',
                :chemin_stockage,
                'TRAITE',
                NOW()
            )
            RETURNING id
        """), {
            "client_id": client_id,
            "nom_fichier": nom_fichier,
            "chemin_stockage": chemin_stockage,
        }).scalar()

    return piece_id


def analyser_piece_ia(piece_id, chemin_piece):

    analyse = {
        "piece_id": piece_id,
        "fournisseur": "FOURNISSEUR DEMO IA",
        "date_facture": str(datetime.now().date()),
        "numero_facture": f"FACT-{piece_id}",
        "montant_ht": 1000,
        "montant_tva": 200,
        "montant_ttc": 1200,
        "compte_charge": "606100",
        "compte_tva": "445660",
        "compte_fournisseur": "401000",
        "journal": "AC",
        "score_ia": 92,
        "statut": "ANALYSE_OK",
    }

    with engine.begin() as conn:

        conn.execute(text("""
            INSERT INTO factures_v3
            (
                client_id,
                sens,
                fournisseur_client,
                numero,
                date_facture,
                montant_ht,
                montant_tva,
                montant_ttc,
                statut,
                score_ia,
                created_at
            )
            VALUES
            (
                1,
                'ACHAT',
                :fournisseur,
                :numero,
                :date_facture,
                :montant_ht,
                :montant_tva,
                :montant_ttc,
                'ANALYSEE',
                :score_ia,
                NOW()
            )
        """), {
            "fournisseur": analyse["fournisseur"],
            "numero": analyse["numero_facture"],
            "date_facture": analyse["date_facture"],
            "montant_ht": analyse["montant_ht"],
            "montant_tva": analyse["montant_tva"],
            "montant_ttc": analyse["montant_ttc"],
            "score_ia": analyse["score_ia"],
        })

    return analyse


def generer_pre_ecriture(client_id, analyse):

    with engine.begin() as conn:

        journal_id = conn.execute(text("""
            SELECT id
            FROM journaux_v3
            WHERE code = 'AC'
            LIMIT 1
        """)).scalar()

        ecriture_id = conn.execute(text("""
            INSERT INTO ecritures_v3
            (
                client_id,
                journal_id,
                date_ecriture,
                piece,
                libelle,
                statut,
                source,
                created_at
            )
            VALUES
            (
                :client_id,
                :journal_id,
                NOW(),
                :piece,
                :libelle,
                'BROUILLARD',
                'IA',
                NOW()
            )
            RETURNING id
        """), {
            "client_id": client_id,
            "journal_id": journal_id,
            "piece": analyse["numero_facture"],
            "libelle": f"FACTURE {analyse['fournisseur']}",
        }).scalar()

        lignes = [
            (
                analyse["compte_charge"],
                "Charge",
                analyse["montant_ht"],
                0
            ),
            (
                analyse["compte_tva"],
                "TVA",
                analyse["montant_tva"],
                0
            ),
            (
                analyse["compte_fournisseur"],
                "Fournisseur",
                0,
                analyse["montant_ttc"]
            ),
        ]

        for compte, libelle, debit, credit in lignes:

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
                "compte": compte,
                "libelle": libelle,
                "debit": debit,
                "credit": credit,
            })

    return {
        "ecriture_id": ecriture_id,
        "journal": analyse["journal"],
        "piece": analyse["numero_facture"],
        "equilibre": True,
    }

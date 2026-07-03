from sqlalchemy import text
from database import engine


def _count(conn, table):
    return conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar() or 0


def _scalar(conn, sql, params=None):
    return conn.execute(text(sql), params or {}).scalar() or 0


def charger_cockpit_reel():
    with engine.begin() as conn:
        total_clients = _count(conn, "clients_v3")
        total_ecritures = _count(conn, "ecritures_v3")
        total_factures = _count(conn, "factures_v3")
        total_pieces = _count(conn, "pieces_v3")
        total_taches = _count(conn, "taches_cabinet_v3")

        exercice_actif = conn.execute(text("""
            SELECT id, date_debut, date_fin, statut
            FROM exercices_v3
            WHERE statut = 'OUVERT'
            ORDER BY date_debut DESC, id DESC
            LIMIT 1
        """)).mappings().first()

        dernier_exercice_cloture = conn.execute(text("""
            SELECT id, date_debut, date_fin, statut, resultat_cloture, date_cloture
            FROM exercices_v3
            WHERE statut IN ('CLOTURE', 'VERROUILLE')
            ORDER BY date_fin DESC, id DESC
            LIMIT 1
        """)).mappings().first()

        ecriture_an = conn.execute(text("""
            SELECT id, piece, date_ecriture
            FROM ecritures_v3
            WHERE source = 'A_NOUVEAUX_AUTO'
              AND COALESCE(statut, '') <> 'ANNULE'
            ORDER BY id DESC
            LIMIT 1
        """)).mappings().first()

        lignes = conn.execute(text("""
            SELECT COALESCE(SUM(l.debit),0) AS debit, COALESCE(SUM(l.credit),0) AS credit
            FROM lignes_ecritures_v3 l
            JOIN ecritures_v3 e ON e.id = l.ecriture_id
            WHERE COALESCE(e.statut, '') <> 'ANNULE'
        """)).mappings().first()

        documents_ocr_a_traiter = _scalar(conn, """
            SELECT COUNT(*)
            FROM pieces_v3
            WHERE statut_validation IN ('A_VALIDER', 'A_TRAITER')
               OR statut_ocr IN ('A_TRAITER', 'A_VALIDER')
        """)

        factures_a_traiter = _scalar(conn, """
            SELECT COUNT(*)
            FROM factures_v3
            WHERE statut IN ('A_ANALYSER', 'A_VALIDER')
        """)

        operations_non_rapprochees = _scalar(conn, """
            SELECT COUNT(*)
            FROM operations_bancaires_v3
            WHERE statut <> 'RAPPROCHE'
        """)

        rapprochements_valides = _scalar(conn, """
            SELECT COUNT(*)
            FROM rapprochements_bancaires_v3
            WHERE statut = 'VALIDE'
        """)

        lettrages_valides = _scalar(conn, """
            SELECT COUNT(*)
            FROM lettrages_tiers_v3
            WHERE statut IN ('LETTRÉ', 'LETTRE', 'VALIDE')
        """)

        immobilisations_actives = _scalar(conn, """
            SELECT COUNT(*)
            FROM immobilisations_v3
            WHERE statut = 'ACTIVE'
        """)

        valeur_immobilisations = _scalar(conn, """
            SELECT COALESCE(SUM(valeur_origine),0)
            FROM immobilisations_v3
            WHERE statut = 'ACTIVE'
        """)

        emprunts_actifs = _scalar(conn, """
            SELECT COUNT(*)
            FROM emprunts_v3
            WHERE statut = 'ACTIF'
        """)

        capital_emprunts = _scalar(conn, """
            SELECT COALESCE(SUM(capital),0)
            FROM emprunts_v3
            WHERE statut = 'ACTIF'
        """)

        taches_ouvertes = _scalar(conn, """
            SELECT COUNT(*)
            FROM taches_cabinet_v3
            WHERE statut <> 'TERMINE'
        """)

        taches_urgentes = conn.execute(text("""
            SELECT titre, priorite, statut
            FROM taches_cabinet_v3
            WHERE statut <> 'TERMINE'
            ORDER BY
                CASE priorite
                    WHEN 'CRITIQUE' THEN 1
                    WHEN 'HAUTE' THEN 2
                    WHEN 'WARNING' THEN 3
                    WHEN 'NORMALE' THEN 4
                    ELSE 5
                END,
                id
            LIMIT 10
        """)).mappings().all()

        factures_a_analyser = conn.execute(text("""
            SELECT fournisseur_client, numero, montant_ttc, statut
            FROM factures_v3
            WHERE statut IN ('A_ANALYSER', 'A_VALIDER')
            ORDER BY id DESC
            LIMIT 10
        """)).mappings().all()

    total_debit = float(lignes["debit"] or 0)
    total_credit = float(lignes["credit"] or 0)
    equilibre = round(total_debit, 2) == round(total_credit, 2)

    alertes = []
    if total_clients == 0:
        alertes.append({"type": "ALERTE", "titre": "Aucun client créé", "niveau": "WARNING"})
    if total_ecritures == 0:
        alertes.append({"type": "ALERTE", "titre": "Aucune écriture comptable enregistrée", "niveau": "WARNING"})
    if not equilibre:
        alertes.append({"type": "ALERTE", "titre": "Balance débit/crédit déséquilibrée", "niveau": "CRITIQUE"})
    if operations_non_rapprochees:
        alertes.append({
            "type": "BANQUE",
            "titre": f"{operations_non_rapprochees} opération(s) bancaire(s) à rapprocher",
            "niveau": "WARNING",
        })
    if not exercice_actif:
        alertes.append({"type": "EXERCICE", "titre": "Aucun exercice ouvert", "niveau": "CRITIQUE"})

    priorites = []

    for t in taches_urgentes:
        priorites.append({
            "type": "WORKFLOW",
            "titre": t["titre"],
            "niveau": t["priorite"] or "NORMALE",
        })

    for f in factures_a_analyser:
        label = f["numero"] or f["fournisseur_client"] or "Facture sans référence"
        priorites.append({
            "type": "FACTURE",
            "titre": f"Analyser facture : {label}",
            "niveau": "HAUTE",
        })

    priorites.extend(alertes)

    score = 100
    score -= min(len([p for p in priorites if p["niveau"] == "HAUTE"]) * 4, 30)
    score -= min(len([p for p in priorites if p["niveau"] == "WARNING"]) * 5, 30)
    score -= min(len([p for p in priorites if p["niveau"] == "CRITIQUE"]) * 15, 40)

    exercice_actif_label = "-"
    if exercice_actif:
        exercice_actif_label = f"{exercice_actif['date_debut']} → {exercice_actif['date_fin']}"

    kpis = {
        "total_societes": total_clients,
        "total_ecritures": total_ecritures,
        "total_documents": total_pieces + total_factures,
        "documents_a_traiter": int(documents_ocr_a_traiter + factures_a_traiter),
        "taches_urgentes": len([p for p in priorites if p["niveau"] in ("HAUTE", "CRITIQUE")]),
        "alertes_critiques": len([p for p in priorites if p["niveau"] in ("WARNING", "CRITIQUE")]),
        "total_debit": total_debit,
        "total_credit": total_credit,
        "equilibre_comptable": equilibre,
        "score_production": max(score, 0),

        "exercice_actif": exercice_actif_label,
        "exercice_actif_statut": exercice_actif["statut"] if exercice_actif else "ABSENT",
        "dernier_resultat": float((dernier_exercice_cloture or {}).get("resultat_cloture") or 0),
        "dernier_exercice_cloture": dernier_exercice_cloture["id"] if dernier_exercice_cloture else None,
        "a_nouveaux_id": ecriture_an["id"] if ecriture_an else None,

        "operations_non_rapprochees": int(operations_non_rapprochees),
        "rapprochements_valides": int(rapprochements_valides),
        "lettrages_valides": int(lettrages_valides),

        "immobilisations_actives": int(immobilisations_actives),
        "valeur_immobilisations": float(valeur_immobilisations or 0),
        "emprunts_actifs": int(emprunts_actifs),
        "capital_emprunts": float(capital_emprunts or 0),
        "taches_ouvertes": int(taches_ouvertes),
    }

    return kpis, priorites[:10]

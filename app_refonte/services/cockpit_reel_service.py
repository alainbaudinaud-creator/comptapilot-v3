from sqlalchemy import text
from database import engine


def _count(conn, table):
    return conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar() or 0


def charger_cockpit_reel():
    with engine.begin() as conn:
        total_clients = _count(conn, "clients_v3")
        total_ecritures = _count(conn, "ecritures_v3")
        total_factures = _count(conn, "factures_v3")
        total_pieces = _count(conn, "pieces_v3")
        total_taches = _count(conn, "taches_cabinet_v3")

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

        lignes = conn.execute(text("""
            SELECT COALESCE(SUM(debit),0) AS debit, COALESCE(SUM(credit),0) AS credit
            FROM lignes_ecritures_v3
        """)).mappings().first()

    total_debit = float(lignes["debit"] or 0)
    total_credit = float(lignes["credit"] or 0)

    alertes = []
    if total_clients == 0:
        alertes.append({"type": "ALERTE", "titre": "Aucun client créé", "niveau": "WARNING"})
    if total_ecritures == 0:
        alertes.append({"type": "ALERTE", "titre": "Aucune écriture comptable enregistrée", "niveau": "WARNING"})
    if total_debit != total_credit:
        alertes.append({"type": "ALERTE", "titre": "Balance débit/crédit déséquilibrée", "niveau": "CRITIQUE"})

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

    kpis = {
        "total_societes": total_clients,
        "total_ecritures": total_ecritures,
        "total_documents": total_pieces + total_factures,
        "documents_a_traiter": total_factures + total_pieces,
        "taches_urgentes": len([p for p in priorites if p["niveau"] in ("HAUTE", "CRITIQUE")]),
        "alertes_critiques": len([p for p in priorites if p["niveau"] in ("WARNING", "CRITIQUE")]),
        "total_debit": total_debit,
        "total_credit": total_credit,
        "equilibre_comptable": total_debit == total_credit,
        "score_production": max(score, 0),
    }

    return kpis, priorites[:10]

from sqlalchemy import text
from database import engine


def stats_moteurs_comptables():

    stats = {}

    queries = {
        "clients": "SELECT COUNT(*) FROM clients_v3",
        "ecritures": "SELECT COUNT(*) FROM ecritures_v3",
        "lignes": "SELECT COUNT(*) FROM lignes_ecritures_v3",
        "factures": "SELECT COUNT(*) FROM factures_v3",
        "pieces": "SELECT COUNT(*) FROM pieces_v3",
        "imports": "SELECT COUNT(*) FROM imports_v3",
    }

    with engine.connect() as conn:
        for key, query in queries.items():
            try:
                stats[key] = conn.execute(text(query)).scalar() or 0
            except Exception:
                stats[key] = 0

    return stats


def generer_balance():

    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT
                compte,
                COALESCE(SUM(debit), 0) AS debit,
                COALESCE(SUM(credit), 0) AS credit,
                COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) AS solde
            FROM lignes_ecritures_v3
            GROUP BY compte
            ORDER BY compte
        """)).mappings().all()

    return [dict(r) for r in rows]


def generer_grand_livre():

    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT
                l.compte,
                e.date_ecriture,
                e.piece,
                e.libelle AS libelle_ecriture,
                l.libelle AS libelle_ligne,
                l.debit,
                l.credit
            FROM lignes_ecritures_v3 l
            LEFT JOIN ecritures_v3 e ON e.id = l.ecriture_id
            ORDER BY l.compte, e.date_ecriture, e.id
        """)).mappings().all()

    return [dict(r) for r in rows]


def generer_tva_ca3():

    with engine.connect() as conn:
        tva_deductible = conn.execute(text("""
            SELECT COALESCE(SUM(debit - credit), 0)
            FROM lignes_ecritures_v3
            WHERE compte LIKE '4456%'
        """)).scalar() or 0

        tva_collectee = conn.execute(text("""
            SELECT COALESCE(SUM(credit - debit), 0)
            FROM lignes_ecritures_v3
            WHERE compte LIKE '4457%'
        """)).scalar() or 0

    tva_due = float(tva_collectee) - float(tva_deductible)

    return {
        "tva_collectee": float(tva_collectee),
        "tva_deductible": float(tva_deductible),
        "tva_due": tva_due,
        "statut": "A_PAYER" if tva_due > 0 else "CREDIT_TVA",
    }


def exporter_fec_demo():

    chemin = "exports/fec_v3_demo.txt"

    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT
                COALESCE(j.code, 'OD') AS journal_code,
                COALESCE(j.libelle, 'Operations diverses') AS journal_libelle,
                e.date_ecriture,
                e.piece,
                e.libelle AS ecriture_libelle,
                l.compte,
                l.libelle AS ligne_libelle,
                l.debit,
                l.credit
            FROM lignes_ecritures_v3 l
            LEFT JOIN ecritures_v3 e ON e.id = l.ecriture_id
            LEFT JOIN journaux_v3 j ON j.id = e.journal_id
            ORDER BY e.date_ecriture, e.id, l.id
        """)).mappings().all()

    headers = [
        "JournalCode",
        "JournalLib",
        "EcritureDate",
        "PieceRef",
        "EcritureLib",
        "CompteNum",
        "CompteLib",
        "Debit",
        "Credit",
    ]

    with open(chemin, "w", encoding="utf-8") as f:
        f.write("|".join(headers) + "\n")

        for r in rows:
            f.write("|".join([
                str(r["journal_code"] or ""),
                str(r["journal_libelle"] or ""),
                str(r["date_ecriture"] or ""),
                str(r["piece"] or ""),
                str(r["ecriture_libelle"] or ""),
                str(r["compte"] or ""),
                str(r["ligne_libelle"] or ""),
                str(r["debit"] or 0),
                str(r["credit"] or 0),
            ]) + "\n")

    return chemin

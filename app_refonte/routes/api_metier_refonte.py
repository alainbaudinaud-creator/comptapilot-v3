from flask import Blueprint, jsonify, request
from sqlalchemy import text

from database import engine
from app_refonte.services.immobilisations_service import amortissement_lineaire
from app_refonte.services.emprunts_service import tableau_amortissement_emprunt
from app_refonte.services.tva_service import calcul_tva
from app_refonte.services.fec_service import controle_colonnes_fec, REQUIRED_FEC_COLUMNS

api_metier_refonte = Blueprint("api_metier_refonte", __name__)


@api_metier_refonte.get("/api/refonte/health")
def health():
    return jsonify({
        "success": True,
        "module": "ComptaPilot V3 Refonte",
        "status": "OK"
    })


@api_metier_refonte.post("/api/refonte/immobilisation/amortissement")
def api_amortissement():
    data = request.get_json(silent=True) or {}
    lignes = amortissement_lineaire(
        data.get("valeur_origine", 0),
        data.get("duree_mois", 0)
    )
    return jsonify({"success": True, "lignes": lignes})


@api_metier_refonte.post("/api/refonte/emprunt/tableau")
def api_emprunt():
    data = request.get_json(silent=True) or {}
    lignes = tableau_amortissement_emprunt(
        data.get("montant", 0),
        data.get("taux_annuel", 0),
        data.get("duree_mois", 0)
    )
    return jsonify({"success": True, "lignes": lignes})


@api_metier_refonte.post("/api/refonte/tva/calcul")
def api_tva():
    data = request.get_json(silent=True) or {}
    resultat = calcul_tva(
        data.get("tva_collectee", 0),
        data.get("tva_deductible", 0)
    )
    return jsonify({"success": True, "resultat": resultat})


@api_metier_refonte.get("/api/refonte/fec/controle-demo")
def api_fec_controle():
    resultat = controle_colonnes_fec(REQUIRED_FEC_COLUMNS)
    return jsonify({"success": True, "resultat": resultat})


@api_metier_refonte.get("/api/refonte/pcg")
def api_pcg():
    q = request.args.get("q", "").strip().lower()
    classe = request.args.get("classe", "").strip()

    sql = """
        SELECT id, societe_id, numero, libelle, type, classe, actif, source
        FROM plan_comptable
        WHERE actif = TRUE
    """
    params = {}

    if q:
        sql += " AND (LOWER(numero) LIKE :q OR LOWER(libelle) LIKE :q)"
        params["q"] = f"%{q}%"

    if classe:
        sql += " AND classe = :classe"
        params["classe"] = classe

    sql += " ORDER BY numero LIMIT 500"

    with engine.begin() as conn:
        rows = conn.execute(text(sql), params).mappings().all()

    return jsonify({
        "success": True,
        "total": len(rows),
        "comptes": [dict(r) for r in rows],
    })

@api_metier_refonte.post("/api/refonte/emprunt/premium")
def api_emprunt_premium():
    from app_refonte.services.emprunts_premium_service import generer_tableau_emprunt, generer_ecritures_emprunt

    data = request.get_json(silent=True) or {}
    tableau = generer_tableau_emprunt(
        data.get("capital", 0),
        data.get("taux_annuel", 0),
        data.get("duree_mois", 0),
    )
    ecritures = generer_ecritures_emprunt(tableau)

    return jsonify({
        "success": True,
        "tableau": tableau,
        "ecritures": ecritures,
    })

@api_metier_refonte.post("/api/refonte/immobilisation/premium")
def api_immobilisation_premium():
    from app_refonte.services.amortissement_ecritures_service import generer_plan_amortissement, generer_ecritures_amortissement

    data = request.get_json(silent=True) or {}
    plan = generer_plan_amortissement(
        data.get("designation", "Immobilisation"),
        data.get("valeur_origine", 0),
        data.get("duree_mois", 0),
        data.get("compte_immo", "218300"),
        data.get("compte_amortissement", "281830"),
        data.get("compte_dotation", "681120"),
    )
    ecritures = generer_ecritures_amortissement(plan)

    return jsonify({
        "success": plan.get("success", False),
        "plan": plan,
        "ecritures": ecritures,
    })


@api_metier_refonte.post("/api/refonte/immobilisation/creer")
def api_creer_immobilisation():
    from app_refonte.services.amortissement_ecritures_service import generer_plan_amortissement, generer_ecritures_amortissement

    data = request.get_json(silent=True) or {}

    designation = data.get("designation", "Immobilisation")
    valeur_origine = data.get("valeur_origine", 0)
    duree_mois = data.get("duree_mois", 0)
    compte_immo = data.get("compte_immo", "218300")
    compte_amortissement = data.get("compte_amortissement", "281830")
    compte_dotation = data.get("compte_dotation", "681120")

    with engine.begin() as conn:
        client = conn.execute(text("SELECT id FROM clients_v3 ORDER BY id LIMIT 1")).fetchone()
        societe_id = client[0] if client else None

        immobilisation_id = conn.execute(text("""
            INSERT INTO immobilisations_v3 (
                societe_id,
                designation,
                valeur_origine,
                duree_mois,
                compte_immo,
                compte_amortissement,
                compte_dotation
            )
            VALUES (
                :societe_id,
                :designation,
                :valeur_origine,
                :duree_mois,
                :compte_immo,
                :compte_amortissement,
                :compte_dotation
            )
            RETURNING id
        """), {
            "societe_id": societe_id,
            "designation": designation,
            "valeur_origine": valeur_origine,
            "duree_mois": duree_mois,
            "compte_immo": compte_immo,
            "compte_amortissement": compte_amortissement,
            "compte_dotation": compte_dotation,
        }).scalar()

    plan = generer_plan_amortissement(
        designation,
        valeur_origine,
        duree_mois,
        compte_immo,
        compte_amortissement,
        compte_dotation,
    )
    ecritures = generer_ecritures_amortissement(plan)

    return jsonify({
        "success": True,
        "immobilisation_id": immobilisation_id,
        "plan": plan,
        "ecritures": ecritures,
    })


@api_metier_refonte.get("/api/refonte/immobilisations")
def api_lister_immobilisations():
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT id, societe_id, designation, date_acquisition, valeur_origine,
                   duree_mois, compte_immo, compte_amortissement, compte_dotation,
                   statut, created_at
            FROM immobilisations_v3
            ORDER BY id DESC
            LIMIT 100
        """)).mappings().all()

    return jsonify({
        "success": True,
        "total": len(rows),
        "immobilisations": [dict(r) for r in rows],
    })



@api_metier_refonte.post("/api/refonte/immobilisation/comptabiliser")
def api_comptabiliser_immobilisation():
    from app_refonte.services.amortissement_ecritures_service import generer_plan_amortissement, generer_ecritures_amortissement

    data = request.get_json(silent=True) or {}

    immobilisation_id = data.get("immobilisation_id")
    if not immobilisation_id:
        return jsonify({"success": False, "error": "immobilisation_id obligatoire"}), 400

    with engine.begin() as conn:
        immo = conn.execute(text("""
            SELECT id, societe_id, designation, valeur_origine, duree_mois,
                   compte_immo, compte_amortissement, compte_dotation
            FROM immobilisations_v3
            WHERE id = :id
        """), {"id": immobilisation_id}).mappings().first()

        if not immo:
            return jsonify({"success": False, "error": "Immobilisation introuvable"}), 404

        exercice = conn.execute(text("""
            SELECT id
            FROM exercices_v3
            WHERE client_id = :client_id
            ORDER BY id
            LIMIT 1
        """), {"client_id": immo["societe_id"]}).fetchone()

        journal = conn.execute(text("""
            SELECT id
            FROM journaux_v3
            WHERE client_id = :client_id AND code = 'OD'
            ORDER BY id
            LIMIT 1
        """), {"client_id": immo["societe_id"]}).fetchone()

        exercice_id = exercice[0] if exercice else None
        journal_id = journal[0] if journal else None

    plan = generer_plan_amortissement(
        immo["designation"],
        immo["valeur_origine"],
        immo["duree_mois"],
        immo["compte_immo"],
        immo["compte_amortissement"],
        immo["compte_dotation"],
    )
    ecritures = generer_ecritures_amortissement(plan)

    ids = []

    with engine.begin() as conn:
        for ecriture in ecritures:
            ecriture_id = conn.execute(text("""
                INSERT INTO ecritures_v3 (
                    client_id,
                    exercice_id,
                    journal_id,
                    date_ecriture,
                    piece,
                    libelle,
                    statut,
                    source
                )
                VALUES (
                    :client_id,
                    :exercice_id,
                    :journal_id,
                    :date_ecriture,
                    :piece,
                    :libelle,
                    'BROUILLARD',
                    'IMMOBILISATION_AUTO'
                )
                RETURNING id
            """), {
                "client_id": immo["societe_id"],
                "exercice_id": exercice_id,
                "journal_id": journal_id,
                "date_ecriture": ecriture.get("date_ecriture"),
                "piece": f"IMMO-{immo['id']}",
                "libelle": ecriture.get("libelle"),
            }).scalar()

            ids.append(ecriture_id)

            for ligne in ecriture.get("lignes", []):
                conn.execute(text("""
                    INSERT INTO lignes_ecritures_v3 (
                        ecriture_id,
                        compte,
                        libelle,
                        debit,
                        credit
                    )
                    VALUES (
                        :ecriture_id,
                        :compte,
                        :libelle,
                        :debit,
                        :credit
                    )
                """), {
                    "ecriture_id": ecriture_id,
                    "compte": ligne.get("compte"),
                    "libelle": ecriture.get("libelle"),
                    "debit": ligne.get("debit", 0),
                    "credit": ligne.get("credit", 0),
                })

    return jsonify({
        "success": True,
        "immobilisation_id": immobilisation_id,
        "ecritures_creees": len(ids),
        "ecriture_ids": ids,
    })



@api_metier_refonte.post("/api/refonte/emprunt/creer")
def api_creer_emprunt():
    from app_refonte.services.emprunts_premium_service import generer_tableau_emprunt, generer_ecritures_emprunt

    data = request.get_json(silent=True) or {}

    organisme = data.get("organisme", "Banque")
    capital = data.get("capital", 0)
    taux_annuel = data.get("taux_annuel", 0)
    duree_mois = data.get("duree_mois", 0)

    with engine.begin() as conn:
        client = conn.execute(text("SELECT id FROM clients_v3 ORDER BY id LIMIT 1")).fetchone()
        societe_id = client[0] if client else None

        emprunt_id = conn.execute(text("""
            INSERT INTO emprunts_v3 (
                societe_id, organisme, capital, taux_annuel, duree_mois
            )
            VALUES (
                :societe_id, :organisme, :capital, :taux_annuel, :duree_mois
            )
            RETURNING id
        """), {
            "societe_id": societe_id,
            "organisme": organisme,
            "capital": capital,
            "taux_annuel": taux_annuel,
            "duree_mois": duree_mois,
        }).scalar()

    tableau = generer_tableau_emprunt(capital, taux_annuel, duree_mois)
    ecritures = generer_ecritures_emprunt(tableau)

    return jsonify({
        "success": True,
        "emprunt_id": emprunt_id,
        "tableau": tableau,
        "ecritures": ecritures,
    })


@api_metier_refonte.post("/api/refonte/emprunt/comptabiliser")
def api_comptabiliser_emprunt():
    from app_refonte.services.emprunts_premium_service import generer_tableau_emprunt, generer_ecritures_emprunt

    data = request.get_json(silent=True) or {}
    emprunt_id = data.get("emprunt_id")

    if not emprunt_id:
        return jsonify({"success": False, "error": "emprunt_id obligatoire"}), 400

    with engine.begin() as conn:
        emp = conn.execute(text("""
            SELECT id, societe_id, organisme, capital, taux_annuel, duree_mois,
                   compte_emprunt, compte_interets, compte_banque
            FROM emprunts_v3
            WHERE id = :id
        """), {"id": emprunt_id}).mappings().first()

        if not emp:
            return jsonify({"success": False, "error": "Emprunt introuvable"}), 404

        exercice = conn.execute(text("""
            SELECT id FROM exercices_v3
            WHERE client_id = :client_id
            ORDER BY id LIMIT 1
        """), {"client_id": emp["societe_id"]}).fetchone()

        journal = conn.execute(text("""
            SELECT id FROM journaux_v3
            WHERE client_id = :client_id AND code = 'BQ'
            ORDER BY id LIMIT 1
        """), {"client_id": emp["societe_id"]}).fetchone()

        exercice_id = exercice[0] if exercice else None
        journal_id = journal[0] if journal else None

    tableau = generer_tableau_emprunt(
        emp["capital"],
        emp["taux_annuel"],
        emp["duree_mois"],
        emp["compte_emprunt"],
        emp["compte_interets"],
        emp["compte_banque"],
    )
    ecritures = generer_ecritures_emprunt(tableau)

    ids = []

    with engine.begin() as conn:
        for ecriture in ecritures:
            ecriture_id = conn.execute(text("""
                INSERT INTO ecritures_v3 (
                    client_id, exercice_id, journal_id, date_ecriture,
                    piece, libelle, statut, source
                )
                VALUES (
                    :client_id, :exercice_id, :journal_id, CURRENT_DATE,
                    :piece, :libelle, 'BROUILLARD', 'EMPRUNT_AUTO'
                )
                RETURNING id
            """), {
                "client_id": emp["societe_id"],
                "exercice_id": exercice_id,
                "journal_id": journal_id,
                "piece": f"EMP-{emp['id']}",
                "libelle": ecriture.get("libelle"),
            }).scalar()

            ids.append(ecriture_id)

            for ligne in ecriture.get("lignes", []):
                conn.execute(text("""
                    INSERT INTO lignes_ecritures_v3 (
                        ecriture_id, compte, libelle, debit, credit
                    )
                    VALUES (
                        :ecriture_id, :compte, :libelle, :debit, :credit
                    )
                """), {
                    "ecriture_id": ecriture_id,
                    "compte": ligne.get("compte"),
                    "libelle": ecriture.get("libelle"),
                    "debit": ligne.get("debit", 0),
                    "credit": ligne.get("credit", 0),
                })

    return jsonify({
        "success": True,
        "emprunt_id": emprunt_id,
        "ecritures_creees": len(ids),
        "ecriture_ids": ids,
    })



@api_metier_refonte.get("/api/refonte/balance")
def api_balance_generale():

    sql = """
    SELECT
        l.compte,
        COALESCE(pc.libelle,'Compte inconnu') AS libelle,
        SUM(COALESCE(l.debit,0))  AS total_debit,
        SUM(COALESCE(l.credit,0)) AS total_credit,
        SUM(COALESCE(l.debit,0)) - SUM(COALESCE(l.credit,0)) AS solde
    FROM lignes_ecritures_v3 l
    LEFT JOIN plan_comptable pc
           ON pc.numero = l.compte
    GROUP BY l.compte, pc.libelle
    ORDER BY l.compte
    """

    with engine.begin() as conn:
        rows = conn.execute(text(sql)).mappings().all()

    total_debit = sum(float(r["total_debit"] or 0) for r in rows)
    total_credit = sum(float(r["total_credit"] or 0) for r in rows)

    return jsonify({
        "success": True,
        "equilibre": round(total_debit,2) == round(total_credit,2),
        "total_debit": total_debit,
        "total_credit": total_credit,
        "comptes": [dict(r) for r in rows]
    })



@api_metier_refonte.get("/api/refonte/grand-livre")
def api_grand_livre():
    compte = request.args.get("compte", "").strip()

    sql = """
    SELECT
        e.date_ecriture,
        e.piece,
        e.libelle,
        e.source,
        l.compte,
        COALESCE(pc.libelle,'Compte inconnu') AS compte_libelle,
        l.debit,
        l.credit
    FROM lignes_ecritures_v3 l
    JOIN ecritures_v3 e ON e.id = l.ecriture_id
    LEFT JOIN plan_comptable pc ON pc.numero = l.compte
    WHERE 1=1
    """
    params = {}

    if compte:
        sql += " AND l.compte = :compte"
        params["compte"] = compte

    sql += " ORDER BY l.compte, e.date_ecriture, e.id"

    with engine.begin() as conn:
        rows = conn.execute(text(sql), params).mappings().all()

    total_debit = sum(float(r["debit"] or 0) for r in rows)
    total_credit = sum(float(r["credit"] or 0) for r in rows)

    return jsonify({
        "success": True,
        "compte": compte or None,
        "total": len(rows),
        "total_debit": total_debit,
        "total_credit": total_credit,
        "solde": total_debit - total_credit,
        "lignes": [dict(r) for r in rows],
    })



@api_metier_refonte.get("/api/refonte/journal")
def api_journal():

    sql = """
    SELECT
        e.id,
        e.date_ecriture,
        e.piece,
        e.libelle,
        e.source,
        l.compte,
        COALESCE(pc.libelle,'Compte inconnu') AS compte_libelle,
        l.debit,
        l.credit
    FROM ecritures_v3 e
    JOIN lignes_ecritures_v3 l
         ON l.ecriture_id = e.id
    LEFT JOIN plan_comptable pc
         ON pc.numero = l.compte
    ORDER BY e.date_ecriture, e.id, l.id
    """

    with engine.begin() as conn:
        rows = conn.execute(text(sql)).mappings().all()

    return jsonify({
        "success": True,
        "total": len(rows),
        "lignes": [dict(r) for r in rows]
    })



@api_metier_refonte.get("/api/refonte/fec/export")
def api_export_fec_reel():
    from flask import Response
    import csv
    import io

    sql = """
    SELECT
        'OD' AS journal_code,
        'Opérations diverses' AS journal_lib,
        e.id AS ecriture_num,
        TO_CHAR(e.date_ecriture, 'YYYYMMDD') AS ecriture_date,
        l.compte AS compte_num,
        COALESCE(pc.libelle,'Compte inconnu') AS compte_lib,
        '' AS comp_aux_num,
        '' AS comp_aux_lib,
        COALESCE(e.piece,'') AS piece_ref,
        TO_CHAR(e.date_ecriture, 'YYYYMMDD') AS piece_date,
        COALESCE(e.libelle,'') AS ecriture_lib,
        l.debit AS debit,
        l.credit AS credit,
        '' AS ecriture_let,
        '' AS date_let,
        TO_CHAR(e.date_ecriture, 'YYYYMMDD') AS valid_date,
        '' AS montant_devise,
        '' AS idevise
    FROM ecritures_v3 e
    JOIN lignes_ecritures_v3 l ON l.ecriture_id = e.id
    LEFT JOIN plan_comptable pc ON pc.numero = l.compte
    ORDER BY e.date_ecriture, e.id, l.id
    """

    with engine.begin() as conn:
        rows = conn.execute(text(sql)).mappings().all()

    output = io.StringIO()
    writer = csv.writer(output, delimiter='|', lineterminator='\n')

    writer.writerow([
        "JournalCode", "JournalLib", "EcritureNum", "EcritureDate",
        "CompteNum", "CompteLib", "CompAuxNum", "CompAuxLib",
        "PieceRef", "PieceDate", "EcritureLib", "Debit", "Credit",
        "EcritureLet", "DateLet", "ValidDate", "Montantdevise", "Idevise"
    ])

    for r in rows:
        writer.writerow([
            r["journal_code"],
            r["journal_lib"],
            r["ecriture_num"],
            r["ecriture_date"],
            r["compte_num"],
            r["compte_lib"],
            r["comp_aux_num"],
            r["comp_aux_lib"],
            r["piece_ref"],
            r["piece_date"],
            r["ecriture_lib"],
            r["debit"],
            r["credit"],
            r["ecriture_let"],
            r["date_let"],
            r["valid_date"],
            r["montant_devise"],
            r["idevise"],
        ])

    data = output.getvalue()
    output.close()

    return Response(
        data,
        mimetype="text/plain; charset=utf-8",
        headers={
            "Content-Disposition": "attachment; filename=FEC_ComptaPilot_V3.txt"
        }
    )



@api_metier_refonte.get("/api/refonte/compte-resultat")
def api_compte_resultat():

    sql = """
    SELECT
        l.compte,
        COALESCE(pc.libelle,'Compte inconnu') AS libelle,
        SUBSTRING(l.compte,1,1) AS classe,
        SUM(COALESCE(l.debit,0)) AS debit,
        SUM(COALESCE(l.credit,0)) AS credit
    FROM lignes_ecritures_v3 l
    LEFT JOIN plan_comptable pc ON pc.numero = l.compte
    WHERE SUBSTRING(l.compte,1,1) IN ('6','7')
    GROUP BY l.compte, pc.libelle
    ORDER BY l.compte
    """

    with engine.begin() as conn:
        rows = conn.execute(text(sql)).mappings().all()

    charges = []
    produits = []

    total_charges = 0
    total_produits = 0

    for r in rows:
        debit = float(r["debit"] or 0)
        credit = float(r["credit"] or 0)

        item = {
            "compte": r["compte"],
            "libelle": r["libelle"],
            "debit": debit,
            "credit": credit,
            "montant": debit - credit if r["classe"] == "6" else credit - debit,
        }

        if r["classe"] == "6":
            total_charges += item["montant"]
            charges.append(item)
        elif r["classe"] == "7":
            total_produits += item["montant"]
            produits.append(item)

    resultat = total_produits - total_charges

    return jsonify({
        "success": True,
        "total_charges": total_charges,
        "total_produits": total_produits,
        "resultat": resultat,
        "type_resultat": "BENEFICE" if resultat >= 0 else "PERTE",
        "charges": charges,
        "produits": produits,
    })



@api_metier_refonte.get("/api/refonte/bilan")
def api_bilan():

    sql = """
    SELECT
        l.compte,
        COALESCE(pc.libelle,'Compte inconnu') AS libelle,
        SUBSTRING(l.compte,1,1) AS classe,
        SUM(COALESCE(l.debit,0)) AS debit,
        SUM(COALESCE(l.credit,0)) AS credit
    FROM lignes_ecritures_v3 l
    LEFT JOIN plan_comptable pc ON pc.numero = l.compte
    WHERE SUBSTRING(l.compte,1,1) IN ('1','2','3','4','5')
    GROUP BY l.compte, pc.libelle
    ORDER BY l.compte
    """

    with engine.begin() as conn:
        rows = conn.execute(text(sql)).mappings().all()

    actif = []
    passif = []
    total_actif = 0
    total_passif = 0

    for r in rows:
        debit = float(r["debit"] or 0)
        credit = float(r["credit"] or 0)
        solde = debit - credit

        item = {
            "compte": r["compte"],
            "libelle": r["libelle"],
            "debit": debit,
            "credit": credit,
            "solde": solde,
        }

        compte = str(r["compte"] or "")
        classe = str(r["classe"] or "")

        # Classement bilan par nature comptable.
        # - Classe 1 : capitaux propres / dettes financières => passif
        # - Comptes 28 : amortissements => passif / correction d'actif
        # - Classe 2 hors 28 : immobilisations => actif
        # - Classe 3 : stocks => actif
        # - Classe 4 : tiers, actif si débiteur, passif si créditeur
        # - Classe 5 : trésorerie, actif si débiteur, passif si créditeur
        if classe == "1" or compte.startswith("28"):
            item["solde"] = abs(solde)
            passif.append(item)
            total_passif += abs(solde)
        elif classe in ("2", "3"):
            item["solde"] = abs(solde)
            actif.append(item)
            total_actif += abs(solde)
        elif classe in ("4", "5"):
            if solde >= 0:
                item["solde"] = abs(solde)
                actif.append(item)
                total_actif += abs(solde)
            else:
                item["solde"] = abs(solde)
                passif.append(item)
                total_passif += abs(solde)
        else:
            if solde >= 0:
                item["solde"] = abs(solde)
                actif.append(item)
                total_actif += abs(solde)
            else:
                item["solde"] = abs(solde)
                passif.append(item)
                total_passif += abs(solde)

    return jsonify({
        "success": True,
        "total_actif": total_actif,
        "total_passif": total_passif,
        "equilibre": round(total_actif, 2) == round(total_passif, 2),
        "actif": actif,
        "passif": passif,
    })



@api_metier_refonte.post("/api/refonte/ocr/analyser-comptabiliser")
def api_ocr_analyser_comptabiliser():
    from app_refonte.services.ocr_ia_service import analyser_facture, generer_ecriture_achat
    from app_refonte.services.validation_service import controle_equilibre_piece
    from app_refonte.services.comptabilisation_ocr_service import comptabiliser_ecriture_ocr

    data = request.get_json(silent=True) or {}
    texte = data.get("texte", "")

    analyse = analyser_facture(texte)
    ecriture = generer_ecriture_achat(analyse)
    controle = controle_equilibre_piece(ecriture["lignes"])

    if not controle["equilibre"]:
        return jsonify({
            "success": False,
            "analyse": analyse,
            "ecriture": ecriture,
            "controle": controle,
            "error": "Ecriture déséquilibrée"
        }), 400

    comptabilisation = comptabiliser_ecriture_ocr(ecriture, client_id=1)

    return jsonify({
        "success": True,
        "analyse": analyse,
        "ecriture": ecriture,
        "controle": controle,
        "comptabilisation": comptabilisation,
    })



@api_metier_refonte.post("/api/refonte/ocr/upload-pdf")
def api_ocr_upload_pdf():
    from pathlib import Path
    from werkzeug.utils import secure_filename
    from app_refonte.services.ocr_pdf_service import extraire_texte_pdf
    from app_refonte.services.ocr_ia_service import analyser_facture, generer_ecriture_achat
    from app_refonte.services.validation_service import controle_equilibre_piece
    from app_refonte.services.comptabilisation_ocr_service import comptabiliser_ecriture_ocr

    file = request.files.get("file")
    if not file:
        return jsonify({"success": False, "error": "Aucun fichier PDF transmis"}), 400

    upload_dir = Path("/app/uploads/ocr")
    upload_dir.mkdir(parents=True, exist_ok=True)

    filename = secure_filename(file.filename or "facture.pdf")
    path = upload_dir / filename
    file.save(path)

    texte = extraire_texte_pdf(path)

    analyse = analyser_facture(texte)
    ecriture = generer_ecriture_achat(analyse)
    controle = controle_equilibre_piece(ecriture["lignes"])

    if not controle["equilibre"]:
        return jsonify({
            "success": False,
            "texte_ocr": texte,
            "analyse": analyse,
            "ecriture": ecriture,
            "controle": controle,
            "error": "Ecriture déséquilibrée"
        }), 400

    comptabilisation = comptabiliser_ecriture_ocr(ecriture, client_id=1)

    with engine.begin() as conn:
        piece_id = conn.execute(text("""
            INSERT INTO pieces_v3 (
                client_id,
                nom_fichier,
                type_piece,
                chemin_stockage,
                statut_ocr,
                texte_ocr
            )
            VALUES (
                1,
                :nom_fichier,
                'FACTURE_ACHAT',
                :chemin_stockage,
                'TRAITE',
                :texte_ocr
            )
            RETURNING id
        """), {
            "nom_fichier": filename,
            "chemin_stockage": str(path),
            "texte_ocr": texte,
        }).scalar()

    return jsonify({
        "success": True,
        "piece_id": piece_id,
        "filename": filename,
        "texte_ocr": texte[:3000],
        "analyse": analyse,
        "ecriture": ecriture,
        "controle": controle,
        "comptabilisation": comptabilisation,
    })



@api_metier_refonte.post("/api/refonte/ocr/upload-pdf-a-valider")
def api_ocr_upload_pdf_a_valider():
    from pathlib import Path
    from werkzeug.utils import secure_filename
    from app_refonte.services.ocr_pdf_service import extraire_texte_pdf
    from app_refonte.services.ocr_ia_service import analyser_facture, generer_ecriture_achat
    from app_refonte.services.validation_service import controle_equilibre_piece
    import json

    file = request.files.get("file")
    if not file:
        return jsonify({"success": False, "error": "Aucun fichier PDF transmis"}), 400

    upload_dir = Path("/app/uploads/ocr")
    upload_dir.mkdir(parents=True, exist_ok=True)

    filename = secure_filename(file.filename or "facture.pdf")
    path = upload_dir / filename
    file.save(path)

    texte = extraire_texte_pdf(path)
    analyse = analyser_facture(texte)
    ecriture = generer_ecriture_achat(analyse)
    controle = controle_equilibre_piece(ecriture["lignes"])

    with engine.begin() as conn:
        piece_id = conn.execute(text("""
            INSERT INTO pieces_v3 (
                client_id,
                nom_fichier,
                type_piece,
                chemin_stockage,
                statut_ocr,
                texte_ocr,
                analyse_ia,
                ecriture_proposee,
                controle_ia,
                statut_validation
            )
            VALUES (
                1,
                :nom_fichier,
                'FACTURE_ACHAT',
                :chemin_stockage,
                'TRAITE',
                :texte_ocr,
                CAST(:analyse_ia AS JSONB),
                CAST(:ecriture_proposee AS JSONB),
                CAST(:controle_ia AS JSONB),
                'A_VALIDER'
            )
            RETURNING id
        """), {
            "nom_fichier": filename,
            "chemin_stockage": str(path),
            "texte_ocr": texte,
            "analyse_ia": json.dumps(analyse, ensure_ascii=False),
            "ecriture_proposee": json.dumps(ecriture, ensure_ascii=False),
            "controle_ia": json.dumps(controle, ensure_ascii=False),
        }).scalar()

    return jsonify({
        "success": True,
        "piece_id": piece_id,
        "statut_validation": "A_VALIDER",
        "filename": filename,
        "texte_ocr": texte[:3000],
        "analyse": analyse,
        "ecriture": ecriture,
        "controle": controle,
    })


@api_metier_refonte.get("/api/refonte/ocr/pieces-a-valider")
def api_pieces_a_valider():
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT id, nom_fichier, type_piece, statut_ocr, statut_validation,
                   analyse_ia, ecriture_proposee, controle_ia, created_at
            FROM pieces_v3
            WHERE statut_validation = 'A_VALIDER'
            ORDER BY id DESC
            LIMIT 100
        """)).mappings().all()

    return jsonify({
        "success": True,
        "total": len(rows),
        "pieces": [dict(r) for r in rows],
    })


@api_metier_refonte.post("/api/refonte/ocr/valider-piece")
def api_valider_piece_ocr():
    from app_refonte.services.comptabilisation_ocr_service import comptabiliser_ecriture_ocr

    data = request.get_json(silent=True) or {}
    piece_id = data.get("piece_id")

    if not piece_id:
        return jsonify({"success": False, "error": "piece_id obligatoire"}), 400

    with engine.begin() as conn:
        piece = conn.execute(text("""
            SELECT id, ecriture_proposee, controle_ia
            FROM pieces_v3
            WHERE id = :id
        """), {"id": piece_id}).mappings().first()

    if not piece:
        return jsonify({"success": False, "error": "Pièce introuvable"}), 404

    ecriture = piece["ecriture_proposee"]
    controle = piece["controle_ia"]

    if not controle or not controle.get("equilibre"):
        return jsonify({"success": False, "error": "Ecriture proposée déséquilibrée"}), 400

    comptabilisation = comptabiliser_ecriture_ocr(ecriture, client_id=1)
    ecriture_id = comptabilisation["ecriture_id"]

    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE pieces_v3
            SET statut_validation = 'COMPTABILISEE',
                ecriture_id = :ecriture_id
            WHERE id = :piece_id
        """), {
            "piece_id": piece_id,
            "ecriture_id": ecriture_id,
        })

    return jsonify({
        "success": True,
        "piece_id": piece_id,
        "statut_validation": "COMPTABILISEE",
        "ecriture_id": ecriture_id,
    })



@api_metier_refonte.post("/api/refonte/banque/seed-demo")
def api_banque_seed_initial():
    operations = [
        {"date_operation": "2026-05-29", "libelle": "Echeance emprunt mois 1", "montant": -8492.16},
        {"date_operation": "2026-05-29", "libelle": "Facture Orange", "montant": -120.00},
        {"date_operation": "2026-05-29", "libelle": "Frais bancaires", "montant": -12.50},
    ]

    ids = []
    with engine.begin() as conn:
        for op in operations:
            oid = conn.execute(text("""
                INSERT INTO operations_bancaires_v3 (
                    client_id, date_operation, libelle, montant
                )
                VALUES (
                    1, :date_operation, :libelle, :montant
                )
                RETURNING id
            """), op).scalar()
            ids.append(oid)

    return jsonify({"success": True, "operation_ids": ids})


@api_metier_refonte.get("/api/refonte/banque/operations")
def api_banque_operations():
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT id, client_id, date_operation, libelle, montant, compte_banque, statut
            FROM operations_bancaires_v3
            ORDER BY id DESC
            LIMIT 200
        """)).mappings().all()

    return jsonify({
        "success": True,
        "total": len(rows),
        "operations": [dict(r) for r in rows],
    })


@api_metier_refonte.get("/api/refonte/banque/propositions")
def api_banque_propositions():
    from app_refonte.services.rapprochement_bancaire_service import proposer_rapprochements

    with engine.begin() as conn:
        operations = conn.execute(text("""
            SELECT id, date_operation, libelle, montant
            FROM operations_bancaires_v3
            WHERE statut = 'A_RAPPROCHER'
            ORDER BY date_operation, id
        """)).mappings().all()

        ecritures = conn.execute(text("""
            SELECT
                e.id AS ecriture_id,
                e.date_ecriture,
                e.piece,
                e.libelle,
                l.compte,
                l.debit,
                l.credit
            FROM ecritures_v3 e
            JOIN lignes_ecritures_v3 l ON l.ecriture_id = e.id
            WHERE l.compte = '512000'
            ORDER BY e.date_ecriture, e.id
        """)).mappings().all()

    propositions = proposer_rapprochements(
        [dict(o) for o in operations],
        [dict(e) for e in ecritures],
        seuil=70
    )

    return jsonify({
        "success": True,
        "total": len(propositions),
        "propositions": propositions,
    })


@api_metier_refonte.post("/api/refonte/banque/valider-rapprochement")
def api_banque_valider_rapprochement():
    data = request.get_json(silent=True) or {}
    operation_id = data.get("operation_id")
    ecriture_id = data.get("ecriture_id")
    score = data.get("score", 0)

    if not operation_id or not ecriture_id:
        return jsonify({"success": False, "error": "operation_id et ecriture_id obligatoires"}), 400

    with engine.begin() as conn:
        rid = conn.execute(text("""
            INSERT INTO rapprochements_bancaires_v3 (
                operation_id, ecriture_id, score, statut
            )
            VALUES (
                :operation_id, :ecriture_id, :score, 'VALIDE'
            )
            RETURNING id
        """), {
            "operation_id": operation_id,
            "ecriture_id": ecriture_id,
            "score": score,
        }).scalar()

        conn.execute(text("""
            UPDATE operations_bancaires_v3
            SET statut = 'RAPPROCHE'
            WHERE id = :operation_id
        """), {"operation_id": operation_id})

    return jsonify({
        "success": True,
        "rapprochement_id": rid,
        "operation_id": operation_id,
        "ecriture_id": ecriture_id,
    })



@api_metier_refonte.post("/api/refonte/lettrage/seed-paiement-demo")
def api_lettrage_seed_paiement_initial():
    with engine.begin() as conn:
        ecriture_id = conn.execute(text("""
            INSERT INTO ecritures_v3 (
                client_id, date_ecriture, piece, libelle, statut, source
            )
            VALUES (
                1, CURRENT_DATE, 'PAY-ORANGE-1', 'Paiement facture Orange', 'VALIDE', 'PAIEMENT_DEMO'
            )
            RETURNING id
        """)).scalar()

        conn.execute(text("""
            INSERT INTO lignes_ecritures_v3 (ecriture_id, compte, libelle, debit, credit)
            VALUES (:ecriture_id, '401000', 'Paiement facture Orange', 120.00, 0)
        """), {"ecriture_id": ecriture_id})

        conn.execute(text("""
            INSERT INTO lignes_ecritures_v3 (ecriture_id, compte, libelle, debit, credit)
            VALUES (:ecriture_id, '512000', 'Paiement facture Orange', 0, 120.00)
        """), {"ecriture_id": ecriture_id})

    return jsonify({"success": True, "ecriture_id": ecriture_id})


@api_metier_refonte.get("/api/refonte/lettrage/propositions")
def api_lettrage_propositions():
    compte = request.args.get("compte", "401000")

    with engine.begin() as conn:
        debits = conn.execute(text("""
            SELECT e.id AS ecriture_id, e.date_ecriture, e.piece, e.libelle, l.debit AS montant
            FROM ecritures_v3 e
            JOIN lignes_ecritures_v3 l ON l.ecriture_id = e.id
            WHERE l.compte = :compte AND l.debit > 0
            ORDER BY e.id
        """), {"compte": compte}).mappings().all()

        credits = conn.execute(text("""
            SELECT e.id AS ecriture_id, e.date_ecriture, e.piece, e.libelle, l.credit AS montant
            FROM ecritures_v3 e
            JOIN lignes_ecritures_v3 l ON l.ecriture_id = e.id
            WHERE l.compte = :compte AND l.credit > 0
            ORDER BY e.id
        """), {"compte": compte}).mappings().all()

        deja_lettres = conn.execute(text("""
            SELECT ecriture_debit_id, ecriture_credit_id
            FROM lettrages_tiers_v3
            WHERE compte = :compte
        """), {"compte": compte}).mappings().all()

    paires_existantes = {
        (r["ecriture_debit_id"], r["ecriture_credit_id"])
        for r in deja_lettres
    }

    propositions = []
    for d in debits:
        for c in credits:
            if (d["ecriture_id"], c["ecriture_id"]) in paires_existantes:
                continue

            if round(float(d["montant"]), 2) == round(float(c["montant"]), 2):
                propositions.append({
                    "compte": compte,
                    "debit": dict(d),
                    "credit": dict(c),
                    "montant": float(d["montant"]),
                    "score": 100,
                    "statut": "PROPOSE",
                })

    return jsonify({
        "success": True,
        "total": len(propositions),
        "propositions": propositions,
    })


@api_metier_refonte.post("/api/refonte/lettrage/valider")
def api_lettrage_valider():
    data = request.get_json(silent=True) or {}

    compte = data.get("compte", "401000")
    ecriture_debit_id = data.get("ecriture_debit_id")
    ecriture_credit_id = data.get("ecriture_credit_id")
    montant = data.get("montant")

    if not ecriture_debit_id or not ecriture_credit_id or not montant:
        return jsonify({"success": False, "error": "Données lettrage incomplètes"}), 400

    with engine.begin() as conn:
        lettre_num = conn.execute(text("SELECT COUNT(*) + 1 FROM lettrages_tiers_v3")).scalar()
        lettre = f"L{lettre_num}"

        lettrage_id = conn.execute(text("""
            INSERT INTO lettrages_tiers_v3 (
                client_id, compte, ecriture_debit_id, ecriture_credit_id, montant, lettre, statut
            )
            VALUES (
                1, :compte, :ecriture_debit_id, :ecriture_credit_id, :montant, :lettre, 'LETTRÉ'
            )
            RETURNING id
        """), {
            "compte": compte,
            "ecriture_debit_id": ecriture_debit_id,
            "ecriture_credit_id": ecriture_credit_id,
            "montant": montant,
            "lettre": lettre,
        }).scalar()

    return jsonify({
        "success": True,
        "lettrage_id": lettrage_id,
        "lettre": lettre,
    })


@api_metier_refonte.get("/api/refonte/lettrage")
def api_lettrage_liste():
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT id, compte, ecriture_debit_id, ecriture_credit_id, montant, lettre, statut, created_at
            FROM lettrages_tiers_v3
            ORDER BY id DESC
        """)).mappings().all()

    return jsonify({
        "success": True,
        "total": len(rows),
        "lettrages": [dict(r) for r in rows],
    })



@api_metier_refonte.get("/api/refonte/ocr/doublons")
def api_ocr_doublons():
    sql = """
    SELECT
        e.libelle,
        e.date_ecriture,
        l401.credit AS montant_ttc,
        COUNT(*) AS nombre,
        ARRAY_AGG(e.id ORDER BY e.id) AS ecriture_ids
    FROM ecritures_v3 e
    JOIN lignes_ecritures_v3 l401
         ON l401.ecriture_id = e.id
        AND l401.compte LIKE '401%'
        AND l401.credit > 0
    WHERE e.source = 'OCR_IA'
    GROUP BY e.libelle, e.date_ecriture, l401.credit
    HAVING COUNT(*) > 1
    ORDER BY nombre DESC, e.libelle
    """

    with engine.begin() as conn:
        rows = conn.execute(text(sql)).mappings().all()

    return jsonify({
        "success": True,
        "total": len(rows),
        "doublons": [dict(r) for r in rows],
    })



@api_metier_refonte.get("/api/refonte/tva/ca3")
def api_tva_ca3():

    with engine.begin() as conn:

        tva_collectee = conn.execute(text("""
            SELECT COALESCE(SUM(credit),0)
            FROM lignes_ecritures_v3
            WHERE compte='445710'
        """)).scalar() or 0

        tva_deductible_abs = conn.execute(text("""
            SELECT COALESCE(SUM(debit),0)
            FROM lignes_ecritures_v3
            WHERE compte='445660'
        """)).scalar() or 0

        tva_deductible_immo = conn.execute(text("""
            SELECT COALESCE(SUM(debit),0)
            FROM lignes_ecritures_v3
            WHERE compte='445620'
        """)).scalar() or 0

    tva_nette = (
        float(tva_collectee)
        - float(tva_deductible_abs)
        - float(tva_deductible_immo)
    )

    return jsonify({
        "success": True,
        "ca3": {
            "ligne_08_tva_collectee": float(tva_collectee),
            "ligne_20_tva_deductible_abs": float(tva_deductible_abs),
            "ligne_21_tva_deductible_immo": float(tva_deductible_immo),
            "ligne_28_tva_nette": round(tva_nette, 2),
            "statut": "A_PAYER" if tva_nette > 0 else "CREDIT_TVA"
        }
    })



@api_metier_refonte.get("/api/refonte/cloture/controle")
def api_cloture_controle():

    with engine.begin() as conn:
        balance = conn.execute(text("""
            SELECT
                SUM(COALESCE(debit,0)) AS total_debit,
                SUM(COALESCE(credit,0)) AS total_credit
            FROM lignes_ecritures_v3
        """)).mappings().first()

        resultat = conn.execute(text("""
            SELECT
                SUM(
                    CASE
                        WHEN compte LIKE '7%' THEN COALESCE(credit,0) - COALESCE(debit,0)
                        WHEN compte LIKE '6%' THEN COALESCE(debit,0) - COALESCE(credit,0)
                        ELSE 0
                    END
                ) AS resultat
            FROM lignes_ecritures_v3
            WHERE compte LIKE '6%' OR compte LIKE '7%'
        """)).scalar() or 0

        tiers_non_lettres = conn.execute(text("""
            SELECT COUNT(*) AS nb
            FROM lignes_ecritures_v3 l
            JOIN ecritures_v3 e ON e.id = l.ecriture_id
            WHERE (l.compte LIKE '401%' OR l.compte LIKE '411%')
              AND COALESCE(e.statut, '') <> 'ANNULE'
              AND e.id NOT IN (
                  SELECT ecriture_debit_id FROM lettrages_tiers_v3
                  UNION
                  SELECT ecriture_credit_id FROM lettrages_tiers_v3
              )
        """)).scalar() or 0

        banques_non_rapprochees = conn.execute(text("""
            SELECT COUNT(*) AS nb
            FROM operations_bancaires_v3
            WHERE statut <> 'RAPPROCHE'
        """)).scalar() or 0

    total_debit = float(balance["total_debit"] or 0)
    total_credit = float(balance["total_credit"] or 0)
    equilibre = round(total_debit, 2) == round(total_credit, 2)

    controles = [
        {
            "code": "BALANCE_EQUILIBREE",
            "libelle": "Balance débit/crédit équilibrée",
            "ok": equilibre,
            "detail": f"Débit {total_debit:.2f} / Crédit {total_credit:.2f}",
        },
        {
            "code": "TIERS_LETTRES",
            "libelle": "Comptes tiers lettrés",
            "ok": tiers_non_lettres == 0,
            "detail": f"{tiers_non_lettres} ligne(s) tiers non lettrée(s)",
        },
        {
            "code": "BANQUE_RAPPROCHEE",
            "libelle": "Banque rapprochée",
            "ok": banques_non_rapprochees == 0,
            "detail": f"{banques_non_rapprochees} opération(s) bancaire(s) non rapprochée(s)",
        },
    ]

    cloturable = all(c["ok"] for c in controles)

    return jsonify({
        "success": True,
        "cloturable": cloturable,
        "resultat": float(resultat),
        "type_resultat": "BENEFICE" if float(resultat) >= 0 else "PERTE",
        "controles": controles,
    })



@api_metier_refonte.get("/api/refonte/cloture/simulation")
def api_cloture_simulation():

    with engine.begin() as conn:
        exercice = conn.execute(text("""
            SELECT id, client_id, date_debut, date_fin, statut
            FROM exercices_v3
            WHERE statut = 'OUVERT'
            ORDER BY id
            LIMIT 1
        """)).mappings().first()

        resultat = conn.execute(text("""
            SELECT
                SUM(
                    CASE
                        WHEN compte LIKE '7%' THEN COALESCE(credit,0) - COALESCE(debit,0)
                        WHEN compte LIKE '6%' THEN COALESCE(debit,0) - COALESCE(credit,0)
                        ELSE 0
                    END
                ) AS resultat
            FROM lignes_ecritures_v3
            WHERE compte LIKE '6%' OR compte LIKE '7%'
        """)).scalar() or 0

    if not exercice:
        return jsonify({
            "success": False,
            "error": "Aucun exercice ouvert trouvé"
        }), 404

    resultat_float = float(resultat)

    if resultat_float >= 0:
        ecriture_cloture = {
            "libelle": "Affectation résultat bénéficiaire",
            "lignes": [
                {"compte": "120000", "debit": 0, "credit": resultat_float},
                {"compte": "129000", "debit": resultat_float, "credit": 0},
            ]
        }
    else:
        perte = abs(resultat_float)
        ecriture_cloture = {
            "libelle": "Affectation résultat déficitaire",
            "lignes": [
                {"compte": "129000", "debit": perte, "credit": 0},
                {"compte": "120000", "debit": 0, "credit": perte},
            ]
        }

    return jsonify({
        "success": True,
        "exercice": dict(exercice),
        "resultat": resultat_float,
        "type_resultat": "BENEFICE" if resultat_float >= 0 else "PERTE",
        "simulation_ecriture": ecriture_cloture,
    })



@api_metier_refonte.post("/api/refonte/cloture/definitive")
def api_cloture_definitive():

    with engine.begin() as conn:
        exercice = conn.execute(text("""
            SELECT id, client_id, date_debut, date_fin, statut
            FROM exercices_v3
            WHERE statut = 'OUVERT'
            ORDER BY id
            LIMIT 1
        """)).mappings().first()

        if not exercice:
            return jsonify({"success": False, "error": "Aucun exercice ouvert"}), 404

        balance = conn.execute(text("""
            SELECT SUM(COALESCE(debit,0)) AS total_debit,
                   SUM(COALESCE(credit,0)) AS total_credit
            FROM lignes_ecritures_v3
        """)).mappings().first()

        tiers_non_lettres = conn.execute(text("""
            SELECT COUNT(*)
            FROM lignes_ecritures_v3 l
            JOIN ecritures_v3 e ON e.id = l.ecriture_id
            WHERE (l.compte LIKE '401%' OR l.compte LIKE '411%')
              AND COALESCE(e.statut, '') <> 'ANNULE'
              AND e.id NOT IN (
                  SELECT ecriture_debit_id FROM lettrages_tiers_v3
                  UNION
                  SELECT ecriture_credit_id FROM lettrages_tiers_v3
              )
        """)).scalar() or 0

        banques_non_rapprochees = conn.execute(text("""
            SELECT COUNT(*)
            FROM operations_bancaires_v3
            WHERE statut <> 'RAPPROCHE'
        """)).scalar() or 0

        total_debit = float(balance["total_debit"] or 0)
        total_credit = float(balance["total_credit"] or 0)

        blocages = []

        if round(total_debit, 2) != round(total_credit, 2):
            blocages.append("Balance déséquilibrée")

        if tiers_non_lettres > 0:
            blocages.append(f"{tiers_non_lettres} ligne(s) tiers non lettrée(s)")

        if banques_non_rapprochees > 0:
            blocages.append(f"{banques_non_rapprochees} opération(s) bancaire(s) non rapprochée(s)")

        if blocages:
            return jsonify({
                "success": False,
                "cloture_refusee": True,
                "blocages": blocages,
            }), 400

        resultat = conn.execute(text("""
            SELECT
                SUM(
                    CASE
                        WHEN compte LIKE '7%' THEN COALESCE(credit,0) - COALESCE(debit,0)
                        WHEN compte LIKE '6%' THEN COALESCE(debit,0) - COALESCE(credit,0)
                        ELSE 0
                    END
                ) AS resultat
            FROM lignes_ecritures_v3
            WHERE compte LIKE '6%' OR compte LIKE '7%'
        """)).scalar() or 0

        resultat_float = float(resultat)

        ecriture_id = conn.execute(text("""
            INSERT INTO ecritures_v3 (
                client_id,
                exercice_id,
                date_ecriture,
                piece,
                libelle,
                statut,
                source
            )
            VALUES (
                :client_id,
                :exercice_id,
                :date_fin,
                'CLOTURE',
                'Ecriture de clôture exercice',
                'VALIDE',
                'CLOTURE_AUTO'
            )
            RETURNING id
        """), {
            "client_id": exercice["client_id"],
            "exercice_id": exercice["id"],
            "date_fin": exercice["date_fin"],
        }).scalar()

        if resultat_float >= 0:
            lignes = [
                {"compte": "129000", "debit": resultat_float, "credit": 0},
                {"compte": "120000", "debit": 0, "credit": resultat_float},
            ]
        else:
            perte = abs(resultat_float)
            lignes = [
                {"compte": "129000", "debit": 0, "credit": perte},
                {"compte": "120000", "debit": perte, "credit": 0},
            ]

        for ligne in lignes:
            conn.execute(text("""
                INSERT INTO lignes_ecritures_v3 (
                    ecriture_id, compte, libelle, debit, credit
                )
                VALUES (
                    :ecriture_id, :compte, 'Ecriture de clôture exercice', :debit, :credit
                )
            """), {
                "ecriture_id": ecriture_id,
                "compte": ligne["compte"],
                "debit": ligne["debit"],
                "credit": ligne["credit"],
            })

        conn.execute(text("""
            UPDATE exercices_v3
            SET statut = 'CLOTURE',
                date_cloture = CURRENT_TIMESTAMP,
                resultat_cloture = :resultat
            WHERE id = :id
        """), {
            "id": exercice["id"],
            "resultat": resultat_float,
        })

    return jsonify({
        "success": True,
        "exercice_id": exercice["id"],
        "ecriture_cloture_id": ecriture_id,
        "resultat": resultat_float,
        "statut": "CLOTURE",
    })


@api_metier_refonte.get("/api/refonte/exercices")
def api_exercices_liste():
    with engine.begin() as conn:
        exercices = conn.execute(text("""
            SELECT
                id,
                client_id,
                date_debut,
                date_fin,
                statut,
                date_cloture,
                resultat_cloture,
                created_at
            FROM exercices_v3
            ORDER BY date_debut DESC, id DESC
        """)).mappings().all()

        ecritures = conn.execute(text("""
            SELECT
                e.id,
                e.exercice_id,
                e.date_ecriture,
                e.piece,
                e.libelle,
                e.statut,
                e.source,
                SUM(l.debit) AS total_debit,
                SUM(l.credit) AS total_credit
            FROM ecritures_v3 e
            LEFT JOIN lignes_ecritures_v3 l ON l.ecriture_id = e.id
            WHERE e.source IN ('CLOTURE_AUTO', 'A_NOUVEAUX_AUTO')
              AND COALESCE(e.statut, '') <> 'ANNULE'
            GROUP BY e.id
            ORDER BY e.date_ecriture DESC, e.id DESC
        """)).mappings().all()

    return jsonify({
        "success": True,
        "total": len(exercices),
        "exercices": [dict(r) for r in exercices],
        "ecritures_speciales": [dict(r) for r in ecritures],
    })


@api_metier_refonte.post("/api/refonte/exercice/verrouiller")
def api_exercice_verrouiller():
    data = request.get_json(silent=True) or {}
    exercice_id = data.get("exercice_id")

    if not exercice_id:
        return jsonify({"success": False, "error": "exercice_id obligatoire"}), 400

    with engine.begin() as conn:
        row = conn.execute(text("""
            UPDATE exercices_v3
            SET statut = 'VERROUILLE'
            WHERE id = :id
              AND statut = 'CLOTURE'
            RETURNING id, statut
        """), {"id": exercice_id}).mappings().first()

    if not row:
        return jsonify({
            "success": False,
            "error": "Exercice introuvable ou non clôturé"
        }), 400

    return jsonify({"success": True, "exercice": dict(row)})


@api_metier_refonte.post("/api/refonte/a-nouveaux/generer")
def api_a_nouveaux_generer():
    data = request.get_json(silent=True) or {}
    exercice_source_id = data.get("exercice_source_id")
    exercice_cible_id = data.get("exercice_cible_id")
    autoriser_compte_attente = bool(data.get("autoriser_compte_attente", False))

    if not exercice_source_id or not exercice_cible_id:
        return jsonify({
            "success": False,
            "error": "exercice_source_id et exercice_cible_id obligatoires"
        }), 400

    with engine.begin() as conn:
        source = conn.execute(text("""
            SELECT id, client_id, date_debut, date_fin, statut
            FROM exercices_v3
            WHERE id = :id
        """), {"id": exercice_source_id}).mappings().first()

        cible = conn.execute(text("""
            SELECT id, client_id, date_debut, date_fin, statut
            FROM exercices_v3
            WHERE id = :id
        """), {"id": exercice_cible_id}).mappings().first()

        if not source or not cible:
            return jsonify({"success": False, "error": "Exercice source ou cible introuvable"}), 404

        existant = conn.execute(text("""
            SELECT id
            FROM ecritures_v3
            WHERE exercice_id = :exercice_cible_id
              AND source = 'A_NOUVEAUX_AUTO'
              AND COALESCE(statut, '') <> 'ANNULE'
            ORDER BY id DESC
            LIMIT 1
        """), {"exercice_cible_id": exercice_cible_id}).scalar()

        if existant:
            return jsonify({
                "success": False,
                "error": "Des à-nouveaux actifs existent déjà pour cet exercice",
                "ecriture_id": existant,
            }), 400

        soldes = conn.execute(text("""
            SELECT
                l.compte,
                ROUND(SUM(l.debit - l.credit), 2) AS solde
            FROM lignes_ecritures_v3 l
            JOIN ecritures_v3 e ON e.id = l.ecriture_id
            WHERE e.exercice_id = :exercice_source_id
              AND COALESCE(e.statut, '') <> 'ANNULE'
              AND (
                l.compte LIKE '1%'
                OR l.compte LIKE '2%'
                OR l.compte LIKE '3%'
                OR l.compte LIKE '4%'
                OR l.compte LIKE '5%'
              )
              AND l.compte <> '129000'
            GROUP BY l.compte
            HAVING ROUND(SUM(l.debit - l.credit), 2) <> 0
            ORDER BY l.compte
        """), {"exercice_source_id": exercice_source_id}).mappings().all()

        ecriture_id = conn.execute(text("""
            INSERT INTO ecritures_v3 (
                client_id, exercice_id, date_ecriture, piece, libelle, statut, source
            )
            VALUES (
                :client_id,
                :exercice_cible_id,
                :date_debut,
                :piece,
                :libelle,
                'VALIDE',
                'A_NOUVEAUX_AUTO'
            )
            RETURNING id
        """), {
            "client_id": cible["client_id"],
            "exercice_cible_id": cible["id"],
            "date_debut": cible["date_debut"],
            "piece": f"AN-{str(cible['date_debut'])[:4]}",
            "libelle": f"A-nouveaux ouverture exercice {str(cible['date_debut'])[:4]}",
        }).scalar()

        total_debit = 0.0
        total_credit = 0.0

        for row in soldes:
            compte = row["compte"]
            solde = float(row["solde"] or 0)

            debit = solde if solde > 0 else 0
            credit = abs(solde) if solde < 0 else 0
            total_debit += debit
            total_credit += credit

            conn.execute(text("""
                INSERT INTO lignes_ecritures_v3 (
                    ecriture_id, compte, libelle, debit, credit
                )
                VALUES (
                    :ecriture_id, :compte, :libelle, :debit, :credit
                )
            """), {
                "ecriture_id": ecriture_id,
                "compte": compte,
                "libelle": "A-nouveaux ouverture exercice",
                "debit": round(debit, 2),
                "credit": round(credit, 2),
            })

        ecart = round(total_debit - total_credit, 2)

        if ecart != 0:
            if not autoriser_compte_attente:
                conn.execute(text("""
                    UPDATE ecritures_v3
                    SET statut = 'ANNULE',
                        libelle = libelle || ' - ANNULE CAR DESEQUILIBRE'
                    WHERE id = :id
                """), {"id": ecriture_id})
                return jsonify({
                    "success": False,
                    "error": "A-nouveaux déséquilibrés",
                    "ecart": ecart,
                    "ecriture_id": ecriture_id,
                }), 400

            conn.execute(text("""
                INSERT INTO lignes_ecritures_v3 (
                    ecriture_id, compte, libelle, debit, credit
                )
                VALUES (
                    :ecriture_id,
                    '471000',
                    'Compte attente équilibrage à-nouveaux',
                    :debit,
                    :credit
                )
            """), {
                "ecriture_id": ecriture_id,
                "debit": abs(ecart) if ecart < 0 else 0,
                "credit": ecart if ecart > 0 else 0,
            })

            if ecart < 0:
                total_debit += abs(ecart)
            else:
                total_credit += ecart

        return jsonify({
            "success": True,
            "ecriture_id": ecriture_id,
            "total_debit": round(total_debit, 2),
            "total_credit": round(total_credit, 2),
            "ecart": round(total_debit - total_credit, 2),
            "compte_attente_utilise": ecart != 0,
        })

@api_metier_refonte.get("/api/refonte/client-360")
def api_client_360():
    client_id = int(request.args.get("client_id", 1))

    with engine.begin() as conn:
        client = conn.execute(text("""
            SELECT id, siren, siret, raison_sociale, forme_juridique,
                   regime_fiscal, regime_tva, adresse, statut, created_at
            FROM clients_v3
            WHERE id = :client_id
        """), {"client_id": client_id}).mappings().first()

        if not client:
            return jsonify({"success": False, "error": "Client introuvable"}), 404

        kpis = conn.execute(text("""
            SELECT
                (SELECT COUNT(*) FROM ecritures_v3 WHERE client_id = :client_id AND COALESCE(statut,'') <> 'ANNULE') AS nb_ecritures,
                (SELECT COUNT(*) FROM pieces_v3 WHERE client_id = :client_id) AS nb_pieces,
                (SELECT COUNT(*) FROM factures_v3 WHERE client_id = :client_id) AS nb_factures,
                (SELECT COUNT(*) FROM immobilisations_v3 WHERE societe_id = :client_id) AS nb_immobilisations,
                (SELECT COUNT(*) FROM emprunts_v3 WHERE societe_id = :client_id) AS nb_emprunts,
                (SELECT COUNT(*) FROM lettrages_tiers_v3 WHERE client_id = :client_id) AS nb_lettrages,
                (
  SELECT COUNT(*)
  FROM rapprochements_bancaires_v3 rb
  JOIN operations_bancaires_v3 ob ON ob.id = rb.operation_id
  WHERE ob.client_id = :client_id
) AS nb_rapprochements,
                (SELECT COUNT(*) FROM operations_bancaires_v3 WHERE client_id = :client_id AND statut <> 'RAPPROCHE') AS banque_a_rapprocher,
                (SELECT COUNT(*) FROM exercices_v3 WHERE client_id = :client_id AND statut='OUVERT') AS exercices_ouverts,
                (SELECT COUNT(*) FROM exercices_v3 WHERE client_id = :client_id AND statut IN ('CLOTURE','VERROUILLE')) AS exercices_clotures
        """), {"client_id": client_id}).mappings().first()

        exercices = conn.execute(text("""
            SELECT id, date_debut, date_fin, statut, date_cloture, resultat_cloture
            FROM exercices_v3
            WHERE client_id = :client_id
            ORDER BY date_debut DESC
        """), {"client_id": client_id}).mappings().all()

        ecritures_speciales = conn.execute(text("""
            SELECT id, exercice_id, date_ecriture, piece, libelle, statut, source
            FROM ecritures_v3
            WHERE client_id = :client_id
              AND source IN ('CLOTURE_AUTO', 'A_NOUVEAUX_AUTO')
              AND COALESCE(statut,'') <> 'ANNULE'
            ORDER BY date_ecriture DESC, id DESC
        """), {"client_id": client_id}).mappings().all()

    return jsonify({
        "success": True,
        "client": dict(client),
        "kpis": dict(kpis),
        "exercices": [dict(r) for r in exercices],
        "ecritures_speciales": [dict(r) for r in ecritures_speciales],
    })

@api_metier_refonte.get("/api/refonte/workflow-cabinet")
def api_workflow_cabinet():
    client_id = int(request.args.get("client_id", 1))

    with engine.begin() as conn:
        taches = conn.execute(text("""
            SELECT
                t.id,
                t.client_id,
                c.raison_sociale,
                t.titre,
                t.priorite,
                t.statut,
                t.echeance,
                t.created_at
            FROM taches_cabinet_v3 t
            LEFT JOIN clients_v3 c ON c.id = t.client_id
            WHERE t.client_id = :client_id
            ORDER BY
                CASE t.priorite
                    WHEN 'CRITIQUE' THEN 1
                    WHEN 'HAUTE' THEN 2
                    WHEN 'WARNING' THEN 3
                    WHEN 'NORMALE' THEN 4
                    ELSE 5
                END,
                t.id
        """), {"client_id": client_id}).mappings().all()

    colonnes = ["A_FAIRE", "EN_COURS", "REVISION", "VALIDATION_EC", "TERMINE"]
    kanban = {c: [] for c in colonnes}

    for t in taches:
        statut = t["statut"] or "A_FAIRE"
        if statut not in kanban:
            kanban[statut] = []
        kanban[statut].append(dict(t))

    return jsonify({
        "success": True,
        "client_id": client_id,
        "total": len(taches),
        "colonnes": colonnes,
        "kanban": kanban,
    })


@api_metier_refonte.post("/api/refonte/workflow-cabinet/statut")
def api_workflow_cabinet_statut():
    data = request.get_json(silent=True) or {}
    tache_id = data.get("tache_id")
    statut = data.get("statut")

    statuts_autorises = ["A_FAIRE", "EN_COURS", "REVISION", "VALIDATION_EC", "TERMINE"]

    if not tache_id or statut not in statuts_autorises:
        return jsonify({
            "success": False,
            "error": "tache_id obligatoire et statut invalide"
        }), 400

    with engine.begin() as conn:
        row = conn.execute(text("""
            UPDATE taches_cabinet_v3
            SET statut = :statut
            WHERE id = :tache_id
            RETURNING id, client_id, titre, priorite, statut, echeance
        """), {
            "tache_id": tache_id,
            "statut": statut,
        }).mappings().first()

    if not row:
        return jsonify({"success": False, "error": "Tâche introuvable"}), 404

    return jsonify({"success": True, "tache": dict(row)})

@api_metier_refonte.get("/api/refonte/supervision-cabinet")
def api_supervision_cabinet():
    with engine.begin() as conn:
        dossiers = conn.execute(text("""
            SELECT
                c.id,
                c.raison_sociale,
                c.siren,
                c.statut,
                COUNT(DISTINCT e.id) AS nb_ecritures,
                COUNT(DISTINCT t.id) FILTER (WHERE t.statut <> 'TERMINE') AS nb_taches_ouvertes,
                COUNT(DISTINCT t.id) FILTER (WHERE t.priorite IN ('HAUTE','CRITIQUE') AND t.statut <> 'TERMINE') AS nb_taches_urgentes,
                COUNT(DISTINCT ex.id) FILTER (WHERE ex.statut = 'OUVERT') AS exercices_ouverts,
                COUNT(DISTINCT ex.id) FILTER (WHERE ex.statut IN ('CLOTURE','VERROUILLE')) AS exercices_clotures,
                COALESCE(MAX(ex.resultat_cloture), 0) AS dernier_resultat
            FROM clients_v3 c
            LEFT JOIN ecritures_v3 e ON e.client_id = c.id AND COALESCE(e.statut,'') <> 'ANNULE'
            LEFT JOIN taches_cabinet_v3 t ON t.client_id = c.id
            LEFT JOIN exercices_v3 ex ON ex.client_id = c.id
            GROUP BY c.id
            ORDER BY nb_taches_urgentes DESC, nb_taches_ouvertes DESC, c.id
        """)).mappings().all()

    total = len(dossiers)
    dossiers_a_traiter = len([d for d in dossiers if int(d["nb_taches_ouvertes"] or 0) > 0])
    urgences = sum(int(d["nb_taches_urgentes"] or 0) for d in dossiers)
    ecritures = sum(int(d["nb_ecritures"] or 0) for d in dossiers)

    return jsonify({
        "success": True,
        "kpis": {
            "total_dossiers": total,
            "dossiers_a_traiter": dossiers_a_traiter,
            "urgences": urgences,
            "ecritures": ecritures,
        },
        "dossiers": [dict(d) for d in dossiers],
    })

@api_metier_refonte.get("/api/refonte/production-cabinet")
def api_production_cabinet():
    with engine.begin() as conn:
        workflow = conn.execute(text("""
            SELECT
                w.id,
                w.client_id,
                c.raison_sociale,
                w.module,
                w.etape,
                w.statut,
                w.responsable,
                w.commentaire,
                w.created_at
            FROM workflow_cabinet_v3 w
            LEFT JOIN clients_v3 c ON c.id = w.client_id
            ORDER BY
                CASE w.statut
                    WHEN 'A_FAIRE' THEN 1
                    WHEN 'EN_COURS' THEN 2
                    WHEN 'REVISION' THEN 3
                    WHEN 'VALIDATION_EC' THEN 4
                    WHEN 'TERMINE' THEN 5
                    ELSE 6
                END,
                w.id
        """)).mappings().all()

        taches = conn.execute(text("""
            SELECT
                t.id,
                t.client_id,
                c.raison_sociale,
                t.titre,
                t.priorite,
                t.statut,
                t.echeance,
                t.created_at
            FROM taches_cabinet_v3 t
            LEFT JOIN clients_v3 c ON c.id = t.client_id
            ORDER BY
                CASE t.priorite
                    WHEN 'CRITIQUE' THEN 1
                    WHEN 'HAUTE' THEN 2
                    WHEN 'WARNING' THEN 3
                    WHEN 'NORMALE' THEN 4
                    ELSE 5
                END,
                t.id
        """)).mappings().all()

    statuts = ["A_FAIRE", "EN_COURS", "REVISION", "VALIDATION_EC", "TERMINE"]
    modules = ["ONBOARDING", "IMPORT", "OCR", "REVISION", "CLOTURE"]

    kpis = {
        "workflow_total": len(workflow),
        "workflow_a_faire": len([w for w in workflow if w["statut"] == "A_FAIRE"]),
        "workflow_en_cours": len([w for w in workflow if w["statut"] == "EN_COURS"]),
        "workflow_revision": len([w for w in workflow if w["statut"] == "REVISION"]),
        "workflow_validation_ec": len([w for w in workflow if w["statut"] == "VALIDATION_EC"]),
        "workflow_termine": len([w for w in workflow if w["statut"] == "TERMINE"]),
        "taches_ouvertes": len([t for t in taches if t["statut"] != "TERMINE"]),
        "taches_urgentes": len([t for t in taches if t["priorite"] in ("HAUTE", "CRITIQUE") and t["statut"] != "TERMINE"]),
    }

    return jsonify({
        "success": True,
        "kpis": kpis,
        "statuts": statuts,
        "modules": modules,
        "workflow": [dict(w) for w in workflow],
        "taches": [dict(t) for t in taches],
    })


@api_metier_refonte.post("/api/refonte/production-cabinet/statut")
def api_production_cabinet_statut():
    data = request.get_json(silent=True) or {}
    workflow_id = data.get("workflow_id")
    statut = data.get("statut")

    statuts_autorises = ["A_FAIRE", "EN_COURS", "REVISION", "VALIDATION_EC", "TERMINE"]

    if not workflow_id or statut not in statuts_autorises:
        return jsonify({
            "success": False,
            "error": "workflow_id obligatoire et statut invalide"
        }), 400

    with engine.begin() as conn:
        row = conn.execute(text("""
            UPDATE workflow_cabinet_v3
            SET statut = :statut
            WHERE id = :workflow_id
            RETURNING id, client_id, module, etape, statut, responsable, commentaire
        """), {
            "workflow_id": workflow_id,
            "statut": statut,
        }).mappings().first()

    if not row:
        return jsonify({"success": False, "error": "Workflow introuvable"}), 404

    return jsonify({"success": True, "workflow": dict(row)})

@api_metier_refonte.get("/api/refonte/centre-fiscal")
def api_centre_fiscal():
    with engine.begin() as conn:
        tva = conn.execute(text("""
            SELECT
                COALESCE(SUM(CASE WHEN compte LIKE '4457%' THEN credit - debit ELSE 0 END),0) AS tva_collectee,
                COALESCE(SUM(CASE WHEN compte LIKE '4456%' THEN debit - credit ELSE 0 END),0) AS tva_deductible
            FROM lignes_ecritures_v3 l
            JOIN ecritures_v3 e ON e.id = l.ecriture_id
            WHERE COALESCE(e.statut,'') <> 'ANNULE'
        """)).mappings().first()

        resultat = conn.execute(text("""
            SELECT
                COALESCE(SUM(CASE WHEN l.compte LIKE '7%' THEN l.credit - l.debit ELSE 0 END),0) AS produits,
                COALESCE(SUM(CASE WHEN l.compte LIKE '6%' THEN l.debit - l.credit ELSE 0 END),0) AS charges
            FROM lignes_ecritures_v3 l
            JOIN ecritures_v3 e ON e.id = l.ecriture_id
            WHERE COALESCE(e.statut,'') <> 'ANNULE'
        """)).mappings().first()

        exercices = conn.execute(text("""
            SELECT id, date_debut, date_fin, statut, resultat_cloture
            FROM exercices_v3
            ORDER BY date_debut DESC
        """)).mappings().all()

        controles = {
            "fec_disponible": True,
            "balance_disponible": True,
            "bilan_disponible": True,
            "compte_resultat_disponible": True,
        }

    tva_collectee = float(tva["tva_collectee"] or 0)
    tva_deductible = float(tva["tva_deductible"] or 0)
    tva_a_payer = round(tva_collectee - tva_deductible, 2)

    produits = float(resultat["produits"] or 0)
    charges = float(resultat["charges"] or 0)
    resultat_fiscal = round(produits - charges, 2)

    return jsonify({
        "success": True,
        "tva": {
            "collectee": tva_collectee,
            "deductible": tva_deductible,
            "a_payer": tva_a_payer,
        },
        "resultat": {
            "produits": produits,
            "charges": charges,
            "resultat_fiscal": resultat_fiscal,
            "type": "BENEFICE" if resultat_fiscal >= 0 else "PERTE",
        },
        "exercices": [dict(e) for e in exercices],
        "controles": controles,
    })


@api_metier_refonte.get("/api/refonte/liasse-fiscale")
def api_liasse_fiscale_v3():
    client_id = int(request.args.get("client_id", 1))

    from app_refonte.services.autorisation_fiscale_service import verifier_autorisation_fiscale

    with engine.begin() as conn:
        client = conn.execute(text("""
            SELECT id, siren, siret, raison_sociale, forme_juridique,
                   regime_fiscal, regime_tva, adresse, statut
            FROM clients_v3
            WHERE id = :client_id
        """), {"client_id": client_id}).mappings().first()

        if not client:
            return jsonify({"success": False, "error": "Client introuvable"}), 404

        exercices = conn.execute(text("""
            SELECT id, date_debut, date_fin, statut, resultat_cloture
            FROM exercices_v3
            WHERE client_id = :client_id
            ORDER BY date_debut DESC
        """), {"client_id": client_id}).mappings().all()

        total_ecritures = conn.execute(text("""
            SELECT COUNT(*)
            FROM ecritures_v3
            WHERE client_id = :client_id
              AND COALESCE(statut,'') <> 'ANNULE'
        """), {"client_id": client_id}).scalar() or 0

        immos = conn.execute(text("""
            SELECT COUNT(*) AS nb, COALESCE(SUM(valeur_origine),0) AS valeur
            FROM immobilisations_v3
            WHERE societe_id = :client_id
              AND statut = 'ACTIVE'
        """), {"client_id": client_id}).mappings().first()

        emprunts = conn.execute(text("""
            SELECT COUNT(*) AS nb, COALESCE(SUM(capital),0) AS capital
            FROM emprunts_v3
            WHERE societe_id = :client_id
              AND statut = 'ACTIF'
        """), {"client_id": client_id}).mappings().first()

        factures = conn.execute(text("""
            SELECT COUNT(*) AS nb, COALESCE(SUM(montant_ht),0) AS ht,
                   COALESCE(SUM(montant_tva),0) AS tva,
                   COALESCE(SUM(montant_ttc),0) AS ttc
            FROM factures_v3
            WHERE client_id = :client_id
        """), {"client_id": client_id}).mappings().first()

        lignes = conn.execute(text("""
            SELECT
              COALESCE(SUM(CASE WHEN l.compte LIKE '6%' THEN l.debit - l.credit ELSE 0 END),0) AS charges,
              COALESCE(SUM(CASE WHEN l.compte LIKE '7%' THEN l.credit - l.debit ELSE 0 END),0) AS produits,
              COALESCE(SUM(CASE WHEN l.compte LIKE '2%' THEN l.debit - l.credit ELSE 0 END),0) AS actif_immo,
              COALESCE(SUM(CASE WHEN l.compte LIKE '1%' THEN l.credit - l.debit ELSE 0 END),0) AS capitaux,
              COALESCE(SUM(CASE WHEN l.compte LIKE '4%' THEN l.credit - l.debit ELSE 0 END),0) AS tiers,
              COALESCE(SUM(CASE WHEN l.compte LIKE '5%' THEN l.debit - l.credit ELSE 0 END),0) AS tresorerie
            FROM lignes_ecritures_v3 l
            JOIN ecritures_v3 e ON e.id = l.ecriture_id
            WHERE e.client_id = :client_id
              AND COALESCE(e.statut,'') <> 'ANNULE'
        """), {"client_id": client_id}).mappings().first()

    charges = float(lignes["charges"] or 0)
    produits = float(lignes["produits"] or 0)
    resultat = round(produits - charges, 2)

    actif_immo = float(lignes["actif_immo"] or 0)
    capitaux = float(lignes["capitaux"] or 0)
    tiers = float(lignes["tiers"] or 0)
    tresorerie = float(lignes["tresorerie"] or 0)

    valeur_immos = float(immos["valeur"] or 0)
    capital_emprunts = float(emprunts["capital"] or 0)

    total_actif = round(actif_immo + max(tiers, 0) + tresorerie, 2)
    total_passif = round(capitaux + capital_emprunts + abs(min(tiers, 0)), 2)

    formulaires = [
        {"formulaire": "2033-A", "rubrique": "Identification", "valeur": client["raison_sociale"], "statut": "PREPARE"},
        {"formulaire": "2033-A", "rubrique": "SIREN", "valeur": client["siren"], "statut": "PREPARE"},
        {"formulaire": "2033-A", "rubrique": "Actif immobilisé", "valeur": round(actif_immo or valeur_immos, 2), "statut": "CALCULE"},
        {"formulaire": "2033-A", "rubrique": "Créances / comptes de tiers", "valeur": round(max(tiers, 0), 2), "statut": "CALCULE"},
        {"formulaire": "2033-A", "rubrique": "Trésorerie", "valeur": round(tresorerie, 2), "statut": "CALCULE"},
        {"formulaire": "2033-A", "rubrique": "Total actif", "valeur": total_actif, "statut": "CALCULE"},
        {"formulaire": "2033-A", "rubrique": "Capitaux propres", "valeur": round(capitaux, 2), "statut": "CALCULE"},
        {"formulaire": "2033-A", "rubrique": "Dettes financières", "valeur": round(capital_emprunts, 2), "statut": "CALCULE"},
        {"formulaire": "2033-A", "rubrique": "Dettes tiers", "valeur": round(abs(min(tiers, 0)), 2), "statut": "CALCULE"},
        {"formulaire": "2033-A", "rubrique": "Total passif", "valeur": total_passif, "statut": "CALCULE"},
        {"formulaire": "2033-B", "rubrique": "Produits d'exploitation", "valeur": round(produits, 2), "statut": "CALCULE"},
        {"formulaire": "2033-B", "rubrique": "Charges d'exploitation", "valeur": round(charges, 2), "statut": "CALCULE"},
        {"formulaire": "2033-B", "rubrique": "Résultat fiscal", "valeur": resultat, "statut": "CALCULE"},
        {"formulaire": "2033-C", "rubrique": "Nombre immobilisations", "valeur": int(immos["nb"] or 0), "statut": "CALCULE"},
        {"formulaire": "2033-C", "rubrique": "Valeur immobilisations", "valeur": round(valeur_immos, 2), "statut": "CALCULE"},
        {"formulaire": "2033-C", "rubrique": "Nombre emprunts", "valeur": int(emprunts["nb"] or 0), "statut": "CALCULE"},
        {"formulaire": "2033-C", "rubrique": "Capital emprunts", "valeur": round(capital_emprunts, 2), "statut": "CALCULE"},
    ]

    autorisation = verifier_autorisation_fiscale()

    controles = {
        "client_identifie": bool(client["siren"] and client["raison_sociale"]),
        "exercice_present": len(exercices) > 0,
        "ecritures_presentes": total_ecritures > 0,
        "liasse_preparee": True,
        "bilan_equilibre": round(total_actif, 2) == round(total_passif, 2),
        "autorisation_fiscale": bool(autorisation.get("declarations_autorisees")),
    }

    return jsonify({
        "success": True,
        "client": dict(client),
        "autorisation": autorisation,
        "kpis": {
            "nb_exercices": len(exercices),
            "nb_ecritures": int(total_ecritures),
            "nb_immobilisations": int(immos["nb"] or 0),
            "nb_emprunts": int(emprunts["nb"] or 0),
            "nb_factures": int(factures["nb"] or 0),
            "valeur_immobilisations": round(valeur_immos, 2),
            "capital_emprunts": round(capital_emprunts, 2),
            "total_actif": total_actif,
            "total_passif": total_passif,
            "equilibre_bilan": round(total_actif, 2) == round(total_passif, 2),
            "resultat_fiscal": resultat,
            "type_resultat": "BENEFICE" if resultat >= 0 else "PERTE",
        },
        "statuts": {
            "2033-A": "PREPARE",
            "2033-B": "PREPARE",
            "2033-C": "PREPARE",
        },
        "controles": controles,
        "exercices": [dict(e) for e in exercices],
        "formulaires": formulaires,
    })



@api_metier_refonte.get("/api/refonte/liasse-fiscale/pdf")
def api_liasse_fiscale_pdf_v3():
    from app_refonte.services.liasse_pdf_v3_service import generer_pdf_liasse_v3

    client_id = int(request.args.get("client_id", 1))

    response = api_liasse_fiscale_v3()
    payload = response.get_json()

    if not payload or not payload.get("success"):
        return jsonify({"success": False, "error": "Liasse non générable"}), 400

    pdf = generer_pdf_liasse_v3(payload)

    return jsonify({
        "success": True,
        "pdf": pdf,
        "message": "PDF fiscal généré avec succès"
    })

@api_metier_refonte.get("/api/refonte/dossier-permanent")
def api_dossier_permanent():
    client_id = int(request.args.get("client_id", 1))

    with engine.begin() as conn:
        client = conn.execute(text("""
            SELECT id, siren, siret, raison_sociale, forme_juridique,
                   regime_fiscal, regime_tva, adresse, statut, created_at
            FROM clients_v3
            WHERE id = :client_id
        """), {"client_id": client_id}).mappings().first()

        if not client:
            return jsonify({"success": False, "error": "Client introuvable"}), 404

        pieces = conn.execute(text("""
            SELECT id, nom_fichier, type_piece, statut_ocr, statut_validation, created_at
            FROM pieces_v3
            WHERE client_id = :client_id
            ORDER BY id DESC
            LIMIT 50
        """), {"client_id": client_id}).mappings().all()

        imports = conn.execute(text("""
            SELECT id, type_import, nom_fichier, statut, nb_lignes, created_at
            FROM imports_v3
            WHERE client_id = :client_id
            ORDER BY id DESC
            LIMIT 50
        """), {"client_id": client_id}).mappings().all()

        exercices = conn.execute(text("""
            SELECT id, date_debut, date_fin, statut, date_cloture, resultat_cloture
            FROM exercices_v3
            WHERE client_id = :client_id
            ORDER BY date_debut DESC
        """), {"client_id": client_id}).mappings().all()

        immobilisations = conn.execute(text("""
            SELECT id, designation, date_acquisition, valeur_origine, duree_mois,
                   compte_immo, compte_amortissement, compte_dotation, statut
            FROM immobilisations_v3
            WHERE societe_id = :client_id
            ORDER BY id DESC
        """), {"client_id": client_id}).mappings().all()

        emprunts = conn.execute(text("""
            SELECT id, organisme, capital, taux_annuel, duree_mois, date_debut,
                   compte_emprunt, compte_interets, compte_banque, statut
            FROM emprunts_v3
            WHERE societe_id = :client_id
            ORDER BY id DESC
        """), {"client_id": client_id}).mappings().all()

        kpis = {
            "documents": len(pieces),
            "imports": len(imports),
            "exercices": len(exercices),
            "immobilisations": len(immobilisations),
            "emprunts": len(emprunts),
            "valeur_immobilisations": float(sum([i["valeur_origine"] or 0 for i in immobilisations])),
            "capital_emprunts": float(sum([e["capital"] or 0 for e in emprunts])),
        }

    return jsonify({
        "success": True,
        "client": dict(client),
        "kpis": kpis,
        "pieces": [dict(p) for p in pieces],
        "imports": [dict(i) for i in imports],
        "exercices": [dict(e) for e in exercices],
        "immobilisations": [dict(i) for i in immobilisations],
        "emprunts": [dict(e) for e in emprunts],
    })

@api_metier_refonte.get("/api/refonte/collaborateurs")
def api_collaborateurs_cabinet():
    with engine.begin() as conn:
        collaborateurs = conn.execute(text("""
            SELECT id, nom, email, role, statut, created_at
            FROM collaborateurs_cabinet_v3
            ORDER BY
                CASE role
                    WHEN 'EXPERT_COMPTABLE' THEN 1
                    WHEN 'CHEF_MISSION' THEN 2
                    WHEN 'COLLABORATEUR' THEN 3
                    ELSE 4
                END,
                id
        """)).mappings().all()

        affectations = conn.execute(text("""
            SELECT
                a.id,
                a.client_id,
                c.raison_sociale,
                a.collaborateur_id,
                col.nom AS collaborateur,
                col.role,
                a.role_dossier,
                a.statut,
                a.created_at
            FROM affectations_dossiers_v3 a
            JOIN clients_v3 c ON c.id = a.client_id
            JOIN collaborateurs_cabinet_v3 col ON col.id = a.collaborateur_id
            ORDER BY a.id
        """)).mappings().all()

        notifications = conn.execute(text("""
            SELECT
                n.id,
                n.collaborateur_id,
                col.nom AS collaborateur,
                n.client_id,
                c.raison_sociale,
                n.titre,
                n.message,
                n.niveau,
                n.statut,
                n.created_at
            FROM notifications_cabinet_v3 n
            LEFT JOIN collaborateurs_cabinet_v3 col ON col.id = n.collaborateur_id
            LEFT JOIN clients_v3 c ON c.id = n.client_id
            ORDER BY n.created_at DESC, n.id DESC
            LIMIT 50
        """)).mappings().all()

    return jsonify({
        "success": True,
        "kpis": {
            "collaborateurs": len(collaborateurs),
            "affectations": len(affectations),
            "notifications": len(notifications),
            "notifications_non_lues": len([n for n in notifications if n["statut"] == "NON_LUE"]),
        },
        "collaborateurs": [dict(c) for c in collaborateurs],
        "affectations": [dict(a) for a in affectations],
        "notifications": [dict(n) for n in notifications],
    })


@api_metier_refonte.post("/api/refonte/notification/lire")
def api_notification_lire():
    data = request.get_json(silent=True) or {}
    notification_id = data.get("notification_id")

    if not notification_id:
        return jsonify({"success": False, "error": "notification_id obligatoire"}), 400

    with engine.begin() as conn:
        row = conn.execute(text("""
            UPDATE notifications_cabinet_v3
            SET statut = 'LUE'
            WHERE id = :id
            RETURNING id, statut
        """), {"id": notification_id}).mappings().first()

    if not row:
        return jsonify({"success": False, "error": "Notification introuvable"}), 404

    return jsonify({"success": True, "notification": dict(row)})

@api_metier_refonte.get("/api/refonte/planning-cabinet")
def api_planning_cabinet():
    with engine.begin() as conn:
        taches = conn.execute(text("""
            SELECT
                t.id,
                t.client_id,
                c.raison_sociale,
                t.titre,
                t.priorite,
                t.statut,
                t.echeance,
                t.created_at,
                col.id AS collaborateur_id,
                col.nom AS collaborateur
            FROM taches_cabinet_v3 t
            LEFT JOIN clients_v3 c ON c.id = t.client_id
            LEFT JOIN affectations_dossiers_v3 a
                ON a.client_id = t.client_id
               AND a.statut = 'ACTIF'
            LEFT JOIN collaborateurs_cabinet_v3 col
                ON col.id = a.collaborateur_id
            WHERE t.statut <> 'TERMINE'
            ORDER BY
                CASE WHEN t.echeance IS NULL THEN 1 ELSE 0 END,
                t.echeance,
                CASE t.priorite
                    WHEN 'CRITIQUE' THEN 1
                    WHEN 'HAUTE' THEN 2
                    WHEN 'WARNING' THEN 3
                    WHEN 'NORMALE' THEN 4
                    ELSE 5
                END,
                t.id
        """)).mappings().all()

        charge = conn.execute(text("""
            SELECT
                col.id,
                col.nom,
                col.role,
                COUNT(DISTINCT a.client_id) AS dossiers_affectes,
                COUNT(DISTINCT t.id) FILTER (WHERE t.statut <> 'TERMINE') AS taches_ouvertes,
                COUNT(DISTINCT t.id) FILTER (
                    WHERE t.statut <> 'TERMINE'
                      AND t.priorite IN ('HAUTE','CRITIQUE')
                ) AS taches_urgentes
            FROM collaborateurs_cabinet_v3 col
            LEFT JOIN affectations_dossiers_v3 a
                ON a.collaborateur_id = col.id
               AND a.statut = 'ACTIF'
            LEFT JOIN taches_cabinet_v3 t
                ON t.client_id = a.client_id
            WHERE col.statut = 'ACTIF'
            GROUP BY col.id
            ORDER BY taches_urgentes DESC, taches_ouvertes DESC, col.id
        """)).mappings().all()

        notifications = conn.execute(text("""
            SELECT
                n.id,
                n.titre,
                n.message,
                n.niveau,
                n.statut,
                n.created_at,
                col.nom AS collaborateur,
                c.raison_sociale
            FROM notifications_cabinet_v3 n
            LEFT JOIN collaborateurs_cabinet_v3 col ON col.id = n.collaborateur_id
            LEFT JOIN clients_v3 c ON c.id = n.client_id
            WHERE n.statut = 'NON_LUE'
            ORDER BY n.created_at DESC, n.id DESC
            LIMIT 20
        """)).mappings().all()

    sans_echeance = len([t for t in taches if t["echeance"] is None])
    urgentes = len([t for t in taches if t["priorite"] in ("HAUTE", "CRITIQUE")])

    return jsonify({
        "success": True,
        "kpis": {
            "taches_ouvertes": len(taches),
            "taches_urgentes": urgentes,
            "sans_echeance": sans_echeance,
            "notifications_non_lues": len(notifications),
            "collaborateurs_actifs": len(charge),
        },
        "taches": [dict(t) for t in taches],
        "charge": [dict(c) for c in charge],
        "notifications": [dict(n) for n in notifications],
    })

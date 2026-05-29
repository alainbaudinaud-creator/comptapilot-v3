from flask import Blueprint, jsonify, request
from sqlalchemy import text

from database import engine
from app_refonte.services.immobilisations_service import amortissement_lineaire
from app_refonte.services.emprunts_service import tableau_amortissement_emprunt
from app_refonte.services.tva_service import calcul_tva
from app_refonte.services.fec_service import controle_colonnes_fec, REQUIRED_FEC_COLUMNS

api_metier_demo = Blueprint("api_metier_demo", __name__)


@api_metier_demo.get("/api/refonte/health")
def health():
    return jsonify({
        "success": True,
        "module": "ComptaPilot V3 Refonte",
        "status": "OK"
    })


@api_metier_demo.post("/api/refonte/immobilisation/amortissement")
def api_amortissement():
    data = request.get_json(silent=True) or {}
    lignes = amortissement_lineaire(
        data.get("valeur_origine", 0),
        data.get("duree_mois", 0)
    )
    return jsonify({"success": True, "lignes": lignes})


@api_metier_demo.post("/api/refonte/emprunt/tableau")
def api_emprunt():
    data = request.get_json(silent=True) or {}
    lignes = tableau_amortissement_emprunt(
        data.get("montant", 0),
        data.get("taux_annuel", 0),
        data.get("duree_mois", 0)
    )
    return jsonify({"success": True, "lignes": lignes})


@api_metier_demo.post("/api/refonte/tva/calcul")
def api_tva():
    data = request.get_json(silent=True) or {}
    resultat = calcul_tva(
        data.get("tva_collectee", 0),
        data.get("tva_deductible", 0)
    )
    return jsonify({"success": True, "resultat": resultat})


@api_metier_demo.get("/api/refonte/fec/controle-demo")
def api_fec_demo():
    resultat = controle_colonnes_fec(REQUIRED_FEC_COLUMNS)
    return jsonify({"success": True, "resultat": resultat})


@api_metier_demo.get("/api/refonte/pcg")
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

@api_metier_demo.post("/api/refonte/emprunt/premium")
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

@api_metier_demo.post("/api/refonte/immobilisation/premium")
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


@api_metier_demo.post("/api/refonte/immobilisation/creer")
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


@api_metier_demo.get("/api/refonte/immobilisations")
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



@api_metier_demo.post("/api/refonte/immobilisation/comptabiliser")
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



@api_metier_demo.post("/api/refonte/emprunt/creer")
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


@api_metier_demo.post("/api/refonte/emprunt/comptabiliser")
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



@api_metier_demo.get("/api/refonte/balance")
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



@api_metier_demo.get("/api/refonte/grand-livre")
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



@api_metier_demo.get("/api/refonte/journal")
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



@api_metier_demo.get("/api/refonte/fec/export")
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



@api_metier_demo.get("/api/refonte/compte-resultat")
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



@api_metier_demo.get("/api/refonte/bilan")
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

        if solde >= 0:
            actif.append(item)
            total_actif += solde
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



@api_metier_demo.post("/api/refonte/ocr/analyser-comptabiliser")
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



@api_metier_demo.post("/api/refonte/ocr/upload-pdf")
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



@api_metier_demo.post("/api/refonte/ocr/upload-pdf-a-valider")
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


@api_metier_demo.get("/api/refonte/ocr/pieces-a-valider")
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


@api_metier_demo.post("/api/refonte/ocr/valider-piece")
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


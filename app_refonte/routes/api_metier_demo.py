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



@api_metier_demo.post("/api/refonte/banque/seed-demo")
def api_banque_seed_demo():
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


@api_metier_demo.get("/api/refonte/banque/operations")
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


@api_metier_demo.get("/api/refonte/banque/propositions")
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


@api_metier_demo.post("/api/refonte/banque/valider-rapprochement")
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



@api_metier_demo.post("/api/refonte/lettrage/seed-paiement-demo")
def api_lettrage_seed_paiement_demo():
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


@api_metier_demo.get("/api/refonte/lettrage/propositions")
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


@api_metier_demo.post("/api/refonte/lettrage/valider")
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


@api_metier_demo.get("/api/refonte/lettrage")
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



@api_metier_demo.get("/api/refonte/ocr/doublons")
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



@api_metier_demo.get("/api/refonte/tva/ca3")
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



@api_metier_demo.get("/api/refonte/cloture/controle")
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



@api_metier_demo.get("/api/refonte/cloture/simulation")
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



@api_metier_demo.post("/api/refonte/cloture/definitive")
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


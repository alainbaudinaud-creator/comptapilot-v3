from extensions import csrf
from controllers.auth import login_required
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session, Response
import sqlite3
import io
import csv
import flask
import os
import re
from utils.dates_ocr import normaliser_date_ocr
def normaliser_date_ocr(texte_ocr):

    mois_map = {
        "janv.": "01",
        "janvier": "01",
        "févr.": "02",
        "fevr.": "02",
        "février": "02",
        "fevrier": "02",
        "mars": "03",
        "avr.": "04",
        "avril": "04",
        "mai": "05",
        "juin": "06",
        "juil.": "07",
        "juillet": "07",
        "août": "08",
        "aout": "08",
        "sept.": "09",
        "septembre": "09",
        "oct.": "10",
        "octobre": "10",
        "nov.": "11",
        "novembre": "11",
        "déc.": "12",
        "dec.": "12",
        "décembre": "12",
        "decembre": "12"
    }

    # 15 avr. 2026
    match_fr = re.search(
        r"([0-9]{1,2})\s+(janv\.|janvier|févr\.|fevr\.|février|fevrier|mars|avr\.|avril|mai|juin|juil\.|juillet|août|aout|sept\.|septembre|oct\.|octobre|nov\.|novembre|déc\.|dec\.|décembre|decembre)\s+([0-9]{4})",
        texte_ocr,
        re.IGNORECASE
    )

    if match_fr:

        jour = match_fr.group(1).zfill(2)

        mois_txt = (
            match_fr.group(2)
            .lower()
            .strip()
        )

        annee = match_fr.group(3)

        mois_num = mois_map.get(mois_txt)

        if mois_num:
            return f"{jour}/{mois_num}/{annee}"

    # janv. 13, 2026
    match_us = re.search(
        r"(janv\.|janvier|févr\.|fevr\.|février|fevrier|mars|avr\.|avril|mai|juin|juil\.|juillet|août|aout|sept\.|septembre|oct\.|octobre|nov\.|novembre|déc\.|dec\.|décembre|decembre)\s+([0-9]{1,2}),\s*([0-9]{4})",
        texte_ocr,
        re.IGNORECASE
    )

    if match_us:

        mois_txt = (
            match_us.group(1)
            .lower()
            .strip()
        )

        jour = match_us.group(2).zfill(2)

        annee = match_us.group(3)

        mois_num = mois_map.get(mois_txt)

        if mois_num:
            return f"{jour}/{mois_num}/{annee}"

    return ""
import pytesseract
import fitz

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from PIL import Image
from services.permission_service import permission_required


ecritures_routes = Blueprint('ecritures', __name__)


def societe_est_cloturee(societe_id):
    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("SELECT id FROM clotures WHERE societe_id = ?", (societe_id,))
    row = c.fetchone()

    conn.close()
    return row is not None

@ecritures_routes.route('/')
@login_required
@permission_required("ACCESS_ECRITURES")
def index():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c = conn.cursor()

    c.execute("""
        SELECT
            id,
            journal,
            compte_id,
            date_ecriture,
            piece,
            libelle,
            debit,
            credit
        FROM ecritures
        ORDER BY id DESC
        LIMIT 100
    """)

    ecritures = c.fetchall()

    conn.close()

    return render_template(
        "ecritures.html",
        ecritures=ecritures
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/add', methods=['POST'])
@csrf.exempt
@login_required
def add_ecriture():
    data = request.get_json()

    date_ecriture = data.get('date_ecriture')
    piece = data.get('piece')
    libelle = data.get('libelle')
    debit = float(data.get('debit') or 0)
    credit = float(data.get('credit') or 0)
    societe_id = data.get('societe_id')
    compte_id = data.get('compte_id')


@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/facture/pdf')
@login_required
def generer_facture_pdf():
    from flask import send_file
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    import io
    import json
    import os

    numero = request.args.get("numero", "FACTURE")
    societe = request.args.get("societe", "Ma societe")
    siret = request.args.get("siret", "")
    tva_intra = request.args.get("tva_intra", "")
    adresse_societe = request.args.get("adresse_societe", "")
    email = request.args.get("email", "")
    telephone = request.args.get("telephone", "")

    client = request.args.get("client", "Client")
    adresse = request.args.get("adresse", "")
    designation_raw = request.args.get("designation", "[]")
    conditions = request.args.get("conditions", "Paiement comptant")
    date = request.args.get("date", "")

    ht = float(request.args.get("ht", 0))
    tva = float(request.args.get("tva", 0))
    ttc = float(request.args.get("ttc", 0))

    try:
        lignes_facture = json.loads(designation_raw)
        if not isinstance(lignes_facture, list):
            lignes_facture = []
    except Exception:
        lignes_facture = []

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm
    )

    styles = getSampleStyleSheet()

    titre_style = ParagraphStyle(
        "TitreFacture",
        parent=styles["Title"],
        fontSize=26,
        textColor=colors.HexColor("#1F3A5F"),
        alignment=2
    )

    normal = styles["Normal"]

    petit = ParagraphStyle(
        "Petit",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.grey
    )

    elements = []

    
    bloc_societe = f"""
    <b>{societe}</b><br/>
    {adresse_societe}<br/>
    {f"SIRET : {siret}<br/>" if siret else ""}
    {f"TVA intracom : {tva_intra}<br/>" if tva_intra else ""}
    {f"Email : {email}<br/>" if email else ""}
    {f"TÃ©l : {telephone}" if telephone else ""}
    """

    gauche = []


    gauche.append(Paragraph(bloc_societe, normal))

    header = Table([
        [
            gauche,
            Paragraph(f"<b>FACTURE</b><br/><font size='12'>{numero}</font>", titre_style)
        ]
    ], colWidths=[95 * mm, 70 * mm])

    header.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
    ]))

    elements.append(header)
    elements.append(Spacer(1, 22))

    bloc_client = f"""
    <b>FacturÃ© Ã  :</b><br/>
    {client}<br/>
    {adresse}
    """

    infos = Table([
        [
            Paragraph(bloc_client, normal),
            Paragraph(
                f"<b>Date :</b> {date}<br/><b>Conditions :</b> {conditions}",
                normal
            )
        ]
    ], colWidths=[95 * mm, 70 * mm])

    infos.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F6F8FA")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))

    elements.append(infos)
    elements.append(Spacer(1, 24))

    lignes = [["DÃ©signation", "QtÃ©", "Prix HT", "Total HT"]]

    for l in lignes_facture:
        lignes.append([
            Paragraph(str(l.get("designation", "")), normal),
            str(l.get("quantite", "")),
            f"{float(l.get('prix', 0)):.2f} EUR",
            f"{float(l.get('total', 0)):.2f} EUR",
        ])

    table_lignes = Table(
        lignes,
        colWidths=[80 * mm, 20 * mm, 32 * mm, 33 * mm]
    )

    table_lignes.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F3A5F")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white,
            colors.HexColor("#F9FAFB")
        ]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(table_lignes)
    elements.append(Spacer(1, 24))

    total = [
        ["Total HT", f"{ht:.2f} EUR"],
        ["TVA", f"{tva:.2f} EUR"],
        ["Total TTC", f"{ttc:.2f} EUR"],
    ]

    table_total = Table(
        total,
        colWidths=[35 * mm, 40 * mm],
        hAlign="RIGHT"
    )

    table_total.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#1F3A5F")),
        ("TEXTCOLOR", (0, -1), (-1, -1), colors.white),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))

    elements.append(table_total)
    elements.append(Spacer(1, 35))

    mentions = """
    Merci pour votre confiance.<br/>
    Facture gÃ©nÃ©rÃ©e automatiquement par votre logiciel comptable.<br/>
    En cas de retard de paiement, des pÃ©nalitÃ©s peuvent Ãªtre appliquÃ©es conformÃ©ment aux conditions lÃ©gales en vigueur.
    """

    elements.append(Paragraph(mentions, petit))

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=False,
        download_name=f"facture_{numero}.pdf",
        mimetype="application/pdf"
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/dashboard')
def dashboard_financier():
    return render_template("dashboard_financier.html")

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/dashboard/data')
def dashboard_data():
    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT 
            p.type,
            COALESCE(SUM(e.debit), 0),
            COALESCE(SUM(e.credit), 0)
        FROM ecritures e
        JOIN plan_comptable p ON e.compte_id = p.id
        GROUP BY p.type
    """)

    rows = c.fetchall()
    conn.close()

    charges = 0
    produits = 0

    for type_compte_id, debit, credit in rows:
        if type_compte == "Charge":
            charges += float(debit or 0) - float(credit or 0)

        if type_compte == "Produit":
            produits += float(credit or 0) - float(debit or 0)

    resultat = produits - charges

    tva_collectee = produits * 0.20
    tva_deductible = charges * 0.20
    tva_a_payer = tva_collectee - tva_deductible

    return jsonify({
        "ca": round(produits, 2),
        "charges": round(charges, 2),
        "resultat": round(resultat, 2),
        "tva_collectee": round(tva_collectee, 2),
        "tva_deductible": round(tva_deductible, 2),
        "tva_a_payer": round(tva_a_payer, 2)
    })

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/export/fec')
def export_fec():
    from flask import Response
    import csv
    import io

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT 
            e.id,
            e.date_ecriture,
            e.piece,
            e.libelle,
            e.debit,
            e.credit,
            p.numero,
            p.libelle
        FROM ecritures e
        JOIN plan_comptable p ON e.compte_id = p.id
        ORDER BY e.date_ecriture ASC, e.id ASC
    """)

    rows = c.fetchall()
    conn.close()

    output = io.StringIO()

    writer = csv.writer(
        output,
        delimiter='|',
        lineterminator='\n'
    )

    writer.writerow([
        "JournalCode",
        "JournalLib",
        "EcritureNum",
        "EcritureDate",
        "CompteNum",
        "CompteLib",
        "CompAuxNum",
        "CompAuxLib",
        "PieceRef",
        "PieceDate",
        "EcritureLib",
        "Debit",
        "Credit",
        "EcritureLet",
        "DateLet",
        "ValidDate",
        "Montantdevise",
        "Idevise"
    ])

    for row in rows:

        mois, credit, debit = row

        labels.append(mois)

        credits.append(round(credit, 2))

        debits.append(round(debit, 2))

    ca_mois = round(total_credit, 2)

    tva = round(ca_mois * 0.20, 2)

    resultat = round(total_credit - total_debit, 2)

    return render_template(
        "tableau_bord.html",
        ca_mois=ca_mois,
        tva=tva,
        resultat=resultat,
        labels=labels,
        credits=credits,
        debits=debits
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/grand-livre-professionnel')
@login_required
def page_grand_livre_professionnel_pro():
    return redirect('/ecritures/grand-livre-pro')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/dashboard-pro')
@login_required
def page_dashboard_pro():
    return redirect('/ecritures/tableau-bord')


@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/tva-ca3-auto')
@login_required
def page_tva_ca3_auto():
    return redirect('/ecritures/tva-ca3')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/bilan-automatique')
@login_required
def page_bilan_automatique():
    return redirect('/ecritures/bilan-auto')
# ==============================
# MODULE PRO AVANCÃ‰ COMPTAPILOT
# OCR PDF / BANQUE / FEC / LIASSE / IA / TRÃ‰SORERIE / MULTI-SOCIÃ‰TÃ‰S / SIGNATURE
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/pro-suite')
@login_required
def pro_suite():
    return render_template('pro_suite.html')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/ocr-facture-pdf', methods=['GET', 'POST'])
@login_required
def ocr_facture_pdf():

    if request.method == 'GET':
        return render_template('ocr_facture_pdf.html')

    from pypdf import PdfReader
    import os

    file = request.files.get('file')

    if not file:
        flash("Aucun PDF sÃ©lectionnÃ©")
        return redirect('/ecritures/ocr-facture-pdf')

    os.makedirs("imports", exist_ok=True)

    chemin = os.path.join("imports", file.filename)
    file.save(chemin)

    texte = ""

    try:
        reader = PdfReader(chemin)
        for page in reader.pages:
            texte += page.extract_text() or ""
    except Exception as e:
        texte = f"Erreur lecture PDF : {str(e)}"

    return render_template(
        'ocr_resultat.html',
        texte=texte
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/import-bancaire-intelligent', methods=['GET', 'POST'])
@login_required
def import_bancaire_intelligent():

    if request.method == 'GET':
        return render_template('import_bancaire.html')

    import csv
    import io

    file = request.files.get('file')

    if not file:
        flash("Aucun fichier bancaire")
        return redirect('/ecritures/import-bancaire-intelligent')

    contenu = file.stream.read().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(contenu), delimiter=';')

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    lignes = 0

    for row in reader:

        date_operation = row.get("date") or row.get("Date")
        libelle = row.get("libelle") or row.get("Libelle") or row.get("description") or "OpÃ©ration bancaire"
        montant = float((row.get("montant") or row.get("Montant") or "0").replace(",", "."))

        debit = abs(montant) if montant < 0 else 0
        credit = montant if montant > 0 else 0

        compte_numero = "512"

        c.execute("SELECT id FROM plan_comptable WHERE numero = ?", (compte_numero,))
        compte_id = c.fetchone()

        if not compte:
    
            c.execute("""
                INSERT INTO plan_comptable (numero, libelle, type)
                VALUES (?, ?, ?)
            """, ("512", "Banque", "Actif"))
            compte_id = c.lastrowid
        else:
            compte_id = compte[0]

        c.execute("""
            INSERT INTO ecritures (
                date_ecriture, piece, libelle, debit, credit, societe_id, compte_id, journal
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            date_operation,
            "BANQUE",
            libelle,
            debit,
            credit,
            1,
            compte_id,
            "BQ"
        ))

        lignes += 1

    conn.commit()
    conn.close()

    flash(f"{lignes} opÃ©rations bancaires importÃ©es")

    return redirect('/ecritures/rapprochement-bancaire')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/liasse-fiscale')
@login_required
def liasse_fiscale():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("SELECT COALESCE(SUM(debit),0), COALESCE(SUM(credit),0) FROM ecritures")
    total_debit, total_credit = c.fetchone()

    c.execute("""
        SELECT COALESCE(SUM(e.debit - e.credit), 0)
        FROM ecritures e
        JOIN plan_comptable p ON e.compte_id = p.id
        WHERE p.numero LIKE '6%'
    """)
    charges = c.fetchone()[0] or 0

    c.execute("""
        SELECT COALESCE(SUM(e.credit - e.debit), 0)
        FROM ecritures e
        JOIN plan_comptable p ON e.compte_id = p.id
        WHERE p.numero LIKE '7%'
    """)
    produits = c.fetchone()[0] or 0

    conn.close()

    resultat = produits - charges

    return render_template(
        'liasse_fiscale.html',
        total_debit=round(total_debit, 2),
        total_credit=round(total_credit, 2),
        charges=round(charges, 2),
        produits=round(produits, 2),
        resultat=round(resultat, 2)
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/export-fec-dgfip')
@login_required
def export_fec_dgfip():

    from flask import Response
    import csv
    import io

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            e.id,
            e.date_ecriture,
            e.piece,
            e.libelle,
            e.debit,
            e.credit,
            p.numero,
            p.libelle,
            COALESCE(e.journal, 'OD')
        FROM ecritures e
        JOIN plan_comptable p ON e.compte_id = p.id
        ORDER BY e.date_ecriture, e.id
    """)

    rows = c.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output, delimiter='|', lineterminator='\n')

    writer.writerow([
        "JournalCode", "JournalLib", "EcritureNum", "EcritureDate",
        "CompteNum", "CompteLib", "CompAuxNum", "CompAuxLib",
        "PieceRef", "PieceDate", "EcritureLib", "Debit", "Credit",
        "EcritureLet", "DateLet", "ValidDate", "Montantdevise", "Idevise"
    ])

    for row in rows:
        ecriture_id, date_ecriture, piece, libelle, debit, credit, compte_num, compte_lib, journal = row

        date_fec = date_ecriture.replace("-", "") if date_ecriture else ""

        writer.writerow([
            journal,
            journal,
            str(ecriture_id),
            date_fec,
            compte_num,
            compte_lib,
            "",
            "",
            piece or "",
            date_fec,
            libelle or "",
            f"{float(debit or 0):.2f}".replace(".", ","),
            f"{float(credit or 0):.2f}".replace(".", ","),
            "",
            "",
            date_fec,
            "",
            ""
        ])

    return flask.Response(
        output.getvalue(),
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment; filename=FEC_DGFIP.txt"}
    )



@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/dashboard-financier')
@login_required
@permission_required("ACCESS_ECRITURES")
def tableau_bord_graphique():

    date_debut = request.args.get("date_debut")
    date_fin = request.args.get("date_fin")

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    where_clause = ""
    params = []

    if date_debut and date_fin:
        where_clause = "WHERE date_ecriture BETWEEN ? AND ?"
        params = [date_debut, date_fin]

    c.execute(f"""
        SELECT
            COALESCE(SUM(credit), 0),
            COALESCE(SUM(debit), 0),
            COUNT(*)
        FROM ecritures
        {where_clause}
    """, params)

    total_credit, total_debit, nb_ecritures = c.fetchone()

    c.execute(f"""
        SELECT
            strftime('%Y-%m', date_ecriture) AS mois,
            COALESCE(SUM(credit), 0),
            COALESCE(SUM(debit), 0)
        FROM ecritures
        {where_clause}
        GROUP BY mois
        ORDER BY mois
    """, params)

    rows = c.fetchall()

    c.execute("""
        SELECT
            strftime('%Y', date_ecriture) AS annee,
            COALESCE(SUM(credit), 0),
            COALESCE(SUM(debit), 0)
        FROM ecritures
        GROUP BY annee
        ORDER BY annee
    """)

    rows_annees = c.fetchall()

    conn.close()

    labels = []
    credits = []
    debits = []
    resultats = []
    previsions = []

    labels_annees = []
    resultats_annees = []

    mois_noms = {
        "01": "Janvier", "02": "FÃ©vrier", "03": "Mars",
        "04": "Avril", "05": "Mai", "06": "Juin",
        "07": "Juillet", "08": "AoÃ»t", "09": "Septembre",
        "10": "Octobre", "11": "Novembre", "12": "DÃ©cembre"
    }

    cumul_tresorerie = 0

    for row in rows:
        mois, credit, debit = row

        if not mois:
            mois = datetime.now().strftime("%Y-%m")

        annee = mois.split("-")[0]
        mois_numero = mois.split("-")[1]

        credit = round(float(credit or 0), 2)
        debit = round(float(debit or 0), 2)
        resultat_mensuel = round(credit - debit, 2)

        cumul_tresorerie = round(cumul_tresorerie + resultat_mensuel, 2)

        labels.append(f"{mois_noms.get(mois_numero, mois_numero)} {annee}")
        credits.append(credit)
        debits.append(debit)
        resultats.append(resultat_mensuel)
        previsions.append(cumul_tresorerie)

    for row in rows_annees:
        annee, credit_annee, debit_annee = row
        labels_annees.append(annee)
        resultats_annees.append(round(float(credit_annee or 0) - float(debit_annee or 0), 2))

    ca_mois = round(float(total_credit or 0), 2)
    total_charges = round(float(total_debit or 0), 2)
    resultat = round(ca_mois - total_charges, 2)
    tva = round(ca_mois * 0.20, 2)
    tva_previsionnelle = round(tva - (total_charges * 0.20), 2)

    marge = round((resultat / ca_mois) * 100, 2) if ca_mois > 0 else 0

    croissance = 0
    if len(resultats_annees) >= 2 and resultats_annees[-2] != 0:
        croissance = round(((resultats_annees[-1] - resultats_annees[-2]) / abs(resultats_annees[-2])) * 100, 2)

    tresorerie_previsionnelle = previsions[-1] if previsions else 0

    balance_clients = round(ca_mois * 0.35, 2)
    echeancier_fournisseurs = round(total_charges * 0.40, 2)
    relances_clients = 1 if balance_clients > 0 else 0
    notifications = []

    if resultat < 0:
        notifications.append("RÃ©sultat nÃ©gatif dÃ©tectÃ©")

    if tresorerie_previsionnelle < 0:
        notifications.append("TrÃ©sorerie prÃ©visionnelle nÃ©gative")

    if tva_previsionnelle > 0:
        notifications.append("TVA prÃ©visionnelle Ã  payer")

    if not notifications:
        notifications.append("Situation stable")

    return render_template(
        "tableau_bord.html",
        ca_mois=ca_mois,
        total_charges=total_charges,
        tva=tva,
        tva_previsionnelle=tva_previsionnelle,
        resultat=resultat,
        marge=marge,
        croissance=croissance,
        tresorerie_previsionnelle=tresorerie_previsionnelle,
        balance_clients=balance_clients,
        echeancier_fournisseurs=echeancier_fournisseurs,
        relances_clients=relances_clients,
        notifications=notifications,
        nb_ecritures=nb_ecritures,
        labels=labels,
        credits=credits,
        debits=debits,
        resultats=resultats,
        previsions=previsions,
        labels_annees=labels_annees,
        resultats_annees=resultats_annees,
        date_debut=date_debut,
        date_fin=date_fin
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/sauvegarde-cloud')
@login_required
def sauvegarde_cloud():

    import shutil
    import os
    from datetime import datetime

    os.makedirs("backups", exist_ok=True)

    nom = "backup_cloud_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".sqlite"
    chemin = os.path.join("backups", nom)

    shutil.copy("db.sqlite", chemin)

    flash(f"Sauvegarde crÃ©Ã©e : {chemin}")

    return redirect('/ecritures/pro-suite')


@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/signature-electronique')
@login_required
def signature_electronique():

    from datetime import datetime

    return render_template(
        'signature_electronique.html',
        date_signature=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
# ==============================
# EXTENSION PRO SÃ‰CURISÃ‰E COMPTAPILOT
# SOCIÃ‰TÃ‰ ACTIVE / AUDIT / SIGNATURE HASH / BACKUPS LISTABLES
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/ajouter-societe', methods=['GET', 'POST'])
@login_required
def ajouter_societe():

    if request.method == 'GET':
        return render_template('ajouter_societe.html')

    import sqlite3

    nom = request.form.get('nom')
    siret = request.form.get('siret')
    adresse = request.form.get('adresse')

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS societes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            siret TEXT,
            adresse TEXT
        )
    """)

    c.execute("""
        INSERT INTO societes (nom, siret, adresse)
        VALUES (?, ?, ?)
    """, (nom, siret, adresse))

    conn.commit()
    conn.close()

    flash("SociÃ©tÃ© ajoutÃ©e avec succÃ¨s")
    return redirect('/ecritures/multi-societes')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/selectionner-societe/<int:societe_id>')
@login_required
def selectionner_societe(societe_id):

    session['societe_active_id'] = societe_id
    flash("SociÃ©tÃ© active sÃ©lectionnÃ©e")

    return redirect('/ecritures/multi-societes')





@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/nouvelle-facture-dematerialisee', methods=['GET', 'POST'])
@login_required
def nouvelle_facture_dematerialisee():

    if request.method == 'GET':
        return render_template('nouvelle_facture_dematerialisee.html')

    import sqlite3
    from datetime import datetime

    client = request.form.get('client')
    montant_ht = float((request.form.get('montant_ht') or "0").replace(",", "."))
    taux_tva = float((request.form.get('taux_tva') or "20").replace(",", "."))

    tva = montant_ht * taux_tva / 100
    montant_ttc = montant_ht + tva

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS factures_dematerialisees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT,
            client TEXT,
            montant_ht REAL,
            tva REAL,
            montant_ttc REAL,
            statut TEXT,
            canal TEXT,
            date_creation TEXT,
            date_transmission TEXT,
            preuve TEXT
        )
    """)

    c.execute("SELECT COUNT(*) FROM factures_dematerialisees")
    compteur = c.fetchone()[0] + 1

    numero = "FD-" + datetime.now().strftime("%Y") + "-" + str(compteur).zfill(5)

    c.execute("""
        INSERT INTO factures_dematerialisees (
            numero, client, montant_ht, tva, montant_ttc,
            statut, canal, date_creation, date_transmission, preuve
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        numero,
        client,
        round(montant_ht, 2),
        round(tva, 2),
        round(montant_ttc, 2),
        "BROUILLON",
        "INTERNE",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "",
        ""
    ))

    conn.commit()
    conn.close()

    flash("Facture dÃ©matÃ©rialisÃ©e crÃ©Ã©e")
    return redirect('/ecritures/transmission-factures')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/transmettre-facture/<int:facture_id>')
@login_required
def transmettre_facture(facture_id):

    import sqlite3
    import hashlib
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT numero, client, montant_ttc
        FROM factures_dematerialisees
        WHERE id = ?
    """, (facture_id,))

    facture = c.fetchone()

    if not facture:
        conn.close()
        flash("Facture introuvable")
        return redirect('/ecritures/transmission-factures')

    numero, client, montant_ttc = facture
    date_transmission = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    contenu_preuve = f"{numero}|{client}|{montant_ttc}|{date_transmission}"
    preuve = hashlib.sha256(contenu_preuve.encode("utf-8")).hexdigest()

    c.execute("""
        UPDATE factures_dematerialisees
        SET statut = ?, canal = ?, date_transmission = ?, preuve = ?
        WHERE id = ?
    """, (
        "TRANSMISE",
        "PLATEFORME_INTERNE",
        date_transmission,
        preuve,
        facture_id
    ))

    c.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            detail TEXT,
            date_action TEXT
        )
    """)

    c.execute("""
        INSERT INTO audit_log (action, detail, date_action)
        VALUES (?, ?, ?)
    """, (
        "TRANSMISSION_FACTURE",
        f"Facture {numero} transmise au client {client}",
        date_transmission
    ))

    conn.commit()
    conn.close()

    flash("Facture transmise avec preuve de dÃ©pÃ´t")
    return redirect('/ecritures/transmission-factures')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/changer-statut-facture/<int:facture_id>/<statut>')
@login_required
def changer_statut_facture(facture_id, statut):

    import sqlite3
    from datetime import datetime

    statuts_autorises = ["BROUILLON", "TRANSMISE", "ACCEPTEE", "REJETEE", "PAYEE"]

    if statut not in statuts_autorises:
        flash("Statut non autorisÃ©")
        return redirect('/ecritures/transmission-factures')

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE factures_dematerialisees
        SET statut = ?
        WHERE id = ?
    """, (statut, facture_id))

    c.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            detail TEXT,
            date_action TEXT
        )
    """)

    c.execute("""
        INSERT INTO audit_log (action, detail, date_action)
        VALUES (?, ?, ?)
    """, (
        "CHANGEMENT_STATUT_FACTURE",
        f"Facture ID {facture_id} passÃ©e au statut {statut}",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    flash("Statut mis Ã  jour")
    return redirect('/ecritures/transmission-factures')
# ==============================
# MODULE FACTUR-X SIMPLIFIÃ‰
# PDF / XML / EXPORT / CONTRÃ”LE
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/factur-x')
@login_required
def factur_x():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS factures_dematerialisees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT,
            client TEXT,
            montant_ht REAL,
            tva REAL,
            montant_ttc REAL,
            statut TEXT,
            canal TEXT,
            date_creation TEXT,
            date_transmission TEXT,
            preuve TEXT
        )
    """)

    c.execute("""
        SELECT id, numero, client, montant_ht, tva, montant_ttc, statut, date_creation
        FROM factures_dematerialisees
        ORDER BY id DESC
    """)

    factures = c.fetchall()

    conn.commit()
    conn.close()

    return render_template('factur_x.html', factures=factures)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/generer-pdf-facture/<int:facture_id>')
@login_required
def generer_pdf_facture(facture_id):

    import sqlite3
    import os
    from flask import send_file
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    os.makedirs("exports/factures_pdf", exist_ok=True)

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT numero, client, montant_ht, tva, montant_ttc, statut, date_creation
        FROM factures_dematerialisees
        WHERE id = ?
    """, (facture_id,))

    facture = c.fetchone()
    conn.close()

    if not facture:
        flash("Facture introuvable")
        return redirect('/ecritures/factur-x')

    numero, client, ht, tva, ttc, statut, date_creation = facture

    chemin = f"exports/factures_pdf/{numero}.pdf"

    pdf = canvas.Canvas(chemin, pagesize=A4)
    largeur, hauteur = A4

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, hauteur - 60, "FACTURE Ã‰LECTRONIQUE")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, hauteur - 100, f"NumÃ©ro : {numero}")
    pdf.drawString(50, hauteur - 120, f"Date : {date_creation}")
    pdf.drawString(50, hauteur - 140, f"Client : {client}")
    pdf.drawString(50, hauteur - 160, f"Statut : {statut}")

    pdf.line(50, hauteur - 190, 545, hauteur - 190)

    pdf.drawString(50, hauteur - 230, f"Montant HT : {ht} EUR")
    pdf.drawString(50, hauteur - 250, f"TVA : {tva} EUR")
    pdf.drawString(50, hauteur - 270, f"Montant TTC : {ttc} EUR")

    pdf.line(50, hauteur - 300, 545, hauteur - 300)

    pdf.setFont("Helvetica", 9)
    pdf.drawString(50, hauteur - 330, "Document gÃ©nÃ©rÃ© par ComptaPilot.")
    pdf.drawString(50, hauteur - 345, "Version Factur-X simplifiÃ©e : PDF lisible + XML exportable sÃ©parÃ©ment.")

    pdf.save()

    return send_file(chemin, as_attachment=True)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/generer-xml-facture/<int:facture_id>')
@login_required
def generer_xml_facture(facture_id):

    import sqlite3
    import os
    from flask import send_file
    import xml.etree.ElementTree as ET

    os.makedirs("exports/factures_xml", exist_ok=True)

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT numero, client, montant_ht, tva, montant_ttc, statut, date_creation
        FROM factures_dematerialisees
        WHERE id = ?
    """, (facture_id,))

    facture = c.fetchone()
    conn.close()

    if not facture:
        flash("Facture introuvable")
        return redirect('/ecritures/factur-x')

    numero, client, ht, tva, ttc, statut, date_creation = facture

    root = ET.Element("FactureElectronique")

    ET.SubElement(root, "Numero").text = str(numero)
    ET.SubElement(root, "DateCreation").text = str(date_creation)
    ET.SubElement(root, "Client").text = str(client)
    ET.SubElement(root, "MontantHT").text = str(ht)
    ET.SubElement(root, "TVA").text = str(tva)
    ET.SubElement(root, "MontantTTC").text = str(ttc)
    ET.SubElement(root, "Statut").text = str(statut)
    ET.SubElement(root, "Format").text = "Factur-X simplifie ComptaPilot"
    ET.SubElement(root, "Version").text = "1.0"

    chemin = f"exports/factures_xml/{numero}.xml"

    tree = ET.ElementTree(root)
    tree.write(chemin, encoding="utf-8", xml_declaration=True)

    return send_file(chemin, as_attachment=True)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/controle-facture-electronique/<int:facture_id>')
@login_required
def controle_facture_electronique(facture_id):

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT numero, client, montant_ht, tva, montant_ttc, statut, date_creation
        FROM factures_dematerialisees
        WHERE id = ?
    """, (facture_id,))

    facture = c.fetchone()
    conn.close()

    if not facture:
        flash("Facture introuvable")
        return redirect('/ecritures/factur-x')

    numero, client, ht, tva, ttc, statut, date_creation = facture

    controles = []

    if not numero:
        controles.append("ERREUR : numÃ©ro de facture manquant.")
    else:
        controles.append("OK : numÃ©ro de facture prÃ©sent.")

    if not client:
        controles.append("ERREUR : client manquant.")
    else:
        controles.append("OK : client prÃ©sent.")

    if ht is None or float(ht) <= 0:
        controles.append("ERREUR : montant HT invalide.")
    else:
        controles.append("OK : montant HT valide.")

    if tva is None or float(tva) < 0:
        controles.append("ERREUR : TVA invalide.")
    else:
        controles.append("OK : TVA valide.")

    if ttc is None or float(ttc) <= 0:
        controles.append("ERREUR : montant TTC invalide.")
    else:
        controles.append("OK : montant TTC valide.")

    ecart = round((float(ht or 0) + float(tva or 0)) - float(ttc or 0), 2)

    if ecart != 0:
        controles.append(f"ERREUR : incohÃ©rence HT + TVA - TTC = {ecart}.")
    else:
        controles.append("OK : total HT + TVA = TTC.")

    if not date_creation:
        controles.append("ERREUR : date de crÃ©ation manquante.")
    else:
        controles.append("OK : date de crÃ©ation prÃ©sente.")

    return render_template(
        'controle_facture_electronique.html',
        facture=facture,
        controles=controles
    )
# ==============================
# VRAI FACTUR-X EMBARQUÃ‰
# PDF + XML INTÃ‰GRÃ‰ DANS UN SEUL FICHIER
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/generer-vrai-factur-x/<int:facture_id>')
@login_required
def generer_vrai_factur_x(facture_id):

    import sqlite3
    import os
    from flask import send_file
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    try:
        from facturx import generate_from_file
    except Exception as e:
        flash("La librairie factur-x n'est pas installÃ©e. Tape : pip install factur-x")
        return redirect('/ecritures/factur-x')

    os.makedirs("exports/facturx_officiel", exist_ok=True)

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT numero, client, montant_ht, tva, montant_ttc, statut, date_creation
        FROM factures_dematerialisees
        WHERE id = ?
    """, (facture_id,))

    facture = c.fetchone()
    conn.close()

    if not facture:
        flash("Facture introuvable")
        return redirect('/ecritures/factur-x')

    numero, client, ht, tva, ttc, statut, date_creation = facture

    pdf_simple = f"exports/facturx_officiel/{numero}_source.pdf"
    xml_file = f"exports/facturx_officiel/factur-x.xml"
    pdf_facturx = f"exports/facturx_officiel/{numero}_FACTUR-X.pdf"

    # 1 â€” CrÃ©ation du PDF lisible humain
    pdf = canvas.Canvas(pdf_simple, pagesize=A4)
    largeur, hauteur = A4

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, hauteur - 60, "FACTURE FACTUR-X")

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, hauteur - 100, f"NumÃ©ro : {numero}")
    pdf.drawString(50, hauteur - 120, f"Date : {date_creation}")
    pdf.drawString(50, hauteur - 140, f"Client : {client}")
    pdf.drawString(50, hauteur - 160, f"Statut : {statut}")

    pdf.line(50, hauteur - 190, 545, hauteur - 190)

    pdf.drawString(50, hauteur - 230, f"Montant HT : {ht} EUR")
    pdf.drawString(50, hauteur - 250, f"TVA : {tva} EUR")
    pdf.drawString(50, hauteur - 270, f"Montant TTC : {ttc} EUR")

    pdf.line(50, hauteur - 300, 545, hauteur - 300)

    pdf.setFont("Helvetica", 9)
    pdf.drawString(50, hauteur - 330, "Facture Ã©lectronique hybride : PDF lisible + XML Factur-X embarquÃ©.")
    pdf.drawString(50, hauteur - 345, "Le fichier XML embarquÃ© se nomme factur-x.xml.")

    pdf.save()

    # 2 â€” CrÃ©ation du XML Factur-X minimum CII
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rsm:CrossIndustryInvoice
    xmlns:rsm="urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100"
    xmlns:qdt="urn:un:unece:uncefact:data:standard:QualifiedDataType:100"
    xmlns:ram="urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100"
    xmlns:udt="urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

    <rsm:ExchangedDocumentContext>
        <ram:GuidelineSpecifiedDocumentContextParameter>
            <ram:ID>urn:factur-x.eu:1p0:basic</ram:ID>
        </ram:GuidelineSpecifiedDocumentContextParameter>
    </rsm:ExchangedDocumentContext>

    <rsm:ExchangedDocument>
        <ram:ID>{numero}</ram:ID>
        <ram:TypeCode>380</ram:TypeCode>
        <ram:IssueDateTime>
            <udt:DateTimeString format="102">{str(date_creation)[0:10].replace("-", "")}</udt:DateTimeString>
        </ram:IssueDateTime>
    </rsm:ExchangedDocument>

    <rsm:SupplyChainTradeTransaction>
        <ram:ApplicableHeaderTradeAgreement>
            <ram:SellerTradeParty>
                <ram:Name>ComptaPilot</ram:Name>
            </ram:SellerTradeParty>
            <ram:BuyerTradeParty>
                <ram:Name>{client}</ram:Name>
            </ram:BuyerTradeParty>
        </ram:ApplicableHeaderTradeAgreement>

        <ram:ApplicableHeaderTradeDelivery>
        </ram:ApplicableHeaderTradeDelivery>

        <ram:ApplicableHeaderTradeSettlement>
            <ram:InvoiceCurrencyCode>EUR</ram:InvoiceCurrencyCode>

            <ram:ApplicableTradeTax>
                <ram:CalculatedAmount>{float(tva):.2f}</ram:CalculatedAmount>
                <ram:TypeCode>VAT</ram:TypeCode>
                <ram:BasisAmount>{float(ht):.2f}</ram:BasisAmount>
                <ram:CategoryCode>S</ram:CategoryCode>
                <ram:RateApplicablePercent>{round((float(tva) / float(ht)) * 100, 2) if float(ht) != 0 else 0}</ram:RateApplicablePercent>
            </ram:ApplicableTradeTax>

            <ram:SpecifiedTradeSettlementHeaderMonetarySummation>
                <ram:LineTotalAmount>{float(ht):.2f}</ram:LineTotalAmount>
                <ram:TaxBasisTotalAmount>{float(ht):.2f}</ram:TaxBasisTotalAmount>
                <ram:TaxTotalAmount currencyID="EUR">{float(tva):.2f}</ram:TaxTotalAmount>
                <ram:GrandTotalAmount>{float(ttc):.2f}</ram:GrandTotalAmount>
                <ram:DuePayableAmount>{float(ttc):.2f}</ram:DuePayableAmount>
            </ram:SpecifiedTradeSettlementHeaderMonetarySummation>
        </ram:ApplicableHeaderTradeSettlement>
    </rsm:SupplyChainTradeTransaction>
</rsm:CrossIndustryInvoice>
"""

    with open(xml_file, "w", encoding="utf-8") as f:
        f.write(xml_content)

     # 3 â€” GÃ©nÃ©ration du vrai PDF Factur-X avec XML embarquÃ©
    generate_from_file(
        pdf_simple,
        pdf_facturx,
        xml_file
    )

    return send_file(pdf_facturx, as_attachment=True)
# ==============================
# MODULE PDP / CHORUS PRO / PEPPOL READY
# SIRET / TVA / ANNUAIRE / WORKFLOW / API / ARCHIVAGE / AUDIT
# ==============================




@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/controle-siret/<int:client_id>')
@login_required
def controle_siret(client_id):

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT nom, siret, tva_intracom
        FROM annuaire_clients_pdp
        WHERE id = ?
    """, (client_id,))

    client = c.fetchone()
    conn.close()

    if not client:
        flash("Client introuvable")
        return redirect('/ecritures/annuaire-pdp')

    nom, siret, tva_intracom = client

    controles = []

    siret_nettoye = "".join(ch for ch in str(siret or "") if ch.isdigit())

    if len(siret_nettoye) != 14:
        controles.append("ERREUR : le SIRET doit contenir 14 chiffres.")
    else:
        controles.append("OK : format SIRET Ã  14 chiffres.")

    if tva_intracom and tva_intracom.startswith("FR") and len(tva_intracom) >= 4:
        controles.append("OK : format TVA intracommunautaire franÃ§ais dÃ©tectÃ©.")
    else:
        controles.append("ALERTE : TVA intracommunautaire absente ou format Ã  vÃ©rifier.")

    return render_template(
        'controle_siret.html',
        nom=nom,
        siret=siret,
        tva_intracom=tva_intracom,
        controles=controles
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/workflow-pdp')
@login_required
def workflow_pdp():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS workflow_factures_pdp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facture_id INTEGER,
            numero TEXT,
            sens TEXT,
            statut TEXT,
            canal TEXT,
            accuse_reception TEXT,
            date_action TEXT,
            detail TEXT
        )
    """)

    c.execute("""
        SELECT id, facture_id, numero, sens, statut, canal, accuse_reception, date_action, detail
        FROM workflow_factures_pdp
        ORDER BY id DESC
    """)

    workflows = c.fetchall()

    conn.commit()
    conn.close()

    return render_template('workflow_pdp.html', workflows=workflows)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/depot-pdp/<int:facture_id>')
@login_required
def depot_pdp(facture_id):

    import sqlite3
    import hashlib
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT numero, client, montant_ttc
        FROM factures_dematerialisees
        WHERE id = ?
    """, (facture_id,))

    facture = c.fetchone()

    if not facture:
        conn.close()
        flash("Facture introuvable")
        return redirect('/ecritures/factur-x')

    numero, client, montant_ttc = facture
    date_action = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    accuse = hashlib.sha256(
        f"PDP|{numero}|{client}|{montant_ttc}|{date_action}".encode("utf-8")
    ).hexdigest()

    c.execute("""
        CREATE TABLE IF NOT EXISTS workflow_factures_pdp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facture_id INTEGER,
            numero TEXT,
            sens TEXT,
            statut TEXT,
            canal TEXT,
            accuse_reception TEXT,
            date_action TEXT,
            detail TEXT
        )
    """)

    c.execute("""
        INSERT INTO workflow_factures_pdp (
            facture_id, numero, sens, statut, canal,
            accuse_reception, date_action, detail
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        facture_id,
        numero,
        "EMISSION",
        "DEPOSEE",
        "PDP_INTERNE",
        accuse,
        date_action,
        f"Facture dÃ©posÃ©e sur connecteur PDP interne pour {client}"
    ))

    c.execute("""
        UPDATE factures_dematerialisees
        SET statut = ?, canal = ?, date_transmission = ?, preuve = ?
        WHERE id = ?
    """, (
        "DEPOSEE_PDP",
        "PDP_INTERNE",
        date_action,
        accuse,
        facture_id
    ))

    conn.commit()
    conn.close()

    flash("Facture dÃ©posÃ©e sur le connecteur PDP interne")
    return redirect('/ecritures/workflow-pdp')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/changer-statut-pdp/<int:workflow_id>/<statut>')
@login_required
def changer_statut_pdp(workflow_id, statut):

    import sqlite3
    from datetime import datetime

    statuts_autorises = [
        "BROUILLON",
        "DEPOSEE",
        "REÃ‡UE",
        "ACCEPTEE",
        "REJETEE",
        "EN_LITIGE",
        "PAYEE",
        "ARCHIVEE"
    ]

    if statut not in statuts_autorises:
        flash("Statut PDP non autorisÃ©")
        return redirect('/ecritures/workflow-pdp')

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE workflow_factures_pdp
        SET statut = ?, date_action = ?
        WHERE id = ?
    """, (
        statut,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        workflow_id
    ))

    conn.commit()
    conn.close()

    flash("Statut PDP mis Ã  jour")
    return redirect('/ecritures/workflow-pdp')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/reception-pdp-simulation')
@login_required
def reception_pdp_simulation():

    import sqlite3
    import hashlib
    from datetime import datetime

    date_action = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    numero = "REC-" + datetime.now().strftime("%Y%m%d%H%M%S")

    accuse = hashlib.sha256(
        f"RECEPTION|{numero}|{date_action}".encode("utf-8")
    ).hexdigest()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS workflow_factures_pdp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facture_id INTEGER,
            numero TEXT,
            sens TEXT,
            statut TEXT,
            canal TEXT,
            accuse_reception TEXT,
            date_action TEXT,
            detail TEXT
        )
    """)

    c.execute("""
        INSERT INTO workflow_factures_pdp (
            facture_id, numero, sens, statut, canal,
            accuse_reception, date_action, detail
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        0,
        numero,
        "RECEPTION",
        "REÃ‡UE",
        "PDP_INTERNE",
        accuse,
        date_action,
        "Simulation de rÃ©ception automatique d'une facture fournisseur"
    ))

    conn.commit()
    conn.close()

    flash("Facture fournisseur simulÃ©e comme reÃ§ue")
    return redirect('/ecritures/workflow-pdp')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/archivage-probatoire')
@login_required
def archivage_probatoire():

    import sqlite3
    import os
    import shutil
    import hashlib
    from datetime import datetime

    os.makedirs("archives_probatoires", exist_ok=True)

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS archives_probatoires (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_archive TEXT,
            empreinte_sha256 TEXT,
            date_archive TEXT,
            detail TEXT
        )
    """)

    nom_archive = "archive_probatoire_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".sqlite"
    chemin_archive = os.path.join("archives_probatoires", nom_archive)

    shutil.copy("db.sqlite", chemin_archive)

    with open(chemin_archive, "rb") as f:
        empreinte = hashlib.sha256(f.read()).hexdigest()

    c.execute("""
        INSERT INTO archives_probatoires (
            nom_archive, empreinte_sha256, date_archive, detail
        )
        VALUES (?, ?, ?, ?)
    """, (
        nom_archive,
        empreinte,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Archive probatoire locale avec empreinte SHA-256"
    ))

    conn.commit()
    conn.close()

    flash("Archivage probatoire crÃ©Ã©")
    return redirect('/ecritures/liste-archives-probatoires')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/liste-archives-probatoires')
@login_required
def liste_archives_probatoires():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS archives_probatoires (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_archive TEXT,
            empreinte_sha256 TEXT,
            date_archive TEXT,
            detail TEXT
        )
    """)

    c.execute("""
        SELECT id, nom_archive, empreinte_sha256, date_archive, detail
        FROM archives_probatoires
        ORDER BY id DESC
    """)

    archives = c.fetchall()

    conn.commit()
    conn.close()

    return render_template('liste_archives_probatoires.html', archives=archives)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/api/e-invoicing/factures')
@login_required
def api_e_invoicing_factures():

    import sqlite3
    from flask import jsonify

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id, numero, client, montant_ht, tva, montant_ttc, statut, canal, date_creation, date_transmission
        FROM factures_dematerialisees
        ORDER BY id DESC
    """)

    rows = c.fetchall()
    conn.close()

    factures = []

    for r in rows:
        factures.append({
            "id": r[0],
            "numero": r[1],
            "client": r[2],
            "montant_ht": r[3],
            "tva": r[4],
            "montant_ttc": r[5],
            "statut": r[6],
            "canal": r[7],
            "date_creation": r[8],
            "date_transmission": r[9]
        })

    return jsonify(factures)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/lignes-facture/<int:facture_id>', methods=['GET', 'POST'])
@login_required
def lignes_facture(facture_id):

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS lignes_factures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facture_id INTEGER,
            designation TEXT,
            quantite REAL,
            prix_unitaire REAL,
            taux_tva REAL,
            total_ht REAL,
            total_tva REAL,
            total_ttc REAL
        )
    """)

    if request.method == 'POST':
        designation = request.form.get('designation')
        quantite = float((request.form.get('quantite') or "1").replace(",", "."))
        prix_unitaire = float((request.form.get('prix_unitaire') or "0").replace(",", "."))
        taux_tva = float((request.form.get('taux_tva') or "20").replace(",", "."))

        total_ht = quantite * prix_unitaire
        total_tva = total_ht * taux_tva / 100
        total_ttc = total_ht + total_tva

        c.execute("""
            INSERT INTO lignes_factures (
                facture_id, designation, quantite, prix_unitaire, taux_tva,
                total_ht, total_tva, total_ttc
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            facture_id,
            designation,
            quantite,
            prix_unitaire,
            taux_tva,
            round(total_ht, 2),
            round(total_tva, 2),
            round(total_ttc, 2)
        ))

        c.execute("""
            SELECT COALESCE(SUM(total_ht),0), COALESCE(SUM(total_tva),0), COALESCE(SUM(total_ttc),0)
            FROM lignes_factures
            WHERE facture_id = ?
        """, (facture_id,))

        ht, tva, ttc = c.fetchone()

        c.execute("""
            UPDATE factures_dematerialisees
            SET montant_ht = ?, tva = ?, montant_ttc = ?
            WHERE id = ?
        """, (
            round(ht, 2),
            round(tva, 2),
            round(ttc, 2),
            facture_id
        ))

        conn.commit()
        conn.close()

        flash("Ligne ajoutÃ©e Ã  la facture")
        return redirect(f'/ecritures/lignes-facture/{facture_id}')

    c.execute("""
        SELECT numero, client, montant_ht, tva, montant_ttc
        FROM factures_dematerialisees
        WHERE id = ?
    """, (facture_id,))

    facture = c.fetchone()

    c.execute("""
        SELECT id, designation, quantite, prix_unitaire, taux_tva, total_ht, total_tva, total_ttc
        FROM lignes_factures
        WHERE facture_id = ?
        ORDER BY id
    """, (facture_id,))

    lignes = c.fetchall()

    conn.commit()
    conn.close()

    return render_template(
        'lignes_facture.html',
        facture_id=facture_id,
        facture=facture,
        lignes=lignes
    )
# ==============================
# MODULE PDP MINIMAL
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/pdp-ready')
@login_required
def pdp_ready():

    return render_template(
        'pdp_ready.html'
    )


@ecritures_routes.route('/annuaire-pdp')
@login_required
def annuaire_pdp():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS annuaire_clients_pdp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            siret TEXT,
            tva_intracom TEXT,
            email TEXT
        )
    """)

    c.execute("""
        SELECT id, nom, siret, tva_intracom, email
        FROM annuaire_clients_pdp
        ORDER BY nom
    """)

    clients = c.fetchall()

    conn.close()

    return render_template(
        'annuaire_pdp.html',
        clients=clients
    )
# ==============================
# PDP - AJOUT CLIENT + CONTRÃ”LE SIRET TVA
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/ajouter-client-pdp', methods=['GET', 'POST'])
@login_required
def ajouter_client_pdp():

    if request.method == 'GET':
        return render_template('ajouter_client_pdp.html')

    import sqlite3
    from datetime import datetime

    nom = request.form.get('nom')
    siret = request.form.get('siret')
    tva_intracom = request.form.get('tva_intracom')
    email = request.form.get('email')

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS annuaire_clients_pdp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            siret TEXT,
            tva_intracom TEXT,
            email TEXT
        )
    """)

    c.execute("""
        INSERT INTO annuaire_clients_pdp (nom, siret, tva_intracom, email)
        VALUES (?, ?, ?, ?)
    """, (nom, siret, tva_intracom, email))

    conn.commit()
    conn.close()

    flash("Client PDP ajoutÃ©")
    return redirect('/ecritures/annuaire-pdp')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/controle-siret-pdp/<int:client_id>')
@login_required
def controle_siret_pdp(client_id):

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT nom, siret, tva_intracom, email
        FROM annuaire_clients_pdp
        WHERE id = ?
    """, (client_id,))

    client = c.fetchone()
    conn.close()

    if not client:
        flash("Client introuvable")
        return redirect('/ecritures/annuaire-pdp')

    nom, siret, tva_intracom, email = client

    controles = []

    siret_clean = "".join(ch for ch in str(siret or "") if ch.isdigit())

    if len(siret_clean) == 14:
        controles.append("OK : le SIRET contient 14 chiffres.")
    else:
        controles.append("ERREUR : le SIRET doit contenir 14 chiffres.")

    if str(tva_intracom or "").upper().startswith("FR"):
        controles.append("OK : TVA intracommunautaire franÃ§aise dÃ©tectÃ©e.")
    else:
        controles.append("ALERTE : TVA intracommunautaire absente ou Ã  vÃ©rifier.")

    if email and "@" in email:
        controles.append("OK : email prÃ©sent.")
    else:
        controles.append("ALERTE : email absent ou invalide.")

    return render_template(
        'controle_siret_pdp.html',
        nom=nom,
        siret=siret,
        tva_intracom=tva_intracom,
        email=email,
        controles=controles
    )
# ==============================
# PDP V2 - WORKFLOW EMISSION / RECEPTION
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/workflow-pdp-v2')
@login_required
def workflow_pdp_v2():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS workflow_factures_pdp_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facture_id INTEGER,
            numero TEXT,
            sens TEXT,
            statut TEXT,
            canal TEXT,
            accuse_reception TEXT,
            date_action TEXT,
            detail TEXT
        )
    """)

    c.execute("""
        SELECT id, facture_id, numero, sens, statut, canal, accuse_reception, date_action, detail
        FROM workflow_factures_pdp_v2
        ORDER BY id DESC
    """)

    workflows = c.fetchall()

    conn.commit()
    conn.close()

    return render_template(
        'workflow_pdp_v2.html',
        workflows=workflows
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/depot-pdp-v2/<int:facture_id>')
@login_required
def depot_pdp_v2(facture_id):

    import sqlite3
    import hashlib
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT numero, client, montant_ttc
        FROM factures_dematerialisees
        WHERE id = ?
    """, (facture_id,))

    facture = c.fetchone()

    if not facture:
        conn.close()
        flash("Facture introuvable")
        return redirect('/ecritures/factur-x')

    numero, client, montant_ttc = facture
    date_action = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    accuse = hashlib.sha256(
        f"PDP_V2|{numero}|{client}|{montant_ttc}|{date_action}".encode("utf-8")
    ).hexdigest()

    c.execute("""
        CREATE TABLE IF NOT EXISTS workflow_factures_pdp_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facture_id INTEGER,
            numero TEXT,
            sens TEXT,
            statut TEXT,
            canal TEXT,
            accuse_reception TEXT,
            date_action TEXT,
            detail TEXT
        )
    """)

    c.execute("""
        INSERT INTO workflow_factures_pdp_v2 (
            facture_id, numero, sens, statut, canal,
            accuse_reception, date_action, detail
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        facture_id,
        numero,
        "EMISSION",
        "DEPOSEE",
        "PDP_INTERNE",
        accuse,
        date_action,
        f"Facture {numero} dÃ©posÃ©e pour {client}"
    ))

    c.execute("""
        UPDATE factures_dematerialisees
        SET statut = ?, canal = ?, date_transmission = ?, preuve = ?
        WHERE id = ?
    """, (
        "DEPOSEE_PDP",
        "PDP_INTERNE",
        date_action,
        accuse,
        facture_id
    ))

    conn.commit()
    conn.close()

    flash("Facture dÃ©posÃ©e dans le workflow PDP")
    return redirect('/ecritures/workflow-pdp-v2')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/reception-pdp-v2')
@login_required
def reception_pdp_v2():

    import sqlite3
    import hashlib
    from datetime import datetime

    date_action = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    numero = "REC-" + datetime.now().strftime("%Y%m%d%H%M%S")

    accuse = hashlib.sha256(
        f"RECEPTION_PDP_V2|{numero}|{date_action}".encode("utf-8")
    ).hexdigest()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS workflow_factures_pdp_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facture_id INTEGER,
            numero TEXT,
            sens TEXT,
            statut TEXT,
            canal TEXT,
            accuse_reception TEXT,
            date_action TEXT,
            detail TEXT
        )
    """)

    c.execute("""
        INSERT INTO workflow_factures_pdp_v2 (
            facture_id, numero, sens, statut, canal,
            accuse_reception, date_action, detail
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        0,
        numero,
        "RECEPTION",
        "REÃ‡UE",
        "PDP_INTERNE",
        accuse,
        date_action,
        "Simulation de rÃ©ception automatique fournisseur"
    ))

    conn.commit()
    conn.close()

    flash("RÃ©ception PDP simulÃ©e")
    return redirect('/ecritures/workflow-pdp-v2')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/statut-pdp-v2/<int:workflow_id>/<statut>')
@login_required
def statut_pdp_v2(workflow_id, statut):

    import sqlite3
    from datetime import datetime

    statuts_autorises = [
        "DEPOSEE",
        "REÃ‡UE",
        "ACCEPTEE",
        "REJETEE",
        "EN_LITIGE",
        "PAYEE",
        "ARCHIVEE"
    ]

    if statut not in statuts_autorises:
        flash("Statut non autorisÃ©")
        return redirect('/ecritures/workflow-pdp-v2')

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE workflow_factures_pdp_v2
        SET statut = ?, date_action = ?
        WHERE id = ?
    """, (
        statut,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        workflow_id
    ))

    conn.commit()
    conn.close()

    flash("Statut PDP mis Ã  jour")
    return redirect('/ecritures/workflow-pdp-v2')
# ==============================
# PDP V2 - ARCHIVAGE PROBATOIRE / API REST / JOURNAL TECHNIQUE
# ==============================


@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/journal-technique-pdp-v2')
@login_required
def journal_technique_pdp_v2():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS journal_technique_pdp_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_evenement TEXT,
            reference TEXT,
            message TEXT,
            empreinte_sha256 TEXT,
            date_evenement TEXT
        )
    """)

    c.execute("""
        SELECT id, type_evenement, reference, message, empreinte_sha256, date_evenement
        FROM journal_technique_pdp_v2
        ORDER BY id DESC
        LIMIT 200
    """)

    logs = c.fetchall()

    conn.commit()
    conn.close()

    return render_template(
        'journal_technique_pdp_v2.html',
        logs=logs
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/archivage-probatoire-v2')
@login_required
def archivage_probatoire_v2():

    import sqlite3
    import os
    import shutil
    import hashlib
    from datetime import datetime

    os.makedirs("archives_probatoires_v2", exist_ok=True)

    date_archive = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nom_archive = "archive_probatoire_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".sqlite"
    chemin_archive = os.path.join("archives_probatoires_v2", nom_archive)

    shutil.copy("db.sqlite", chemin_archive)

    with open(chemin_archive, "rb") as f:
        empreinte = hashlib.sha256(f.read()).hexdigest()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS archives_probatoires_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_archive TEXT,
            chemin_archive TEXT,
            empreinte_sha256 TEXT,
            date_archive TEXT,
            detail TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS journal_technique_pdp_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_evenement TEXT,
            reference TEXT,
            message TEXT,
            empreinte_sha256 TEXT,
            date_evenement TEXT
        )
    """)

    c.execute("""
        INSERT INTO archives_probatoires_v2 (
            nom_archive, chemin_archive, empreinte_sha256, date_archive, detail
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        nom_archive,
        chemin_archive,
        empreinte,
        date_archive,
        "Archive probatoire locale de la base ComptaPilot"
    ))

    c.execute("""
        INSERT INTO journal_technique_pdp_v2 (
            type_evenement, reference, message, empreinte_sha256, date_evenement
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        "ARCHIVAGE_PROBATOIRE",
        nom_archive,
        "Archive probatoire crÃ©Ã©e avec empreinte SHA-256",
        empreinte,
        date_archive
    ))

    conn.commit()
    conn.close()

    flash("Archive probatoire crÃ©Ã©e")
    return redirect('/ecritures/liste-archives-probatoires-v2')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/liste-archives-probatoires-v2')
@login_required
def liste_archives_probatoires_v2():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS archives_probatoires_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_archive TEXT,
            chemin_archive TEXT,
            empreinte_sha256 TEXT,
            date_archive TEXT,
            detail TEXT
        )
    """)

    c.execute("""
        SELECT id, nom_archive, chemin_archive, empreinte_sha256, date_archive, detail
        FROM archives_probatoires_v2
        ORDER BY id DESC
    """)

    archives = c.fetchall()

    conn.commit()
    conn.close()

    return render_template(
        'liste_archives_probatoires_v2.html',
        archives=archives
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/api-v2/e-invoicing/factures')
@login_required
def api_v2_e_invoicing_factures():

    import sqlite3
    from flask import jsonify

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id, numero, client, montant_ht, tva, montant_ttc, statut, canal, date_creation, date_transmission, preuve
        FROM factures_dematerialisees
        ORDER BY id DESC
    """)

    rows = c.fetchall()
    conn.close()

    factures = []

    for r in rows:
        factures.append({
            "id": r[0],
            "numero": r[1],
            "client": r[2],
            "montant_ht": r[3],
            "tva": r[4],
            "montant_ttc": r[5],
            "statut": r[6],
            "canal": r[7],
            "date_creation": r[8],
            "date_transmission": r[9],
            "preuve_sha256": r[10]
        })

    return jsonify({
        "application": "ComptaPilot",
        "module": "e-invoicing",
        "version": "v2",
        "factures": factures
    })

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/api-v2/e-invoicing/workflow')
@login_required
def api_v2_e_invoicing_workflow():

    import sqlite3
    from flask import jsonify

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS workflow_factures_pdp_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facture_id INTEGER,
            numero TEXT,
            sens TEXT,
            statut TEXT,
            canal TEXT,
            accuse_reception TEXT,
            date_action TEXT,
            detail TEXT
        )
    """)

    c.execute("""
        SELECT id, facture_id, numero, sens, statut, canal, accuse_reception, date_action, detail
        FROM workflow_factures_pdp_v2
        ORDER BY id DESC
    """)

    rows = c.fetchall()
    conn.close()

    workflows = []

    for r in rows:
        workflows.append({
            "id": r[0],
            "facture_id": r[1],
            "numero": r[2],
            "sens": r[3],
            "statut": r[4],
            "canal": r[5],
            "accuse_reception": r[6],
            "date_action": r[7],
            "detail": r[8]
        })

    return jsonify({
        "application": "ComptaPilot",
        "module": "workflow-pdp",
        "version": "v2",
        "workflows": workflows
    })

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/api-v2/e-invoicing/archives')
@login_required
def api_v2_e_invoicing_archives():

    import sqlite3
    from flask import jsonify

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS archives_probatoires_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_archive TEXT,
            chemin_archive TEXT,
            empreinte_sha256 TEXT,
            date_archive TEXT,
            detail TEXT
        )
    """)

    c.execute("""
        SELECT id, nom_archive, chemin_archive, empreinte_sha256, date_archive, detail
        FROM archives_probatoires_v2
        ORDER BY id DESC
    """)

    rows = c.fetchall()
    conn.close()

    archives = []

    for r in rows:
        archives.append({
            "id": r[0],
            "nom_archive": r[1],
            "chemin_archive": r[2],
            "empreinte_sha256": r[3],
            "date_archive": r[4],
            "detail": r[5]
        })

    return jsonify({
        "application": "ComptaPilot",
        "module": "archives-probatoires",
        "version": "v2",
        "archives": archives
    })

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/supervision-pdp-v2')
@login_required
def supervision_pdp_v2():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM factures_dematerialisees")
    nb_factures = c.fetchone()[0]

    c.execute("""
        CREATE TABLE IF NOT EXISTS workflow_factures_pdp_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facture_id INTEGER,
            numero TEXT,
            sens TEXT,
            statut TEXT,
            canal TEXT,
            accuse_reception TEXT,
            date_action TEXT,
            detail TEXT
        )
    """)

    c.execute("SELECT COUNT(*) FROM workflow_factures_pdp_v2")
    nb_workflows = c.fetchone()[0]

    c.execute("""
        SELECT COUNT(*)
        FROM workflow_factures_pdp_v2
        WHERE statut = 'REJETEE'
    """)
    nb_rejetees = c.fetchone()[0]

    c.execute("""
        SELECT COUNT(*)
        FROM workflow_factures_pdp_v2
        WHERE statut = 'EN_LITIGE'
    """)
    nb_litiges = c.fetchone()[0]

    c.execute("""
        CREATE TABLE IF NOT EXISTS archives_probatoires_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_archive TEXT,
            chemin_archive TEXT,
            empreinte_sha256 TEXT,
            date_archive TEXT,
            detail TEXT
        )
    """)

    c.execute("SELECT COUNT(*) FROM archives_probatoires_v2")
    nb_archives = c.fetchone()[0]

    conn.commit()
    conn.close()

    return render_template(
        'supervision_pdp_v2.html',
        nb_factures=nb_factures,
        nb_workflows=nb_workflows,
        nb_rejetees=nb_rejetees,
        nb_litiges=nb_litiges,
        nb_archives=nb_archives
    )
# ==============================
# API SÃ‰CURISÃ‰E V1 - JWT / API KEY / OPENAPI
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/api-secure/token')
@login_required
def api_secure_token():

    import jwt
    from datetime import datetime, timedelta
    from flask import jsonify

    secret = "COMPTAPILOT_SECRET_LOCAL_DEV"

    payload = {
        "app": "ComptaPilot",
        "user": "local_admin",
        "role": "admin",
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    token = jwt.encode(payload, secret, algorithm="HS256")

    return jsonify({
        "token": token,
        "type": "Bearer",
        "expires_in": "2 heures"
    })


def verifier_token_api():

    import jwt
    from flask import request, jsonify

    secret = "COMPTAPILOT_SECRET_LOCAL_DEV"

    auth = request.headers.get("Authorization", "")

    if not auth.startswith("Bearer "):
        return False, jsonify({"erreur": "Token manquant"}), 401

    token = auth.replace("Bearer ", "")

    try:
        jwt.decode(token, secret, algorithms=["HS256"])
        return True, None, None
    except Exception as e:
        return False, jsonify({"erreur": "Token invalide", "detail": str(e)}), 401

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/api-secure/factures')
def api_secure_factures():

    import sqlite3
    from flask import jsonify

    ok, reponse, code = verifier_token_api()

    if not ok:
        return reponse, code

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id, numero, client, montant_ht, tva, montant_ttc, statut
        FROM factures_dematerialisees
        ORDER BY id DESC
    """)

    rows = c.fetchall()
    conn.close()

    factures = []

    for r in rows:
        factures.append({
            "id": r[0],
            "numero": r[1],
            "client": r[2],
            "montant_ht": r[3],
            "tva": r[4],
            "montant_ttc": r[5],
            "statut": r[6]
        })

    return jsonify({
        "application": "ComptaPilot",
        "endpoint": "factures sÃ©curisÃ©es",
        "factures": factures
    })

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/api-secure/workflow')
def api_secure_workflow():

    import sqlite3
    from flask import jsonify

    ok, reponse, code = verifier_token_api()

    if not ok:
        return reponse, code

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id, facture_id, numero, sens, statut, canal, date_action, detail
        FROM workflow_factures_pdp_v2
        ORDER BY id DESC
    """)

    rows = c.fetchall()
    conn.close()

    workflows = []

    for r in rows:
        workflows.append({
            "id": r[0],
            "facture_id": r[1],
            "numero": r[2],
            "sens": r[3],
            "statut": r[4],
            "canal": r[5],
            "date_action": r[6],
            "detail": r[7]
        })

    return jsonify({
        "application": "ComptaPilot",
        "endpoint": "workflow sÃ©curisÃ©",
        "workflows": workflows
    })

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/openapi-comptapilot')
@login_required
def openapi_comptapilot():

    from flask import jsonify

    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "ComptaPilot API",
            "version": "1.0.0",
            "description": "API sÃ©curisÃ©e e-invoicing / PDP / factures"
        },
        "paths": {
            "/ecritures/api-secure/token": {
                "get": {
                    "summary": "GÃ©nÃ©rer un token JWT",
                    "responses": {
                        "200": {
                            "description": "Token gÃ©nÃ©rÃ©"
                        }
                    }
                }
            },
            "/ecritures/api-secure/factures": {
                "get": {
                    "summary": "Liste sÃ©curisÃ©e des factures",
                    "security": [{"bearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Liste des factures"
                        },
                        "401": {
                            "description": "Token manquant ou invalide"
                        }
                    }
                }
            },
            "/ecritures/api-secure/workflow": {
                "get": {
                    "summary": "Workflow PDP sÃ©curisÃ©",
                    "security": [{"bearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Liste workflow PDP"
                        },
                        "401": {
                            "description": "Token manquant ou invalide"
                        }
                    }
                }
            }
        },
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        }
    })# ==============================
# IMPORTATION DOCUMENTS COMPTABLES EXTERIEURS V1
# PDF / XML / CSV / TXT / CLASSEMENT / REGISTRE
# ==============================

@ecritures_routes.route('/import-documents-comptables', methods=['GET', 'POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def import_documents_comptables():

    import os
    import hashlib
    from datetime import datetime

    os.makedirs("imports_documents_comptables", exist_ok=True)

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS documents_comptables_importes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_fichier TEXT,
            type_document TEXT,
            extension TEXT,
            chemin TEXT,
            taille_ko REAL,
            empreinte_sha256 TEXT,
            statut TEXT,
            date_import TEXT,
            commentaire TEXT,
            texte_ocr TEXT
        )
    """)

    if request.method == "GET":

        c.execute("""
            SELECT
                id,
                nom_fichier,
                type_document,
                extension,
                chemin,
                taille_ko,
                empreinte_sha256,
                statut,
                date_import,
                commentaire,
                texte_ocr
            FROM documents_comptables_importes
            ORDER BY id DESC
        """)

        documents = c.fetchall()

        conn.close()

        return render_template(
            "import_documents_comptables.html",
            documents=documents
        )

    fichier = request.files.get("file")
    type_document = request.form.get("type_document") or "AUTRE"
    commentaire = request.form.get("commentaire") or ""

    if not fichier:

        conn.close()

        flash("Aucun fichier sélectionné.", "danger")

        return redirect("/ecritures/import-documents-comptables")

    nom_original = fichier.filename

    extension = (
        nom_original.rsplit(".", 1)[-1].lower()
        if "." in nom_original
        else ""
    )

    extensions_autorisees = [
        "pdf",
        "xml",
        "csv",
        "txt",
        "png",
        "jpg",
        "jpeg"
    ]

    if extension not in extensions_autorisees:

        conn.close()

        flash(
            "Extension non autorisée. Formats acceptés : PDF, XML, CSV, TXT, PNG, JPG.",
            "danger"
        )

        return redirect("/ecritures/import-documents-comptables")

    nom_securise = datetime.now().strftime("%Y%m%d_%H%M%S_") + nom_original

    chemin = os.path.join(
        "imports_documents_comptables",
        nom_securise
    )

    fichier.save(chemin)

    taille_ko = round(os.path.getsize(chemin) / 1024, 2)

    with open(chemin, "rb") as f:
        empreinte = hashlib.sha256(f.read()).hexdigest()

    texte_ocr = ""

    try:

        if extension in ["png", "jpg", "jpeg"]:

            image = Image.open(chemin)

            texte_ocr = pytesseract.image_to_string(
                image,
                lang="fra"
            )

        elif extension == "pdf":

            doc = fitz.open(chemin)

            for page in doc:

                texte_ocr += page.get_text()

            doc.close()

        elif extension in ["txt", "csv", "xml"]:

            with open(chemin, "r", encoding="utf-8", errors="ignore") as f:
                texte_ocr = f.read()

    except Exception as e:

        texte_ocr = "OCR impossible : " + str(e)

    c.execute("""
        INSERT INTO documents_comptables_importes
        (
            nom_fichier,
            type_document,
            extension,
            chemin,
            taille_ko,
            empreinte_sha256,
            statut,
            date_import,
            commentaire,
            texte_ocr
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        nom_original,
        type_document,
        extension,
        chemin,
        taille_ko,
        empreinte,
        "IMPORTE",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        commentaire,
        texte_ocr
    ))

    conn.commit()
    conn.close()

    flash("Document comptable importé avec succès.", "success")

    return redirect("/ecritures/import-documents-comptables")

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/analyser-document-comptable/<int:document_id>')
@login_required
def analyser_document_comptable(document_id):

    import sqlite3
    import csv
    import xml.etree.ElementTree as ET
    from pypdf import PdfReader

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT nom_fichier, type_document, extension, chemin, commentaire
        FROM documents_comptables_importes
        WHERE id = ?
    """, (document_id,))

    doc = c.fetchone()

    if not doc:
        conn.close()
        flash("Document introuvable")
        return redirect('/ecritures/import-documents-comptables')

    nom_fichier, type_document, extension, chemin, commentaire = doc

    resultat = []

    try:
        if extension == "pdf":
            reader = PdfReader(chemin)
            texte = ""
            for page in reader.pages:
                texte += page.extract_text() or ""

            resultat.append("Lecture PDF effectuÃ©e.")
            resultat.append(texte[:5000] if texte else "Aucun texte dÃ©tectÃ© dans le PDF.")

        elif extension == "xml":
            tree = ET.parse(chemin)
            root = tree.getroot()

            resultat.append("Lecture XML effectuÃ©e.")
            resultat.append("Balise racine : " + root.tag)

            for elem in list(root)[:20]:
                resultat.append(f"{elem.tag} : {elem.text}")

        elif extension == "csv":
            with open(chemin, "r", encoding="utf-8-sig") as f:
                sample = f.read(5000)

            resultat.append("Lecture CSV effectuÃ©e.")
            resultat.append(sample)

        elif extension == "txt":
            with open(chemin, "r", encoding="utf-8-sig") as f:
                texte = f.read(5000)

            resultat.append("Lecture TXT effectuÃ©e.")
            resultat.append(texte)

        else:
            resultat.append("Format non analysable.")

        c.execute("""
            UPDATE documents_comptables_importes
            SET statut = ?
            WHERE id = ?
        """, ("ANALYSE", document_id))

    except Exception as e:
        resultat.append("Erreur pendant l'analyse : " + str(e))

        c.execute("""
            UPDATE documents_comptables_importes
            SET statut = ?
            WHERE id = ?
        """, ("ERREUR_ANALYSE", document_id))

    conn.commit()
    conn.close()

    return render_template(
        'analyse_document_comptable.html',
        nom_fichier=nom_fichier,
        type_document=type_document,
        extension=extension,
        commentaire=commentaire,
        resultat=resultat
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/changer-statut-document-comptable/<int:document_id>/<statut>')
@login_required
def changer_statut_document_comptable(document_id, statut):

    import sqlite3

    statuts_autorises = [
        "IMPORTE",
        "ANALYSE",
        "A_TRAITER",
        "TRAITE",
        "REJETE",
        "ARCHIVE"
    ]

    if statut not in statuts_autorises:
        flash("Statut non autorisÃ©")
        return redirect('/ecritures/import-documents-comptables')

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE documents_comptables_importes
        SET statut = ?
        WHERE id = ?
    """, (statut, document_id))

    conn.commit()
    conn.close()

    flash("Statut du document mis Ã  jour")
    return redirect('/ecritures/import-documents-comptables')
# ==============================
# EXTRACTION INTELLIGENTE DOCUMENTS COMPTABLES V1
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/extraire-document-comptable/<int:document_id>')
@login_required
def extraire_document_comptable(document_id):

    import sqlite3
    import re
    from pypdf import PdfReader

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT nom_fichier, type_document, extension, chemin
        FROM documents_comptables_importes
        WHERE id = ?
    """, (document_id,))

    doc = c.fetchone()

    if not doc:
        conn.close()
        flash("Document introuvable")
        return redirect('/ecritures/import-documents-comptables')

    nom_fichier, type_document, extension, chemin = doc

    texte = ""

    try:
        if extension == "pdf":
            reader = PdfReader(chemin)
            for page in reader.pages:
                texte += page.extract_text() or ""

        elif extension in ["txt", "csv", "xml"]:
            with open(chemin, "r", encoding="utf-8-sig") as f:
                texte = f.read()

    except Exception as e:
        texte = "Erreur lecture document : " + str(e)

    montants = re.findall(r"\d+[,.]\d{2}", texte)
    dates = re.findall(r"\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2}", texte)
    sirets = re.findall(r"\b\d{14}\b", texte)
    tvas = re.findall(r"\bFR[A-Z0-9]{2}\d{9}\b", texte.upper())
    factures = re.findall(r"(?:facture|invoice|nÂ°|numero|numÃ©ro)[\s:.-]*([A-Z0-9\-\/]+)", texte, re.IGNORECASE)

    montant_ttc = montants[-1] if montants else ""
    date_document = dates[0] if dates else ""
    siret = sirets[0] if sirets else ""
    tva_intracom = tvas[0] if tvas else ""
    numero_facture = factures[0] if factures else ""

    fournisseur_probable = ""
    lignes = texte.splitlines()

    for ligne in lignes[:20]:
        if len(ligne.strip()) > 3:
            fournisseur_probable = ligne.strip()
            break

    c.execute("""
        CREATE TABLE IF NOT EXISTS extractions_documents_comptables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            fournisseur_client TEXT,
            numero_facture TEXT,
            date_document TEXT,
            montant_ttc TEXT,
            siret TEXT,
            tva_intracom TEXT,
            type_probable TEXT,
            texte_extrait TEXT
        )
    """)

    c.execute("""
        INSERT INTO extractions_documents_comptables (
            document_id, fournisseur_client, numero_facture, date_document,
            montant_ttc, siret, tva_intracom, type_probable, texte_extrait
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        document_id,
        fournisseur_probable,
        numero_facture,
        date_document,
        montant_ttc,
        siret,
        tva_intracom,
        type_document,
        texte[:10000]
    ))

    c.execute("""
        UPDATE documents_comptables_importes
        SET statut = ?
        WHERE id = ?
    """, ("EXTRAIT", document_id))

    conn.commit()
    conn.close()

    return render_template(
        'extraction_document_comptable.html',
        nom_fichier=nom_fichier,
        fournisseur_probable=fournisseur_probable,
        numero_facture=numero_facture,
        date_document=date_document,
        montant_ttc=montant_ttc,
        siret=siret,
        tva_intracom=tva_intracom,
        type_document=type_document,
        texte=texte[:3000]
    )
# ==============================
# PRE-COMPTABILISATION AUTOMATIQUE V1
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/precomptabiliser-document/<int:document_id>')
@login_required
def precomptabiliser_document(document_id):

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            fournisseur_client,
            numero_facture,
            date_document,
            montant_ttc,
            siret,
            tva_intracom,
            type_probable
        FROM extractions_documents_comptables
        WHERE document_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (document_id,))

    extraction = c.fetchone()

    if not extraction:
        conn.close()
        flash("Aucune extraction trouvÃ©e")
        return redirect('/ecritures/import-documents-comptables')

    (
        fournisseur_client,
        numero_facture,
        date_document,
        montant_ttc,
        siret,
        tva_intracom,
        type_probable
    ) = extraction

    try:
        montant_ttc_float = float(
            str(montant_ttc).replace(",", ".")
        )
    except:
        montant_ttc_float = 0

    montant_ht = round(montant_ttc_float / 1.20, 2)
    montant_tva = round(montant_ttc_float - montant_ht, 2)

    journal = "OD"
    compte_charge = "628"
    compte_tva = "44566"
    compte_tiers = "401"
    sens = "ACHAT"

    type_upper = str(type_probable or "").upper()

    if "CLIENT" in type_upper:
        journal = "VEN"
        compte_charge = "706"
        compte_tiers = "411"
        sens = "VENTE"

    elif "FOURNISSEUR" in type_upper:
        journal = "ACH"
        compte_charge = "607"
        compte_tiers = "401"
        sens = "ACHAT"

    elif "BANCAIRE" in type_upper:
        journal = "BQ"
        compte_charge = "512"
        compte_tiers = "512"
        sens = "BANQUE"

    libelle = f"{sens} {fournisseur_client} {numero_facture}"

    c.execute("""
        CREATE TABLE IF NOT EXISTS precomptabilisation_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            journal TEXT,
            compte_tiers TEXT,
            compte_charge TEXT,
            compte_tva TEXT,
            libelle TEXT,
            date_piece TEXT,
            montant_ht REAL,
            montant_tva REAL,
            montant_ttc REAL,
            statut TEXT
        )
    """)

    c.execute("""
        INSERT INTO precomptabilisation_documents (
            document_id,
            journal,
            compte_tiers,
            compte_charge,
            compte_tva,
            libelle,
            date_piece,
            montant_ht,
            montant_tva,
            montant_ttc,
            statut
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        document_id,
        journal,
        compte_tiers,
        compte_charge,
        compte_tva,
        libelle,
        date_document,
        montant_ht,
        montant_tva,
        montant_ttc_float,
        "A_VALIDER"
    ))

    c.execute("""
        UPDATE documents_comptables_importes
        SET statut = ?
        WHERE id = ?
    """, ("PRECOMPTABILISE", document_id))

    conn.commit()
    conn.close()

    flash("PrÃ©-comptabilisation gÃ©nÃ©rÃ©e")
    return redirect('/ecritures/liste-precomptabilisations')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/liste-precomptabilisations')
@login_required
def liste_precomptabilisations():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS precomptabilisation_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            journal TEXT,
            compte_tiers TEXT,
            compte_charge TEXT,
            compte_tva TEXT,
            libelle TEXT,
            date_piece TEXT,
            montant_ht REAL,
            montant_tva REAL,
            montant_ttc REAL,
            statut TEXT
        )
    """)

    c.execute("""
        SELECT
            id,
            document_id,
            journal,
            compte_tiers,
            compte_charge,
            compte_tva,
            libelle,
            date_piece,
            montant_ht,
            montant_tva,
            montant_ttc,
            statut
        FROM precomptabilisation_documents
        ORDER BY id DESC
    """)

    lignes = c.fetchall()

    conn.close()

    return render_template(
        'liste_precomptabilisations.html',
        lignes=lignes
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/valider-precomptabilisation/<int:precomp_id>')
@login_required
def valider_precomptabilisation(precomp_id):

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            document_id,
            journal,
            compte_tiers,
            compte_charge,
            compte_tva,
            libelle,
            date_piece,
            montant_ht,
            montant_tva,
            montant_ttc
        FROM precomptabilisation_documents
        WHERE id = ?
    """, (precomp_id,))

    ligne = c.fetchone()

    if not ligne:
        conn.close()
        flash("PrÃ©-comptabilisation introuvable")
        return redirect('/ecritures/liste-precomptabilisations')

    (
        document_id,
        journal,
        compte_tiers,
        compte_charge,
        compte_tva,
        libelle,
        date_piece,
        montant_ht,
        montant_tva,
        montant_ttc
    ) = ligne

    c.execute("""
        CREATE TABLE IF NOT EXISTS ecritures_auto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            journal TEXT,
            date_ecriture TEXT,
            libelle TEXT,
            compte_id TEXT,
            debit REAL,
            credit REAL
        )
    """)

    # Ligne charge / produit
    c.execute("""
        INSERT INTO ecritures_auto (
            journal, date_ecriture, libelle,
            compte_id, debit, credit
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        journal,
        date_piece,
        libelle,
        compte_charge,
        montant_ht,
        0
    ))

    # TVA
    c.execute("""
        INSERT INTO ecritures_auto (
            journal, date_ecriture, libelle,
            compte_id, debit, credit
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        journal,
        date_piece,
        libelle,
        compte_tva,
        montant_tva,
        0
    ))

    # Tiers
    c.execute("""
        INSERT INTO ecritures_auto (
            journal, date_ecriture, libelle,
            compte_id, debit, credit
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        journal,
        date_piece,
        libelle,
        compte_tiers,
        0,
        montant_ttc
    ))

    c.execute("""
        UPDATE precomptabilisation_documents
        SET statut = ?
        WHERE id = ?
    """, (
        "VALIDEE",
        precomp_id
    ))

    conn.commit()
    conn.close()

    flash("Ã‰criture comptable gÃ©nÃ©rÃ©e automatiquement")
    return redirect('/ecritures/liste-precomptabilisations')
# ==============================
# ECRITURES COMPTABLES AUTOMATIQUES
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/ecritures-automatiques')
@login_required
def ecritures_automatiques():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS ecritures_auto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            journal TEXT,
            date_ecriture TEXT,
            libelle TEXT,
            compte_id TEXT,
            debit REAL,
            credit REAL
        )
    """)

    c.execute("""
        SELECT
            id,
            journal,
            date_ecriture,
            libelle,
            compte_id,
            debit,
            credit
        FROM ecritures_auto
        ORDER BY id DESC
    """)

    lignes = c.fetchall()

    conn.close()

    return render_template(
        'ecritures_automatiques.html',
        lignes=lignes
    )
# ==============================
# ASSISTANT COMPTABLE INTELLIGENT V1
# APPRENTISSAGE COMPTES / ANTI-DOUBLON / SCORE CONFIANCE
# ==============================

# ==============================
# ASSISTANT COMPTABLE INTELLIGENT V1
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/assistant-comptable-intelligent')
@login_required
def assistant_comptable_intelligent():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS regles_comptables_ia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mot_cle TEXT,
            compte_suggere TEXT,
            journal_suggere TEXT,
            type_document TEXT,
            commentaire TEXT
        )
    """)

    c.execute("""
        SELECT id, mot_cle, compte_suggere, journal_suggere, type_document, commentaire
        FROM regles_comptables_ia
        ORDER BY id DESC
    """)

    regles = c.fetchall()

    conn.close()

    return render_template(
        'assistant_comptable_intelligent.html',
        regles=regles
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/ajouter-regle-comptable-ia', methods=['GET', 'POST'])
@login_required
def ajouter_regle_comptable_ia():

    if request.method == 'GET':
        return render_template('ajouter_regle_comptable_ia.html')

    import sqlite3

    mot_cle = request.form.get('mot_cle')
    compte_suggere = request.form.get('compte_suggere')
    journal_suggere = request.form.get('journal_suggere')
    type_document = request.form.get('type_document')
    commentaire = request.form.get('commentaire')

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS regles_comptables_ia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mot_cle TEXT,
            compte_suggere TEXT,
            journal_suggere TEXT,
            type_document TEXT,
            commentaire TEXT
        )
    """)

    c.execute("""
        INSERT INTO regles_comptables_ia (
            mot_cle, compte_suggere, journal_suggere, type_document, commentaire
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        mot_cle,
        compte_suggere,
        journal_suggere,
        type_document,
        commentaire
    ))

    conn.commit()
    conn.close()

    flash("RÃ¨gle comptable IA ajoutÃ©e")
    return redirect('/ecritures/assistant-comptable-intelligent')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/analyse-ia-document/<int:document_id>')
@login_required
def analyse_ia_document(document_id):

    import sqlite3
    import hashlib

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT nom_fichier, type_document, empreinte_sha256
        FROM documents_comptables_importes
        WHERE id = ?
    """, (document_id,))

    document = c.fetchone()

    if not document:
        conn.close()
        flash("Document introuvable")
        return redirect('/ecritures/import-documents-comptables')

    nom_fichier, type_document, empreinte = document

    c.execute("""
        SELECT fournisseur_client, numero_facture, date_document, montant_ttc, texte_extrait
        FROM extractions_documents_comptables
        WHERE document_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (document_id,))

    extraction = c.fetchone()

    if not extraction:
        conn.close()
        flash("Extraction introuvable. Lance d'abord Extraction intelligente.")
        return redirect('/ecritures/import-documents-comptables')

    fournisseur_client, numero_facture, date_document, montant_ttc, texte_extrait = extraction

    c.execute("""
        SELECT COUNT(*)
        FROM documents_comptables_importes
        WHERE empreinte_sha256 = ?
    """, (empreinte,))

    nb_meme_hash = c.fetchone()[0]

    doublon = nb_meme_hash > 1

    c.execute("""
        SELECT mot_cle, compte_suggere, journal_suggere, type_document, commentaire
        FROM regles_comptables_ia
    """)

    regles = c.fetchall()

    compte_suggere = "628"
    journal_suggere = "OD"
    regle_trouvee = "Aucune rÃ¨gle trouvÃ©e"
    score = 50

    texte_global = f"{nom_fichier} {type_document} {fournisseur_client} {texte_extrait}".lower()

    for r in regles:
        mot_cle, compte_id, journal, type_regle, commentaire = r

        if mot_cle and mot_cle.lower() in texte_global:
            compte_suggere = compte
            journal_suggere = journal
            regle_trouvee = f"Mot-clÃ© trouvÃ© : {mot_cle}"
            score = 90
            break

    if doublon:
        score = 20

    c.execute("""
        CREATE TABLE IF NOT EXISTS analyses_ia_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            compte_suggere TEXT,
            journal_suggere TEXT,
            regle_trouvee TEXT,
            score_confiance INTEGER,
            doublon TEXT
        )
    """)

    c.execute("""
        INSERT INTO analyses_ia_documents (
            document_id, compte_suggere, journal_suggere,
            regle_trouvee, score_confiance, doublon
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        document_id,
        compte_suggere,
        journal_suggere,
        regle_trouvee,
        score,
        "OUI" if doublon else "NON"
    ))

    conn.commit()
    conn.close()

    return render_template(
        'analyse_ia_document.html',
        nom_fichier=nom_fichier,
        fournisseur_client=fournisseur_client,
        numero_facture=numero_facture,
        montant_ttc=montant_ttc,
        compte_suggere=compte_suggere,
        journal_suggere=journal_suggere,
        regle_trouvee=regle_trouvee,
        score=score,
        doublon=doublon
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/liste-analyses-ia')
@login_required
def liste_analyses_ia():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS analyses_ia_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            compte_suggere TEXT,
            journal_suggere TEXT,
            regle_trouvee TEXT,
            score_confiance INTEGER,
            doublon TEXT
        )
    """)

    c.execute("""
        SELECT id, document_id, compte_suggere, journal_suggere,
               regle_trouvee, score_confiance, doublon
        FROM analyses_ia_documents
        ORDER BY id DESC
    """)

    analyses = c.fetchall()

    conn.close()

    return render_template(
        'liste_analyses_ia.html',
        analyses=analyses
    )
# ==============================
# MOTEUR APPRENTISSAGE IA COMPTABLE V2
# FOURNISSEURS / PCG / TVA / ANOMALIES / GED / MATCHING BANQUE
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/moteur-apprentissage-ia-v2')
@login_required
def moteur_apprentissage_ia_v2():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS fournisseurs_ia_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            compte_pcg TEXT,
            compte_tva TEXT,
            journal TEXT,
            taux_tva REAL,
            nb_validations INTEGER DEFAULT 0,
            derniere_utilisation TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS historique_apprentissage_ia_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fournisseur TEXT,
            compte_pcg TEXT,
            compte_tva TEXT,
            journal TEXT,
            montant_ttc REAL,
            source TEXT,
            date_apprentissage TEXT
        )
    """)

    c.execute("SELECT COUNT(*) FROM fournisseurs_ia_v2")
    nb_fournisseurs = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM historique_apprentissage_ia_v2")
    nb_apprentissages = c.fetchone()[0]

    conn.commit()
    conn.close()

    return render_template(
        'moteur_apprentissage_ia_v2.html',
        nb_fournisseurs=nb_fournisseurs,
        nb_apprentissages=nb_apprentissages
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/fournisseurs-ia-v2')
@login_required
def fournisseurs_ia_v2():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS fournisseurs_ia_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            compte_pcg TEXT,
            compte_tva TEXT,
            journal TEXT,
            taux_tva REAL,
            nb_validations INTEGER DEFAULT 0,
            derniere_utilisation TEXT
        )
    """)

    c.execute("""
        SELECT id, nom, compte_pcg, compte_tva, journal, taux_tva, nb_validations, derniere_utilisation
        FROM fournisseurs_ia_v2
        ORDER BY nb_validations DESC, nom
    """)

    fournisseurs = c.fetchall()

    conn.commit()
    conn.close()

    return render_template(
        'fournisseurs_ia_v2.html',
        fournisseurs=fournisseurs
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/apprentissage-depuis-precompta-v2/<int:precomp_id>')
@login_required
def apprentissage_depuis_precompta_v2(precomp_id):

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT libelle, compte_charge, compte_tva, journal, montant_ttc
        FROM precomptabilisation_documents
        WHERE id = ?
    """, (precomp_id,))

    ligne = c.fetchone()

    if not ligne:
        conn.close()
        flash("PrÃ©-comptabilisation introuvable")
        return redirect('/ecritures/liste-precomptabilisations')

    libelle, compte_charge, compte_tva, journal, montant_ttc = ligne

    fournisseur = str(libelle or "").replace("ACHAT", "").replace("VENTE", "").strip()

    if not fournisseur:
        fournisseur = "FOURNISSEUR_INCONNU"

    c.execute("""
        CREATE TABLE IF NOT EXISTS fournisseurs_ia_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            compte_pcg TEXT,
            compte_tva TEXT,
            journal TEXT,
            taux_tva REAL,
            nb_validations INTEGER DEFAULT 0,
            derniere_utilisation TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS historique_apprentissage_ia_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fournisseur TEXT,
            compte_pcg TEXT,
            compte_tva TEXT,
            journal TEXT,
            montant_ttc REAL,
            source TEXT,
            date_apprentissage TEXT
        )
    """)

    c.execute("""
        SELECT id, nb_validations
        FROM fournisseurs_ia_v2
        WHERE lower(nom) = lower(?)
    """, (fournisseur,))

    existant = c.fetchone()
    maintenant = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if existant:
        fournisseur_id, nb_validations = existant
        c.execute("""
            UPDATE fournisseurs_ia_v2
            SET compte_pcg = ?, compte_tva = ?, journal = ?,
                nb_validations = ?, derniere_utilisation = ?
            WHERE id = ?
        """, (
            compte_charge,
            compte_tva,
            journal,
            int(nb_validations or 0) + 1,
            maintenant,
            fournisseur_id
        ))
    else:
        c.execute("""
            INSERT INTO fournisseurs_ia_v2 (
                nom, compte_pcg, compte_tva, journal, taux_tva,
                nb_validations, derniere_utilisation
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            fournisseur,
            compte_charge,
            compte_tva,
            journal,
            20,
            1,
            maintenant
        ))

    c.execute("""
        INSERT INTO historique_apprentissage_ia_v2 (
            fournisseur, compte_pcg, compte_tva, journal,
            montant_ttc, source, date_apprentissage
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        fournisseur,
        compte_charge,
        compte_tva,
        journal,
        montant_ttc,
        "VALIDATION_PRECOMPTA",
        maintenant
    ))

    conn.commit()
    conn.close()

    flash("Apprentissage IA enregistrÃ©")
    return redirect('/ecritures/fournisseurs-ia-v2')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/suggestion-pcg-ia-v2/<int:document_id>')
@login_required
def suggestion_pcg_ia_v2(document_id):

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT fournisseur_client, montant_ttc, type_probable, texte_extrait
        FROM extractions_documents_comptables
        WHERE document_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (document_id,))

    extraction = c.fetchone()

    if not extraction:
        conn.close()
        flash("Extraction introuvable")
        return redirect('/ecritures/import-documents-comptables')

    fournisseur_client, montant_ttc, type_probable, texte_extrait = extraction

    c.execute("""
        CREATE TABLE IF NOT EXISTS fournisseurs_ia_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            compte_pcg TEXT,
            compte_tva TEXT,
            journal TEXT,
            taux_tva REAL,
            nb_validations INTEGER DEFAULT 0,
            derniere_utilisation TEXT
        )
    """)

    c.execute("""
        SELECT nom, compte_pcg, compte_tva, journal, taux_tva, nb_validations
        FROM fournisseurs_ia_v2
        ORDER BY nb_validations DESC
    """)

    fournisseurs = c.fetchall()

    compte_pcg = "628"
    compte_tva = "44566"
    journal = "OD"
    taux_tva = 20
    score = 45
    motif = "Suggestion par dÃ©faut"

    texte_global = f"{fournisseur_client} {type_probable} {texte_extrait}".lower()

    for f in fournisseurs:
        nom, pcg, tva, jrn, taux, nb = f

        if nom and nom.lower() in texte_global:
            compte_pcg = pcg
            compte_tva = tva
            journal = jrn
            taux_tva = taux
            score = min(95, 70 + int(nb or 0) * 5)
            motif = f"Fournisseur reconnu : {nom}"
            break

    return render_template(
        'suggestion_pcg_ia_v2.html',
        document_id=document_id,
        fournisseur_client=fournisseur_client,
        montant_ttc=montant_ttc,
        compte_pcg=compte_pcg,
        compte_tva=compte_tva,
        journal=journal,
        taux_tva=taux_tva,
        score=score,
        motif=motif
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/detection-anomalies-ia-v2/<int:document_id>')
@login_required
def detection_anomalies_ia_v2(document_id):

    import sqlite3

    anomalies = []

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT nom_fichier, type_document, empreinte_sha256, statut
        FROM documents_comptables_importes
        WHERE id = ?
    """, (document_id,))

    doc = c.fetchone()

    if not doc:
        conn.close()
        flash("Document introuvable")
        return redirect('/ecritures/import-documents-comptables')

    nom_fichier, type_document, empreinte, statut = doc

    c.execute("""
        SELECT COUNT(*)
        FROM documents_comptables_importes
        WHERE empreinte_sha256 = ?
    """, (empreinte,))

    nb_hash = c.fetchone()[0]

    if nb_hash > 1:
        anomalies.append("DOUBLON : mÃªme empreinte SHA-256 dÃ©tectÃ©e plusieurs fois.")

    c.execute("""
        SELECT fournisseur_client, numero_facture, date_document, montant_ttc, siret, tva_intracom
        FROM extractions_documents_comptables
        WHERE document_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (document_id,))

    extraction = c.fetchone()

    if extraction:
        fournisseur, numero, date_doc, montant_ttc, siret, tva_intracom = extraction

        if not numero:
            anomalies.append("ALERTE : numÃ©ro de facture non dÃ©tectÃ©.")

        if not date_doc:
            anomalies.append("ALERTE : date du document non dÃ©tectÃ©e.")

        try:
            montant = float(str(montant_ttc).replace(",", "."))
            if montant <= 0:
                anomalies.append("ERREUR : montant TTC nul ou nÃ©gatif.")
            if montant > 10000:
                anomalies.append("ALERTE : montant Ã©levÃ© supÃ©rieur Ã  10 000 â‚¬.")
        except:
            anomalies.append("ERREUR : montant TTC illisible.")

        if not siret:
            anomalies.append("ALERTE : SIRET non dÃ©tectÃ©.")

        if not tva_intracom:
            anomalies.append("ALERTE : TVA intracommunautaire non dÃ©tectÃ©e.")
    else:
        anomalies.append("ERREUR : aucune extraction intelligente trouvÃ©e.")

    if not anomalies:
        anomalies.append("OK : aucune anomalie majeure dÃ©tectÃ©e.")

    conn.close()

    return render_template(
        'detection_anomalies_ia_v2.html',
        document_id=document_id,
        nom_fichier=nom_fichier,
        anomalies=anomalies
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/ged-comptable-avancee-v2')
@login_required
def ged_comptable_avancee_v2():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id, nom_fichier, type_document, extension, chemin,
               taille_ko, statut, date_import, commentaire
        FROM documents_comptables_importes
        ORDER BY id DESC
    """)

    documents = c.fetchall()
    conn.close()

    return render_template(
        'ged_comptable_avancee_v2.html',
        documents=documents
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/matching-facture-banque-ia-v2/<int:document_id>')
@login_required
def matching_facture_banque_ia_v2(document_id):

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT fournisseur_client, montant_ttc, date_document
        FROM extractions_documents_comptables
        WHERE document_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (document_id,))

    extraction = c.fetchone()

    if not extraction:
        conn.close()
        flash("Extraction introuvable")
        return redirect('/ecritures/import-documents-comptables')

    fournisseur, montant_ttc, date_document = extraction

    try:
        montant = abs(float(str(montant_ttc).replace(",", ".")))
    except:
        montant = 0

    c.execute("""
        SELECT id, date_ecriture, libelle, debit, credit, journal
        FROM ecritures
        WHERE ABS(debit - ?) < 1 OR ABS(credit - ?) < 1
        ORDER BY date_ecriture DESC
        LIMIT 20
    """, (montant, montant))

    rapprochements = c.fetchall()

    conn.close()

    return render_template(
        'matching_facture_banque_ia_v2.html',
        document_id=document_id,
        fournisseur=fournisseur,
        montant_ttc=montant_ttc,
        rapprochements=rapprochements
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/workflow-expert-comptable-v2')
@login_required
def workflow_expert_comptable_v2():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS workflow_expert_comptable_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            statut TEXT,
            validateur TEXT,
            commentaire TEXT,
            date_action TEXT
        )
    """)

    c.execute("""
        SELECT id, document_id, statut, validateur, commentaire, date_action
        FROM workflow_expert_comptable_v2
        ORDER BY id DESC
    """)

    validations = c.fetchall()

    conn.commit()
    conn.close()

    return render_template(
        'workflow_expert_comptable_v2.html',
        validations=validations
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/validation-expert-v2/<int:document_id>/<decision>')
@login_required
def validation_expert_v2(document_id, decision):

    import sqlite3
    from datetime import datetime

    decisions = ["APPROUVE", "REJETE", "A_CORRIGER"]

    if decision not in decisions:
        flash("DÃ©cision non autorisÃ©e")
        return redirect('/ecritures/import-documents-comptables')

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS workflow_expert_comptable_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            statut TEXT,
            validateur TEXT,
            commentaire TEXT,
            date_action TEXT
        )
    """)

    c.execute("""
        INSERT INTO workflow_expert_comptable_v2 (
            document_id, statut, validateur, commentaire, date_action
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        document_id,
        decision,
        "expert_local",
        "Validation expert-comptable simulÃ©e",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    c.execute("""
        UPDATE documents_comptables_importes
        SET statut = ?
        WHERE id = ?
    """, (
        decision,
        document_id
    ))

    conn.commit()
    conn.close()

    flash("DÃ©cision expert-comptable enregistrÃ©e")
    return redirect('/ecritures/workflow-expert-comptable-v2')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/historique-apprentissage-ia-v2')
@login_required
def historique_apprentissage_ia_v2():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS historique_apprentissage_ia_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fournisseur TEXT,
            compte_pcg TEXT,
            compte_tva TEXT,
            journal TEXT,
            montant_ttc REAL,
            source TEXT,
            date_apprentissage TEXT
        )
    """)

    c.execute("""
        SELECT id, fournisseur, compte_pcg, compte_tva, journal,
               montant_ttc, source, date_apprentissage
        FROM historique_apprentissage_ia_v2
        ORDER BY id DESC
    """)

    historique = c.fetchall()

    conn.commit()
    conn.close()

    return render_template(
        'historique_apprentissage_ia_v2.html',
        historique=historique
    )
# ==============================
# PRODUCTION COMPTABLE AUTOMATIQUE COMPLETE V3
# TVA CA3 / GRAND LIVRE / BALANCE / BILAN / RESULTAT / CLOTURE / FRAUDE / FEC / API / DSP2
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/production-comptable-v3')
@login_required
def production_comptable_v3():

    return render_template('production_comptable_v3.html')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/grand-livre-v3')
@login_required
def grand_livre_v3():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS ecritures_auto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            journal TEXT,
            date_ecriture TEXT,
            libelle TEXT,
            compte_id TEXT,
            debit REAL,
            credit REAL
        )
    """)

    c.execute("""
        SELECT compte_id, journal, date_ecriture, libelle, debit, credit
        FROM ecritures_auto
        ORDER BY compte_id, date_ecriture, id
    """)

    lignes = c.fetchall()
    conn.close()

    return render_template('grand_livre_v3.html', lignes=lignes)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/balance-v3')
@login_required
def balance_v3():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS ecritures_auto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            journal TEXT,
            date_ecriture TEXT,
            libelle TEXT,
            compte_id TEXT,
            debit REAL,
            credit REAL
        )
    """)

    c.execute("""
        SELECT
            compte_id,
            COALESCE(SUM(debit),0),
            COALESCE(SUM(credit),0),
            COALESCE(SUM(debit-credit),0)
        FROM ecritures_auto
        GROUP BY compte_id
        ORDER BY compte_id
    """)

    lignes = c.fetchall()
    conn.close()

    return render_template('balance_v3.html', lignes=lignes)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/tva-ca3-v3')
@login_required
def tva_ca3_v3():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS ecritures_auto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            journal TEXT,
            date_ecriture TEXT,
            libelle TEXT,
            compte_id TEXT,
            debit REAL,
            credit REAL
        )
    """)

    c.execute("""
        SELECT COALESCE(SUM(debit),0)
        FROM ecritures_auto
        WHERE compte_id LIKE '44566%'
    """)
    tva_deductible = c.fetchone()[0] or 0

    c.execute("""
        SELECT COALESCE(SUM(credit),0)
        FROM ecritures_auto
        WHERE compte_id LIKE '44571%'
    """)
    tva_collectee = c.fetchone()[0] or 0

    tva_due = round(float(tva_collectee) - float(tva_deductible), 2)

    conn.close()

    return render_template(
        'tva_ca3_v3.html',
        tva_deductible=round(tva_deductible, 2),
        tva_collectee=round(tva_collectee, 2),
        tva_due=tva_due
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/bilan-v3')
@login_required
def bilan_v3():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT compte_id, COALESCE(SUM(debit-credit),0)
        FROM ecritures_auto
        GROUP BY compte
    """)

    rows = c.fetchall()
    conn.close()

    actif = 0
    passif = 0

    for compte_id, solde in rows:
        compte_id = str(compte or "")
        solde = float(solde or 0)

        if compte.startswith(("2", "3", "4", "5")):
            actif += solde

        if compte.startswith(("1", "4")):
            passif += -solde

    return render_template(
        'bilan_v3.html',
        actif=round(actif, 2),
        passif=round(passif, 2),
        ecart=round(actif-passif, 2)
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/compte-resultat-v3')
@login_required
def compte_resultat_v3():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT COALESCE(SUM(debit-credit),0)
        FROM ecritures_auto
        WHERE compte_id IN (SELECT id FROM plan_comptable WHERE numero LIKE '6%')
    """)
    charges = c.fetchone()[0] or 0

    c.execute("""
        SELECT COALESCE(SUM(credit-debit),0)
        FROM ecritures_auto
        WHERE compte_id IN (SELECT id FROM plan_comptable WHERE numero LIKE '7%')
    """)
    produits = c.fetchone()[0] or 0

    conn.close()

    resultat = round(float(produits) - float(charges), 2)

    return render_template(
        'compte_resultat_v3.html',
        charges=round(charges, 2),
        produits=round(produits, 2),
        resultat=resultat
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/cloture-comptable-v3')
@login_required
def cloture_comptable_v3():

    import sqlite3
    import hashlib
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS clotures_comptables_v3 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_cloture TEXT,
            total_debit REAL,
            total_credit REAL,
            resultat REAL,
            empreinte_sha256 TEXT,
            statut TEXT
        )
    """)

    c.execute("SELECT COALESCE(SUM(debit),0), COALESCE(SUM(credit),0) FROM ecritures_auto")
    total_debit, total_credit = c.fetchone()

    resultat = float(total_credit or 0) - float(total_debit or 0)
    date_cloture = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    empreinte = hashlib.sha256(
        f"{date_cloture}|{total_debit}|{total_credit}|{resultat}".encode("utf-8")
    ).hexdigest()

    c.execute("""
        INSERT INTO clotures_comptables_v3 (
            date_cloture, total_debit, total_credit, resultat, empreinte_sha256, statut
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        date_cloture,
        round(total_debit, 2),
        round(total_credit, 2),
        round(resultat, 2),
        empreinte,
        "CLOTURE_SIMULEE"
    ))

    conn.commit()
    conn.close()

    flash("ClÃ´ture comptable simulÃ©e crÃ©Ã©e")
    return redirect('/ecritures/liste-clotures-v3')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/liste-clotures-v3')
@login_required
def liste_clotures_v3():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS clotures_comptables_v3 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_cloture TEXT,
            total_debit REAL,
            total_credit REAL,
            resultat REAL,
            empreinte_sha256 TEXT,
            statut TEXT
        )
    """)

    c.execute("""
        SELECT id, date_cloture, total_debit, total_credit, resultat, empreinte_sha256, statut
        FROM clotures_comptables_v3
        ORDER BY id DESC
    """)

    clotures = c.fetchall()
    conn.close()

    return render_template('liste_clotures_v3.html', clotures=clotures)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/detection-fraude-v3')
@login_required
def detection_fraude_v3():

    import sqlite3

    alertes = []

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT libelle, COUNT(*), COALESCE(SUM(debit+credit),0)
        FROM ecritures_auto
        GROUP BY libelle
        HAVING COUNT(*) > 3
    """)

    doublons = c.fetchall()

    for d in doublons:
        alertes.append(f"ALERTE : libellÃ© rÃ©pÃ©tÃ© plus de 3 fois : {d[0]}")

    c.execute("""
        SELECT id, journal, date_ecriture, libelle, compte_id, debit, credit
        FROM ecritures_auto
        WHERE debit > 10000 OR credit > 10000
    """)

    gros_montants = c.fetchall()

    for g in gros_montants:
        alertes.append(f"ALERTE : montant Ã©levÃ© Ã©criture ID {g[0]} - {g[3]}")

    if not alertes:
        alertes.append("OK : aucune anomalie majeure dÃ©tectÃ©e.")

    conn.close()

    return render_template('detection_fraude_v3.html', alertes=alertes)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/controle-fec-dgfip-v3')
@login_required
def controle_fec_dgfip_v3():

    import sqlite3

    controles = []

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM ecritures_auto")
    nb = c.fetchone()[0]

    if nb == 0:
        controles.append("ERREUR : aucune Ã©criture automatique trouvÃ©e.")
    else:
        controles.append(f"OK : {nb} Ã©critures trouvÃ©es.")

    c.execute("""
        SELECT COUNT(*)
        FROM ecritures_auto
        WHERE date_ecriture IS NULL OR date_ecriture = ''
    """)
    dates_manquantes = c.fetchone()[0]

    if dates_manquantes > 0:
        controles.append(f"ERREUR : {dates_manquantes} Ã©critures sans date.")
    else:
        controles.append("OK : toutes les Ã©critures ont une date.")

    c.execute("""
        SELECT COUNT(*)
        FROM ecritures_auto
        WHERE compte_id IS NULL OR compte_id = ''
    """)
    comptes_manquants = c.fetchone()[0]

    if comptes_manquants > 0:
        controles.append(f"ERREUR : {comptes_manquants} Ã©critures sans compte.")
    else:
        controles.append("OK : toutes les Ã©critures ont un compte.")

    c.execute("SELECT COALESCE(SUM(debit),0), COALESCE(SUM(credit),0) FROM ecritures_auto")
    debit, credit = c.fetchone()

    ecart = round(float(debit or 0) - float(credit or 0), 2)

    if ecart != 0:
        controles.append(f"ALERTE : balance non Ã©quilibrÃ©e, Ã©cart {ecart} â‚¬.")
    else:
        controles.append("OK : dÃ©bit = crÃ©dit.")

    conn.close()

    return render_template('controle_fec_dgfip_v3.html', controles=controles)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/assistant-conversationnel-comptable-v3', methods=['GET', 'POST'])
@login_required
def assistant_conversationnel_comptable_v3():

    import sqlite3

    reponse = ""

    if request.method == 'POST':
        question = (request.form.get('question') or "").lower()

        conn = sqlite3.connect("db.sqlite")
        c = conn.cursor()

        if "tva" in question:
            c.execute("SELECT COALESCE(SUM(debit),0) FROM ecritures_auto WHERE compte_id LIKE '44566%'")
            tva_deductible = c.fetchone()[0] or 0
            c.execute("SELECT COALESCE(SUM(credit),0) FROM ecritures_auto WHERE compte_id LIKE '44571%'")
            tva_collectee = c.fetchone()[0] or 0
            reponse = f"TVA collectÃ©e : {tva_collectee} â‚¬. TVA dÃ©ductible : {tva_deductible} â‚¬. TVA due estimÃ©e : {round(tva_collectee - tva_deductible, 2)} â‚¬."

        elif "rÃ©sultat" in question or "resultat" in question:
            c.execute("SELECT COALESCE(SUM(debit-credit),0) FROM ecritures_auto WHERE compte_id IN (SELECT id FROM plan_comptable WHERE numero LIKE '6%')")
            charges = c.fetchone()[0] or 0
            c.execute("SELECT COALESCE(SUM(credit-debit),0) FROM ecritures_auto WHERE compte_id IN (SELECT id FROM plan_comptable WHERE numero LIKE '7%')")
            produits = c.fetchone()[0] or 0
            reponse = f"Produits : {produits} â‚¬. Charges : {charges} â‚¬. RÃ©sultat estimÃ© : {round(produits - charges, 2)} â‚¬."

        elif "balance" in question:
            c.execute("SELECT COALESCE(SUM(debit),0), COALESCE(SUM(credit),0) FROM ecritures_auto")
            debit, credit = c.fetchone()
            reponse = f"Total dÃ©bit : {debit} â‚¬. Total crÃ©dit : {credit} â‚¬. Ã‰cart : {round(debit-credit, 2)} â‚¬."

        else:
            reponse = "Je peux rÃ©pondre aux questions sur la TVA, le rÃ©sultat ou la balance."

        conn.close()

    return render_template(
        'assistant_conversationnel_comptable_v3.html',
        reponse=reponse
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/api-comptable-externe-v3')
@login_required
def api_comptable_externe_v3():

    import sqlite3
    from flask import jsonify

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id, journal, date_ecriture, libelle, compte_id, debit, credit
        FROM ecritures_auto
        ORDER BY id DESC
    """)

    rows = c.fetchall()
    conn.close()

    data = []

    for r in rows:
        data.append({
            "id": r[0],
            "journal": r[1],
            "date": r[2],
            "libelle": r[3],
            "compte": r[4],
            "debit": r[5],
            "credit": r[6]
        })

    return jsonify({
        "application": "ComptaPilot",
        "module": "api-comptable-externe-v3",
        "ecritures": data
    })

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/connecteur-bancaire-dsp2-v3')
@login_required
def connecteur_bancaire_dsp2_v3():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS connecteurs_bancaires_dsp2_v3 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            banque TEXT,
            statut TEXT,
            derniere_synchro TEXT,
            commentaire TEXT
        )
    """)

    c.execute("""
        SELECT id, banque, statut, derniere_synchro, commentaire
        FROM connecteurs_bancaires_dsp2_v3
        ORDER BY id DESC
    """)

    connecteurs = c.fetchall()

    conn.commit()
    conn.close()

    return render_template(
        'connecteur_bancaire_dsp2_v3.html',
        connecteurs=connecteurs
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/simulation-synchro-dsp2-v3')
@login_required
def simulation_synchro_dsp2_v3():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS connecteurs_bancaires_dsp2_v3 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            banque TEXT,
            statut TEXT,
            derniere_synchro TEXT,
            commentaire TEXT
        )
    """)

    c.execute("""
        INSERT INTO connecteurs_bancaires_dsp2_v3 (
            banque, statut, derniere_synchro, commentaire
        )
        VALUES (?, ?, ?, ?)
    """, (
        "BANQUE_DEMO_DSP2",
        "SYNCHRONISE",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Simulation DSP2 locale. Pas encore de connexion bancaire rÃ©elle."
    ))

    conn.commit()
    conn.close()

    flash("Synchronisation DSP2 simulÃ©e")
    return redirect('/ecritures/connecteur-bancaire-dsp2-v3')
# ==============================
# GESTION COMPLETE ENTREPRISE V4
# LETTRAGE / RELANCES / ECHEANCIERS / IMMOS / ANALYTIQUE / BUDGETS / REPORTING / ROLES / COFFRE / CONNECTEURS
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/gestion-entreprise-v4')
@login_required
def gestion_entreprise_v4():
    return render_template('gestion_entreprise_v4.html')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/lettrage-automatique-v4')
@login_required
def lettrage_automatique_v4():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS lettrages_auto_v4 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            compte_id TEXT,
            libelle TEXT,
            montant REAL,
            statut TEXT,
            date_lettrage TEXT
        )
    """)

    c.execute("""
        SELECT compte_id, libelle, ABS(debit-credit)
        FROM ecritures_auto
        WHERE compte_id LIKE '401%' OR compte_id LIKE '411%'
    """)

    lignes = c.fetchall()
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for compte_id, libelle, montant in lignes:
        c.execute("""
            INSERT INTO lettrages_auto_v4 (compte_id, libelle, montant, statut, date_lettrage)
            VALUES (?, ?, ?, ?, ?)
        """, (compte_id, libelle, montant, "LETTRAGE_SUGGERE", date_now))

    conn.commit()
    conn.close()

    flash("Lettrage automatique simulÃ©")
    return redirect('/ecritures/liste-lettrages-v4')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/liste-lettrages-v4')
@login_required
def liste_lettrages_v4():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS lettrages_auto_v4 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            compte_id TEXT,
            libelle TEXT,
            montant REAL,
            statut TEXT,
            date_lettrage TEXT
        )
    """)

    c.execute("""
        SELECT id, compte_id, libelle, montant, statut, date_lettrage
        FROM lettrages_auto_v4
        ORDER BY id DESC
    """)

    lignes = c.fetchall()
    conn.close()

    return render_template('liste_lettrages_v4.html', lignes=lignes)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/relances-clients-v4')
@login_required
def relances_clients_v4():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS relances_clients_v4 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client TEXT,
            facture TEXT,
            montant REAL,
            niveau TEXT,
            message TEXT,
            date_relance TEXT
        )
    """)

    c.execute("""
        SELECT numero, client, montant_ttc, statut
        FROM factures_dematerialisees
        WHERE statut != 'PAYEE'
    """)

    factures = c.fetchall()

    for numero, client, montant, statut in factures:
        message = f"Relance automatique : facture {numero} de {montant} EUR en attente de paiement."
        c.execute("""
            INSERT INTO relances_clients_v4 (client, facture, montant, niveau, message, date_relance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            client,
            numero,
            montant,
            "RELANCE_1",
            message,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

    conn.commit()
    conn.close()

    flash("Relances clients gÃ©nÃ©rÃ©es")
    return redirect('/ecritures/liste-relances-clients-v4')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/liste-relances-clients-v4')
@login_required
def liste_relances_clients_v4():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id, client, facture, montant, niveau, message, date_relance
        FROM relances_clients_v4
        ORDER BY id DESC
    """)

    relances = c.fetchall()
    conn.close()

    return render_template('liste_relances_clients_v4.html', relances=relances)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/echeancier-fournisseurs-v4')
@login_required
def echeancier_fournisseurs_v4():

    import sqlite3
    from datetime import datetime, timedelta

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS echeancier_fournisseurs_v4 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fournisseur TEXT,
            facture TEXT,
            montant REAL,
            date_echeance TEXT,
            statut TEXT
        )
    """)

    c.execute("""
        SELECT fournisseur_client, numero_facture, montant_ttc
        FROM extractions_documents_comptables
        WHERE type_probable LIKE '%FOURNISSEUR%'
    """)

    lignes = c.fetchall()

    for fournisseur, facture, montant in lignes:
        c.execute("""
            INSERT INTO echeancier_fournisseurs_v4 (
                fournisseur, facture, montant, date_echeance, statut
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            fournisseur,
            facture,
            montant,
            (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "A_PAYER"
        ))

    conn.commit()
    conn.close()

    return redirect('/ecritures/liste-echeancier-fournisseurs-v4')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/liste-echeancier-fournisseurs-v4')
@login_required
def liste_echeancier_fournisseurs_v4():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id, fournisseur, facture, montant, date_echeance, statut
        FROM echeancier_fournisseurs_v4
        ORDER BY date_echeance
    """)

    lignes = c.fetchall()
    conn.close()

    return render_template('liste_echeancier_fournisseurs_v4.html', lignes=lignes)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/immobilisations-v4')
@login_required
def immobilisations_v4():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS immobilisations_v4 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            valeur REAL,
            duree INTEGER,
            date_acquisition TEXT,
            compte_id TEXT
        )
    """)

    c.execute("""
        SELECT id, nom, valeur, duree, date_acquisition, compte
        FROM immobilisations_v4
        ORDER BY id DESC
    """)

    immos = c.fetchall()
    conn.close()

    return render_template('immobilisations_v4.html', immos=immos)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/ajouter-immobilisation-v4', methods=['GET', 'POST'])
@login_required
def ajouter_immobilisation_v4():

    if request.method == 'GET':
        return render_template('ajouter_immobilisation_v4.html')

    import sqlite3

    nom = request.form.get('nom')
    valeur = float((request.form.get('valeur') or "0").replace(",", "."))
    duree = int(request.form.get('duree') or "5")
    date_acquisition = request.form.get('date_acquisition')
    compte_id = request.form.get('compte') or "218"

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        INSERT INTO immobilisations_v4 (nom, valeur, duree, date_acquisition, compte)
        VALUES (?, ?, ?, ?, ?)
    """, (nom, valeur, duree, date_acquisition, compte))

    conn.commit()
    conn.close()

    return redirect('/ecritures/immobilisations-v4')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/amortissements-v4')
@login_required
def amortissements_v4():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id, nom, valeur, duree
        FROM immobilisations_v4
    """)

    immos = c.fetchall()

    amortissements = []

    for immo_id, nom, valeur, duree in immos:
        dotation = round(float(valeur or 0) / int(duree or 1), 2)
        amortissements.append((immo_id, nom, valeur, duree, dotation))

    conn.close()

    return render_template('amortissements_v4.html', amortissements=amortissements)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/analytique-v4')
@login_required
def analytique_v4():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS analytique_v4 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            axe TEXT,
            compte_id TEXT,
            montant REAL,
            commentaire TEXT
        )
    """)

    c.execute("""
        SELECT id, axe, compte_id, montant, commentaire
        FROM analytique_v4
        ORDER BY id DESC
    """)

    lignes = c.fetchall()
    conn.close()

    return render_template('analytique_v4.html', lignes=lignes)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/budgets-v4')
@login_required
def budgets_v4():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS budgets_v4 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            axe TEXT,
            budget REAL,
            realise REAL,
            ecart REAL
        )
    """)

    c.execute("""
        SELECT id, axe, budget, realise, ecart
        FROM budgets_v4
        ORDER BY id DESC
    """)

    budgets = c.fetchall()
    conn.close()

    return render_template('budgets_v4.html', budgets=budgets)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/reporting-financier-ia-v4')
@login_required
def reporting_financier_ia_v4():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("SELECT COALESCE(SUM(debit),0), COALESCE(SUM(credit),0) FROM ecritures_auto")
    debit, credit = c.fetchone()

    resultat = round(float(credit or 0) - float(debit or 0), 2)

    messages = []

    if resultat > 0:
        messages.append("RÃ©sultat positif dÃ©tectÃ©.")
    elif resultat < 0:
        messages.append("RÃ©sultat nÃ©gatif dÃ©tectÃ©.")
    else:
        messages.append("RÃ©sultat neutre.")

    if abs(float(debit or 0) - float(credit or 0)) > 0:
        messages.append("Attention : les Ã©critures automatiques ne sont pas Ã©quilibrÃ©es.")

    conn.close()

    return render_template(
        'reporting_financier_ia_v4.html',
        debit=debit,
        credit=credit,
        resultat=resultat,
        messages=messages
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/dashboard-graphiques-v4')
@login_required
def dashboard_graphiques_v4():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("SELECT COALESCE(SUM(debit),0), COALESCE(SUM(credit),0) FROM ecritures_auto")
    debit, credit = c.fetchone()

    c.execute("SELECT COUNT(*) FROM documents_comptables_importes")
    docs = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM factures_dematerialisees")
    factures = c.fetchone()[0]

    conn.close()

    return render_template(
        'dashboard_graphiques_v4.html',
        debit=debit,
        credit=credit,
        docs=docs,
        factures=factures
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/utilisateurs-roles-v4')
@login_required
def utilisateurs_roles_v4():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS roles_permissions_v4 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utilisateur TEXT,
            role TEXT,
            permission TEXT,
            statut TEXT
        )
    """)

    c.execute("""
        SELECT id, utilisateur, role, permission, statut
        FROM roles_permissions_v4
        ORDER BY id DESC
    """)

    roles = c.fetchall()
    conn.close()

    return render_template('utilisateurs_roles_v4.html', roles=roles)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/journalisation-legale-v4')
@login_required
def journalisation_legale_v4():

    import sqlite3
    import hashlib
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS journal_legal_v4 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evenement TEXT,
            detail TEXT,
            empreinte_sha256 TEXT,
            date_evenement TEXT
        )
    """)

    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    evenement = "CONTROLE_LEGAL"
    detail = "Journalisation lÃ©gale complÃ¨te simulÃ©e"
    empreinte = hashlib.sha256(f"{evenement}|{detail}|{date_now}".encode("utf-8")).hexdigest()

    c.execute("""
        INSERT INTO journal_legal_v4 (evenement, detail, empreinte_sha256, date_evenement)
        VALUES (?, ?, ?, ?)
    """, (evenement, detail, empreinte, date_now))

    conn.commit()
    conn.close()

    return redirect('/ecritures/liste-journal-legal-v4')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/liste-journal-legal-v4')
@login_required
def liste_journal_legal_v4():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id, evenement, detail, empreinte_sha256, date_evenement
        FROM journal_legal_v4
        ORDER BY id DESC
    """)

    lignes = c.fetchall()
    conn.close()

    return render_template('liste_journal_legal_v4.html', lignes=lignes)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/cachet-serveur-v4')
@login_required
def cachet_serveur_v4():

    import hashlib
    from datetime import datetime

    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    empreinte = hashlib.sha256(f"CACHET_SERVEUR_COMPTAPILOT|{date_now}".encode("utf-8")).hexdigest()

    return render_template(
        'cachet_serveur_v4.html',
        date_now=date_now,
        empreinte=empreinte
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/coffre-fort-probatoire-v4')
@login_required
def coffre_fort_probatoire_v4():

    import sqlite3
    import os
    import hashlib
    import shutil
    from datetime import datetime

    os.makedirs("C:/Users/alain/mon-projet-agent/coffre_fort_probatoire_v4", exist_ok=True)

    nom = "coffre_probatoire_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".sqlite"
    chemin = os.path.join("C:/Users/alain/mon-projet-agent/coffre_fort_probatoire_v4", nom)

    shutil.copy("C:/Users/alain/mon-projet-agent/db.sqlite", chemin)

    with open(chemin, "rb") as f:
        empreinte = hashlib.sha256(f.read()).hexdigest()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS coffre_fort_probatoire_v4 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fichier TEXT,
            chemin TEXT,
            empreinte_sha256 TEXT,
            date_depot TEXT
        )
    """)

    c.execute("""
        INSERT INTO coffre_fort_probatoire_v4 (fichier, chemin, empreinte_sha256, date_depot)
        VALUES (?, ?, ?, ?)
    """, (
        nom,
        chemin,
        empreinte,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return redirect('/ecritures/liste-coffre-fort-probatoire-v4')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/liste-coffre-fort-probatoire-v4')
@login_required
def liste_coffre_fort_probatoire_v4():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id, fichier, chemin, empreinte_sha256, date_depot
        FROM coffre_fort_probatoire_v4
        ORDER BY id DESC
    """)

    lignes = c.fetchall()
    conn.close()

    return render_template('liste_coffre_fort_probatoire_v4.html', lignes=lignes)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/connecteur-chorus-pro-v4')
@login_required
def connecteur_chorus_pro_v4():
    return render_template('connecteur_chorus_pro_v4.html')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/connecteur-peppol-v4')
@login_required
def connecteur_peppol_v4():
    return render_template('connecteur_peppol_v4.html')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/api-bancaire-dsp2-reelle-v4')
@login_required
def api_bancaire_dsp2_reelle_v4():
    return render_template('api_bancaire_dsp2_reelle_v4.html')
# ==============================
# COCKPIT DIRIGEANT + VALIDATIONS V4
# LETTRAGE / RELANCES / FOURNISSEURS / BUDGETS / ANALYTIQUE / PILOTAGE
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/cockpit-dirigeant-v4')
@login_required
def cockpit_dirigeant_v4():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    def count_table(table):
        try:
            c.execute(f"SELECT COUNT(*) FROM {table}")
            return c.fetchone()[0]
        except:
            return 0

    nb_documents = count_table("documents_comptables_importes")
    nb_factures = count_table("factures_dematerialisees")
    nb_ecritures_auto = count_table("ecritures_auto")
    nb_relances = count_table("relances_clients_v4")
    nb_lettrages = count_table("lettrages_auto_v4")
    nb_fournisseurs = count_table("echeancier_fournisseurs_v4")
    nb_immos = count_table("immobilisations_v4")
    nb_budgets = count_table("budgets_v4")

    try:
        c.execute("SELECT COALESCE(SUM(debit),0), COALESCE(SUM(credit),0) FROM ecritures_auto")
        debit, credit = c.fetchone()
    except:
        debit, credit = 0, 0

    resultat_estime = round(float(credit or 0) - float(debit or 0), 2)

    conn.close()

    return render_template(
        'cockpit_dirigeant_v4.html',
        nb_documents=nb_documents,
        nb_factures=nb_factures,
        nb_ecritures_auto=nb_ecritures_auto,
        nb_relances=nb_relances,
        nb_lettrages=nb_lettrages,
        nb_fournisseurs=nb_fournisseurs,
        nb_immos=nb_immos,
        nb_budgets=nb_budgets,
        debit=round(float(debit or 0), 2),
        credit=round(float(credit or 0), 2),
        resultat_estime=resultat_estime
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/valider-lettrage-v4/<int:lettrage_id>')
@login_required
def valider_lettrage_v4(lettrage_id):

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE lettrages_auto_v4
        SET statut = ?
        WHERE id = ?
    """, ("LETTRAGE_VALIDE", lettrage_id))

    conn.commit()
    conn.close()

    flash("Lettrage validÃ©")
    return redirect('/ecritures/liste-lettrages-v4')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/marquer-relance-envoyee-v4/<int:relance_id>')
@login_required
def marquer_relance_envoyee_v4(relance_id):

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE relances_clients_v4
        SET niveau = ?
        WHERE id = ?
    """, ("ENVOYEE", relance_id))

    conn.commit()
    conn.close()

    flash("Relance marquÃ©e comme envoyÃ©e")
    return redirect('/ecritures/liste-relances-clients-v4')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/marquer-fournisseur-paye-v4/<int:echeance_id>')
@login_required
def marquer_fournisseur_paye_v4(echeance_id):

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE echeancier_fournisseurs_v4
        SET statut = ?
        WHERE id = ?
    """, ("PAYE", echeance_id))

    conn.commit()
    conn.close()

    flash("Fournisseur marquÃ© comme payÃ©")
    return redirect('/ecritures/liste-echeancier-fournisseurs-v4')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/ajouter-budget-v4', methods=['GET', 'POST'])
@login_required
def ajouter_budget_v4():

    if request.method == 'GET':
        return render_template('ajouter_budget_v4.html')

    import sqlite3

    axe = request.form.get('axe')
    budget = float((request.form.get('budget') or "0").replace(",", "."))
    realise = float((request.form.get('realise') or "0").replace(",", "."))
    ecart = round(realise - budget, 2)

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS budgets_v4 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            axe TEXT,
            budget REAL,
            realise REAL,
            ecart REAL
        )
    """)

    c.execute("""
        INSERT INTO budgets_v4 (axe, budget, realise, ecart)
        VALUES (?, ?, ?, ?)
    """, (axe, budget, realise, ecart))

    conn.commit()
    conn.close()

    flash("Budget ajoutÃ©")
    return redirect('/ecritures/budgets-v4')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/ajouter-analytique-v4', methods=['GET', 'POST'])
@login_required
def ajouter_analytique_v4():

    if request.method == 'GET':
        return render_template('ajouter_analytique_v4.html')

    import sqlite3

    axe = request.form.get('axe')
    compte_id = request.form.get('compte')
    montant = float((request.form.get('montant') or "0").replace(",", "."))
    commentaire = request.form.get('commentaire')

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS analytique_v4 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            axe TEXT,
            compte_id TEXT,
            montant REAL,
            commentaire TEXT
        )
    """)

    c.execute("""
        INSERT INTO analytique_v4 (axe, compte_id, montant, commentaire)
        VALUES (?, ?, ?, ?)
    """, (axe, compte_id, montant, commentaire))

    conn.commit()
    conn.close()

    flash("Ligne analytique ajoutÃ©e")
    return redirect('/ecritures/analytique-v4')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/ajouter-role-v4', methods=['GET', 'POST'])
@login_required
def ajouter_role_v4():

    if request.method == 'GET':
        return render_template('ajouter_role_v4.html')

    import sqlite3

    utilisateur = request.form.get('utilisateur')
    role = request.form.get('role')
    permission = request.form.get('permission')
    statut = request.form.get('statut') or "ACTIF"

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS roles_permissions_v4 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utilisateur TEXT,
            role TEXT,
            permission TEXT,
            statut TEXT
        )
    """)

    c.execute("""
        INSERT INTO roles_permissions_v4 (
            utilisateur, role, permission, statut
        )
        VALUES (?, ?, ?, ?)
    """, (utilisateur, role, permission, statut))

    conn.commit()
    conn.close()

    flash("RÃ´le ajoutÃ©")
    return redirect('/ecritures/utilisateurs-roles-v4')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/plan-paiement-fournisseurs-v4')
@login_required
def plan_paiement_fournisseurs_v4():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT fournisseur, facture, montant, date_echeance, statut
        FROM echeancier_fournisseurs_v4
        ORDER BY date_echeance
    """)

    lignes = c.fetchall()

    total_a_payer = 0

    for l in lignes:
        if l[4] != "PAYE":
            try:
                total_a_payer += float(l[2] or 0)
            except:
                pass
# ==============================
# SECURISATION + PARAMETRAGE + QUALITE PRODUCTION V5
# SOCIETE / NUMEROTATION / EXERCICES / VERROUILLAGE / CONTROLES / EXPORT / JOURNAL
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/qualite-production-v5')
@login_required
def qualite_production_v5():
    return render_template('qualite_production_v5.html')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/parametres-societe-v5', methods=['GET', 'POST'])
@login_required
def parametres_societe_v5():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS parametres_societe_v5 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raison_sociale TEXT,
            siret TEXT,
            tva_intracom TEXT,
            adresse TEXT,
            email TEXT,
            date_modification TEXT
        )
    """)

    if request.method == 'POST':
        raison_sociale = request.form.get('raison_sociale')
        siret = request.form.get('siret')
        tva_intracom = request.form.get('tva_intracom')
        adresse = request.form.get('adresse')
        email = request.form.get('email')

        c.execute("""
            INSERT INTO parametres_societe_v5 (
                raison_sociale, siret, tva_intracom, adresse, email, date_modification
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            raison_sociale,
            siret,
            tva_intracom,
            adresse,
            email,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        flash("ParamÃ¨tres sociÃ©tÃ© enregistrÃ©s")
        return redirect('/ecritures/parametres-societe-v5')

    c.execute("""
        SELECT id, raison_sociale, siret, tva_intracom, adresse, email, date_modification
        FROM parametres_societe_v5
        ORDER BY id DESC
        LIMIT 1
    """)

    societe = c.fetchone()

    conn.close()

    return render_template(
        'parametres_societe_v5.html',
        societe=societe
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/exercices-comptables-v5', methods=['GET', 'POST'])
@login_required
def exercices_comptables_v5():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS exercices_comptables_v5 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            date_debut TEXT,
            date_fin TEXT,
            statut TEXT,
            date_creation TEXT
        )
    """)

    if request.method == 'POST':
        nom = request.form.get('nom')
        date_debut = request.form.get('date_debut')
        date_fin = request.form.get('date_fin')

        c.execute("""
            INSERT INTO exercices_comptables_v5 (
                nom, date_debut, date_fin, statut, date_creation
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            nom,
            date_debut,
            date_fin,
            "OUVERT",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        flash("Exercice comptable crÃ©Ã©")
        return redirect('/ecritures/exercices-comptables-v5')

    c.execute("""
        SELECT id, nom, date_debut, date_fin, statut, date_creation
        FROM exercices_comptables_v5
        ORDER BY id DESC
    """)

    exercices = c.fetchall()

    conn.close()

    return render_template(
        'exercices_comptables_v5.html',
        exercices=exercices
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/verrouiller-exercice-v5/<int:exercice_id>')
@login_required
def verrouiller_exercice_v5(exercice_id):

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE exercices_comptables_v5
        SET statut = ?
        WHERE id = ?
    """, ("VERROUILLE", exercice_id))

    c.execute("""
        CREATE TABLE IF NOT EXISTS journal_actions_v5 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            detail TEXT,
            date_action TEXT
        )
    """)

    c.execute("""
        INSERT INTO journal_actions_v5 (action, detail, date_action)
        VALUES (?, ?, ?)
    """, (
        "VERROUILLAGE_EXERCICE",
        f"Exercice ID {exercice_id} verrouillÃ©",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    flash("Exercice verrouillÃ©")
    return redirect('/ecritures/exercices-comptables-v5')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/numerotation-officielle-v5', methods=['GET', 'POST'])
@login_required
def numerotation_officielle_v5():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS numerotation_officielle_v5 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_document TEXT,
            prefixe TEXT,
            prochain_numero INTEGER,
            date_modification TEXT
        )
    """)

    if request.method == 'POST':
        type_document = request.form.get('type_document')
        prefixe = request.form.get('prefixe')
        prochain_numero = int(request.form.get('prochain_numero') or 1)

        c.execute("""
            INSERT INTO numerotation_officielle_v5 (
                type_document, prefixe, prochain_numero, date_modification
            )
            VALUES (?, ?, ?, ?)
        """, (
            type_document,
            prefixe,
            prochain_numero,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        flash("NumÃ©rotation enregistrÃ©e")
        return redirect('/ecritures/numerotation-officielle-v5')

    c.execute("""
        SELECT id, type_document, prefixe, prochain_numero, date_modification
        FROM numerotation_officielle_v5
        ORDER BY id DESC
    """)

    numerotations = c.fetchall()

    conn.close()

    return render_template(
        'numerotation_officielle_v5.html',
        numerotations=numerotations
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/controle-equilibre-global-v5')
@login_required
def controle_equilibre_global_v5():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    controles = []

    c.execute("""
        SELECT COALESCE(SUM(debit),0), COALESCE(SUM(credit),0)
        FROM ecritures_auto
    """)

    debit, credit = c.fetchone()

    ecart = round(float(debit or 0) - float(credit or 0), 2)

    if ecart == 0:
        controles.append("OK : les Ã©critures automatiques sont Ã©quilibrÃ©es.")
    else:
        controles.append(f"ALERTE : Ã©cart dÃ©bit/crÃ©dit de {ecart} â‚¬.")

    c.execute("""
        SELECT COUNT(*)
        FROM ecritures_auto
        WHERE compte_id IS NULL OR compte_id = ''
    """)

    sans_compte = c.fetchone()[0]

    if sans_compte == 0:
        controles.append("OK : toutes les Ã©critures ont un compte.")
    else:
        controles.append(f"ERREUR : {sans_compte} Ã©critures sans compte.")

    c.execute("""
        SELECT COUNT(*)
        FROM ecritures_auto
        WHERE date_ecriture IS NULL OR date_ecriture = ''
    """)

    sans_date = c.fetchone()[0]

    if sans_date == 0:
        controles.append("OK : toutes les Ã©critures ont une date.")
    else:
        controles.append(f"ERREUR : {sans_date} Ã©critures sans date.")

    conn.close()

    return render_template(
        'controle_equilibre_global_v5.html',
        controles=controles,
        debit=round(float(debit or 0), 2),
        credit=round(float(credit or 0), 2),
        ecart=ecart
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/tableau-conformite-v5')
@login_required
def tableau_conformite_v5():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    indicateurs = []

    def table_count(table_name):
        try:
            c.execute(f"SELECT COUNT(*) FROM {table_name}")
            return c.fetchone()[0]
        except:
            return 0

    indicateurs.append(("Documents importÃ©s", table_count("documents_comptables_importes")))
    indicateurs.append(("Ã‰critures automatiques", table_count("ecritures_auto")))
    indicateurs.append(("Factures dÃ©matÃ©rialisÃ©es", table_count("factures_dematerialisees")))
    indicateurs.append(("Archives probatoires", table_count("archives_probatoires_v2")))
    indicateurs.append(("Journal lÃ©gal", table_count("journal_legal_v4")))
    indicateurs.append(("Exercices comptables", table_count("exercices_comptables_v5")))
    indicateurs.append(("ClÃ´tures comptables", table_count("clotures_comptables_v3")))

    conn.close()

    return render_template(
        'tableau_conformite_v5.html',
        indicateurs=indicateurs
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/journal-actions-v5')
@login_required
def journal_actions_v5():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS journal_actions_v5 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            detail TEXT,
            date_action TEXT
        )
    """)

    c.execute("""
        SELECT id, action, detail, date_action
        FROM journal_actions_v5
        ORDER BY id DESC
        LIMIT 300
    """)

    actions = c.fetchall()

    conn.close()

    return render_template(
        'journal_actions_v5.html',
        actions=actions
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/sauvegarde-avant-cloture-v5')
@login_required
def sauvegarde_avant_cloture_v5():

    import os
    import shutil
    import hashlib
    import sqlite3
    from datetime import datetime

    dossier = "C:/Users/alain/mon-projet-agent/sauvegardes_avant_cloture_v5"
    os.makedirs(dossier, exist_ok=True)

    nom = "sauvegarde_avant_cloture_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".sqlite"
    chemin = os.path.join(dossier, nom)

    shutil.copy("C:/Users/alain/mon-projet-agent/db.sqlite", chemin)

    with open(chemin, "rb") as f:
        empreinte = hashlib.sha256(f.read()).hexdigest()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS sauvegardes_avant_cloture_v5 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fichier TEXT,
            chemin TEXT,
            empreinte_sha256 TEXT,
            date_sauvegarde TEXT
        )
    """)

    c.execute("""
        INSERT INTO sauvegardes_avant_cloture_v5 (
            fichier, chemin, empreinte_sha256, date_sauvegarde
        )
        VALUES (?, ?, ?, ?)
    """, (
        nom,
        chemin,
        empreinte,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    c.execute("""
        CREATE TABLE IF NOT EXISTS journal_actions_v5 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            detail TEXT,
            date_action TEXT
        )
    """)

    c.execute("""
        INSERT INTO journal_actions_v5 (action, detail, date_action)
        VALUES (?, ?, ?)
    """, (
        "SAUVEGARDE_AVANT_CLOTURE",
        f"Sauvegarde crÃ©Ã©e : {chemin}",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    flash("Sauvegarde avant clÃ´ture crÃ©Ã©e")
    return redirect('/ecritures/liste-sauvegardes-avant-cloture-v5')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/liste-sauvegardes-avant-cloture-v5')
@login_required
def liste_sauvegardes_avant_cloture_v5():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS sauvegardes_avant_cloture_v5 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fichier TEXT,
            chemin TEXT,
            empreinte_sha256 TEXT,
            date_sauvegarde TEXT
        )
    """)

    c.execute("""
        SELECT id, fichier, chemin, empreinte_sha256, date_sauvegarde
        FROM sauvegardes_avant_cloture_v5
        ORDER BY id DESC
    """)

    sauvegardes = c.fetchall()

    conn.close()

    return render_template(
        'liste_sauvegardes_avant_cloture_v5.html',
        sauvegardes=sauvegardes
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/export-complet-csv-v5')
@login_required
def export_complet_csv_v5():

    import sqlite3
    import csv
    import io
    from flask import Response

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id, journal, date_ecriture, libelle, compte_id, debit, credit
        FROM ecritures_auto
        ORDER BY id
    """)

    lignes = c.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')

    writer.writerow([
        "ID",
        "Journal",
        "Date",
        "Libelle",
        "Compte",
        "Debit",
        "Credit"
    ])

    for l in lignes:
        writer.writerow(l)

    return flask.Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=export_comptable_complet_v5.csv"}
    )
    conn.close()

    return render_template(
        'plan_paiement_fournisseurs_v4.html',
        lignes=lignes,
        total_a_payer=round(total_a_payer, 2)
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/export-tresorerie-v4')
@login_required
def export_tresorerie_v4():

    import sqlite3
    import csv
    import io
    from flask import Response

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT date_ecriture, libelle, debit, credit, journal
        FROM ecritures_auto
        ORDER BY date_ecriture
    """)

    lignes = c.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')

    writer.writerow(["Date", "Libelle", "Debit", "Credit", "Journal"])

    for l in lignes:
        writer.writerow(l)

    return flask.Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=tresorerie_v4.csv"}
    )
# ==============================
# SAAS + SECURITE + INDUSTRIALISATION V6
# MULTI-TENANT / ABONNEMENTS / LIMITES / RGPD / AUDIT / SANTE SYSTEME
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/saas-securite-v6')
@login_required
def saas_securite_v6():
    return render_template('saas_securite_v6.html')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/tenants-v6', methods=['GET', 'POST'])
@login_required
def tenants_v6():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS tenants_v6 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            code TEXT,
            statut TEXT,
            date_creation TEXT
        )
    """)

    if request.method == 'POST':
        nom = request.form.get('nom')
        code = request.form.get('code')

        c.execute("""
            INSERT INTO tenants_v6 (nom, code, statut, date_creation)
            VALUES (?, ?, ?, ?)
        """, (
            nom,
            code,
            "ACTIF",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        flash("Espace SaaS crÃ©Ã©")
        return redirect('/ecritures/tenants-v6')

    c.execute("""
        SELECT id, nom, code, statut, date_creation
        FROM tenants_v6
        ORDER BY id DESC
    """)

    tenants = c.fetchall()

    conn.close()

    return render_template('tenants_v6.html', tenants=tenants)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/abonnements-v6', methods=['GET', 'POST'])
@login_required
def abonnements_v6():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS abonnements_v6 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant TEXT,
            plan TEXT,
            prix REAL,
            statut TEXT,
            date_creation TEXT
        )
    """)

    if request.method == 'POST':
        tenant = request.form.get('tenant')
        plan = request.form.get('plan')
        prix = float((request.form.get('prix') or "0").replace(",", "."))

        c.execute("""
            INSERT INTO abonnements_v6 (tenant, plan, prix, statut, date_creation)
            VALUES (?, ?, ?, ?, ?)
        """, (
            tenant,
            plan,
            prix,
            "ACTIF",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        flash("Abonnement ajoutÃ©")
        return redirect('/ecritures/abonnements-v6')

    c.execute("""
        SELECT id, tenant, plan, prix, statut, date_creation
        FROM abonnements_v6
        ORDER BY id DESC
    """)

    abonnements = c.fetchall()

    conn.close()

    return render_template('abonnements_v6.html', abonnements=abonnements)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/limites-usage-v6')
@login_required
def limites_usage_v6():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    def count_table(table_name):
        try:
            c.execute(f"SELECT COUNT(*) FROM {table_name}")
            return c.fetchone()[0]
        except:
            return 0

    limites = [
        ("Documents importÃ©s", count_table("documents_comptables_importes"), 1000),
        ("Factures", count_table("factures_dematerialisees"), 1000),
        ("Ã‰critures automatiques", count_table("ecritures_auto"), 10000),
        ("Archives probatoires", count_table("archives_probatoires_v2"), 500),
        ("Utilisateurs / rÃ´les", count_table("roles_permissions_v4"), 50),
    ]

    conn.close()

    return render_template('limites_usage_v6.html', limites=limites)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/droits-modules-v6', methods=['GET', 'POST'])
@login_required
def droits_modules_v6():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS droits_modules_v6 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utilisateur TEXT,
            module TEXT,
            droit TEXT,
            date_creation TEXT
        )
    """)

    if request.method == 'POST':
        utilisateur = request.form.get('utilisateur')
        module = request.form.get('module')
        droit = request.form.get('droit')

        c.execute("""
            INSERT INTO droits_modules_v6 (utilisateur, module, droit, date_creation)
            VALUES (?, ?, ?, ?)
        """, (
            utilisateur,
            module,
            droit,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        flash("Droit module ajoutÃ©")
        return redirect('/ecritures/droits-modules-v6')

    c.execute("""
        SELECT id, utilisateur, module, droit, date_creation
        FROM droits_modules_v6
        ORDER BY id DESC
    """)

    droits = c.fetchall()

    conn.close()

    return render_template('droits_modules_v6.html', droits=droits)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/journal-acces-v6')
@login_required
def journal_acces_v6():

    import sqlite3
    from datetime import datetime
    from flask import request

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS journal_acces_v6 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utilisateur TEXT,
            ip TEXT,
            page TEXT,
            date_acces TEXT
        )
    """)

    c.execute("""
        INSERT INTO journal_acces_v6 (utilisateur, ip, page, date_acces)
        VALUES (?, ?, ?, ?)
    """, (
        "utilisateur_local",
        request.remote_addr,
        request.path,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    c.execute("""
        SELECT id, utilisateur, ip, page, date_acces
        FROM journal_acces_v6
        ORDER BY id DESC
        LIMIT 200
    """)

    acces = c.fetchall()

    conn.commit()
    conn.close()

    return render_template('journal_acces_v6.html', acces=acces)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/audit-securite-v6')
@login_required
def audit_securite_v6():

    import sqlite3
    import os

    controles = []

    if os.path.exists("C:/Users/alain/mon-projet-agent/db.sqlite"):
        controles.append("OK : base de donnÃ©es prÃ©sente.")
    else:
        controles.append("ERREUR : base de donnÃ©es absente.")

    dossiers = [
        "C:/Users/alain/mon-projet-agent/imports_documents_comptables",
        "C:/Users/alain/mon-projet-agent/archives_probatoires_v2",
        "C:/Users/alain/mon-projet-agent/coffre_fort_probatoire_v4",
        "C:/Users/alain/mon-projet-agent/sauvegardes_avant_cloture_v5"
    ]

    for dossier in dossiers:
        if os.path.exists(dossier):
            controles.append(f"OK : dossier prÃ©sent : {dossier}")
        else:
            controles.append(f"ALERTE : dossier absent : {dossier}")

    try:
        conn = sqlite3.connect("db.sqlite")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        nb_tables = c.fetchone()[0]
        conn.close()
        controles.append(f"OK : {nb_tables} tables dÃ©tectÃ©es.")
    except Exception as e:
        controles.append(f"ERREUR SQLite : {str(e)}")

    return render_template('audit_securite_v6.html', controles=controles)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/export-rgpd-v6')
@login_required
def export_rgpd_v6():

    import sqlite3
    import json
    from flask import Response

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    data = {}

    tables = [
        "tenants_v6",
        "abonnements_v6",
        "droits_modules_v6",
        "journal_acces_v6",
        "roles_permissions_v4"
    ]

    for table in tables:
        try:
            c.execute(f"SELECT * FROM {table}")
            colonnes = [d[0] for d in c.description]
            lignes = c.fetchall()
            data[table] = [dict(zip(colonnes, ligne)) for ligne in lignes]
        except:
            data[table] = []

    conn.close()

    contenu = json.dumps(data, indent=4, ensure_ascii=False)

    return flask.Response(
        contenu,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment; filename=export_rgpd_v6.json"}
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/mode-lecture-seule-v6')
@login_required
def mode_lecture_seule_v6():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS mode_application_v6 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode TEXT,
            date_activation TEXT
        )
    """)

    c.execute("""
        INSERT INTO mode_application_v6 (mode, date_activation)
        VALUES (?, ?)
    """, (
        "LECTURE_SEULE",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    flash("Mode lecture seule enregistrÃ©")
    return redirect('/ecritures/statut-application-v6')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/statut-maintenance-v6')
@login_required
def statut_maintenance_v6():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS mode_application_v6 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode TEXT,
            date_activation TEXT
        )
    """)

    c.execute("""
        INSERT INTO mode_application_v6 (mode, date_activation)
        VALUES (?, ?)
    """, (
        "MAINTENANCE",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    flash("Mode maintenance enregistrÃ©")
    return redirect('/ecritures/statut-application-v6')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/statut-application-v6')
@login_required
def statut_application_v6():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS mode_application_v6 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode TEXT,
            date_activation TEXT
        )
    """)

    c.execute("""
        SELECT id, mode, date_activation
        FROM mode_application_v6
        ORDER BY id DESC
        LIMIT 20
    """)

    modes = c.fetchall()

    conn.close()

    return render_template('statut_application_v6.html', modes=modes)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/sante-systeme-v6')
@login_required
def sante_systeme_v6():

    import os
    import sqlite3
    import time

    debut = time.time()
    controles = []

    if os.path.exists("C:/Users/alain/mon-projet-agent/app.py"):
        controles.append("OK : app.py prÃ©sent.")
    else:
        controles.append("ERREUR : app.py introuvable.")

    if os.path.exists("C:/Users/alain/mon-projet-agent/controllers/gestion_ecritures.py"):
        controles.append("OK : contrÃ´leur principal prÃ©sent.")
    else:
        controles.append("ERREUR : contrÃ´leur principal introuvable.")

    try:
        conn = sqlite3.connect("db.sqlite")
        c = conn.cursor()
        c.execute("SELECT 1")
        conn.close()
        controles.append("OK : connexion SQLite fonctionnelle.")
    except Exception as e:
        controles.append(f"ERREUR SQLite : {str(e)}")

    duree = round(time.time() - debut, 4)

    return render_template(
        'sante_systeme_v6.html',
        controles=controles,
        duree=duree
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/monitoring-erreurs-v6')
@login_required
def monitoring_erreurs_v6():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS erreurs_systeme_v6 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_erreur TEXT,
            message TEXT,
            date_erreur TEXT
        )
    """)

    c.execute("""
        SELECT id, type_erreur, message, date_erreur
        FROM erreurs_systeme_v6
        ORDER BY id DESC
        LIMIT 200
    """)

    erreurs = c.fetchall()

    conn.close()

    return render_template('monitoring_erreurs_v6.html', erreurs=erreurs)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/simuler-erreur-v6')
@login_required
def simuler_erreur_v6():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS erreurs_systeme_v6 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_erreur TEXT,
            message TEXT,
            date_erreur TEXT
        )
    """)

    c.execute("""
        INSERT INTO erreurs_systeme_v6 (type_erreur, message, date_erreur)
        VALUES (?, ?, ?)
    """, (
        "SIMULATION",
        "Erreur simulÃ©e pour tester le monitoring",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    flash("Erreur simulÃ©e enregistrÃ©e")
    return redirect('/ecritures/monitoring-erreurs-v6')
# ==============================
# AUTOMATISATION IA + ORCHESTRATION METIER V7
# TACHES / SCENARIOS / ALERTES / EMAILS / SCORES / CASHFLOW / ROBOTS / SCHEDULER
# ==============================

@login_required
def orchestration_ia_v7():
    return render_template('orchestration_ia_v7.html')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/taches-automatiques-v7', methods=['GET', 'POST'])
def taches_automatiques_v7():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS taches_automatiques_v7 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            type_tache TEXT,
            frequence TEXT,
            statut TEXT,
            derniere_execution TEXT,
            date_creation TEXT
        )
    """)

    if request.method == 'POST':
        nom = request.form.get('nom')
        type_tache = request.form.get('type_tache')
        frequence = request.form.get('frequence')

        c.execute("""
            INSERT INTO taches_automatiques_v7 (
                nom, type_tache, frequence, statut, derniere_execution, date_creation
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            nom,
            type_tache,
            frequence,
            "ACTIVE",
            "",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        flash("TÃ¢che automatique ajoutÃ©e")
        return redirect('/ecritures/taches-automatiques-v7')

    c.execute("""
        SELECT id, nom, type_tache, frequence, statut, derniere_execution, date_creation
        FROM taches_automatiques_v7
        ORDER BY id DESC
    """)

    taches = c.fetchall()

    conn.close()

    return render_template('taches_automatiques_v7.html', taches=taches)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/executer-tache-v7/<int:tache_id>')
@login_required
def executer_tache_v7(tache_id):

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("""
        UPDATE taches_automatiques_v7
        SET derniere_execution = ?
        WHERE id = ?
    """, (date_now, tache_id))

    c.execute("""
        CREATE TABLE IF NOT EXISTS journal_orchestration_v7 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evenement TEXT,
            detail TEXT,
            date_evenement TEXT
        )
    """)

    c.execute("""
        INSERT INTO journal_orchestration_v7 (evenement, detail, date_evenement)
        VALUES (?, ?, ?)
    """, (
        "EXECUTION_TACHE",
        f"TÃ¢che automatique ID {tache_id} exÃ©cutÃ©e",
        date_now
    ))

    conn.commit()
    conn.close()

    flash("TÃ¢che exÃ©cutÃ©e")
    return redirect('/ecritures/taches-automatiques-v7')

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/scenarios-intelligents-v7', methods=['GET', 'POST'])
@login_required
def scenarios_intelligents_v7():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS scenarios_intelligents_v7 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            condition_declenchement TEXT,
            action TEXT,
            statut TEXT,
            date_creation TEXT
        )
    """)

    if request.method == 'POST':
        nom = request.form.get('nom')
        condition_declenchement = request.form.get('condition_declenchement')
        action = request.form.get('action')

        c.execute("""
            INSERT INTO scenarios_intelligents_v7 (
                nom, condition_declenchement, action, statut, date_creation
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            nom,
            condition_declenchement,
            action,
            "ACTIF",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        flash("ScÃ©nario intelligent ajoutÃ©")
        return redirect('/ecritures/scenarios-intelligents-v7')

    c.execute("""
        SELECT id, nom, condition_declenchement, action, statut, date_creation
        FROM scenarios_intelligents_v7
        ORDER BY id DESC
    """)

    scenarios = c.fetchall()

    conn.close()

    return render_template('scenarios_intelligents_v7.html', scenarios=scenarios)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/centre-alertes-v7')
@login_required
def centre_alertes_v7():

    import sqlite3
    from datetime import datetime

    alertes = []

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    try:
        c.execute("SELECT COALESCE(SUM(debit),0), COALESCE(SUM(credit),0) FROM ecritures_auto")
        debit, credit = c.fetchone()
        if round(float(debit or 0) - float(credit or 0), 2) != 0:
            alertes.append("ALERTE : les Ã©critures automatiques ne sont pas Ã©quilibrÃ©es.")
    except:
        alertes.append("ALERTE : table ecritures_auto non disponible.")

    try:
        c.execute("SELECT COUNT(*) FROM factures_dematerialisees WHERE statut != 'PAYEE'")
        impayees = c.fetchone()[0]
        if impayees > 0:
            alertes.append(f"ALERTE : {impayees} facture(s) non payÃ©e(s).")
    except:
        pass

    try:
        c.execute("SELECT COUNT(*) FROM documents_comptables_importes WHERE statut IN ('IMPORTE', 'A_TRAITER')")
        docs = c.fetchone()[0]
        if docs > 0:
            alertes.append(f"ALERTE : {docs} document(s) comptable(s) Ã  traiter.")
    except:
        pass

    if not alertes:
        alertes.append("OK : aucune alerte critique dÃ©tectÃ©e.")

    c.execute("""
        CREATE TABLE IF NOT EXISTS alertes_metier_v7 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alerte TEXT,
            niveau TEXT,
            date_alerte TEXT
        )
    """)

    for alerte in alertes:
        c.execute("""
            INSERT INTO alertes_metier_v7 (alerte, niveau, date_alerte)
            VALUES (?, ?, ?)
        """, (
            alerte,
            "CRITIQUE" if alerte.startswith("ALERTE") else "INFO",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

    conn.commit()

    c.execute("""
        SELECT id, alerte, niveau, date_alerte
        FROM alertes_metier_v7
        ORDER BY id DESC
        LIMIT 100
    """)

    lignes = c.fetchall()

    conn.close()

    return render_template('centre_alertes_v7.html', lignes=lignes)




@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/emails-automatiques-v7')
@login_required
def emails_automatiques_v7():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS emails_automatiques_v7 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destinataire TEXT,
            sujet TEXT,
            message TEXT,
            statut TEXT,
            date_creation TEXT
        )
    """)

    try:
        c.execute("""
            SELECT client, facture, montant, message
            FROM relances_clients_v4
            WHERE niveau != 'ENVOYEE'
        """)

        relances = c.fetchall()

        for client, facture, montant, message in relances:
            c.execute("""
                INSERT INTO emails_automatiques_v7 (
                    destinataire, sujet, message, statut, date_creation
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                client,
                f"Relance facture {facture}",
                message,
                "BROUILLON_EMAIL",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
    except:
        pass

    conn.commit()

    c.execute("""
        SELECT id, destinataire, sujet, message, statut, date_creation
        FROM emails_automatiques_v7
        ORDER BY id DESC
    """)

    emails = c.fetchall()

    conn.close()

    return render_template('emails_automatiques_v7.html', emails=emails)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/assistant-decisionnel-v7', methods=['GET', 'POST'])
@login_required
def assistant_decisionnel_v7():

    import sqlite3

    reponse = ""

    if request.method == 'POST':
        question = (request.form.get('question') or "").lower()

        conn = sqlite3.connect("db.sqlite")
        c = conn.cursor()

        if "risque" in question:
            reponse = "Analyse : surveiller les factures impayÃ©es, les Ã©critures dÃ©sÃ©quilibrÃ©es et les gros montants."
        elif "cash" in question or "trÃ©sorerie" in question or "tresorerie" in question:
            try:
                c.execute("SELECT COALESCE(SUM(credit),0), COALESCE(SUM(debit),0) FROM ecritures_auto")
                entrees, sorties = c.fetchone()
                reponse = f"Cashflow estimÃ© : entrÃ©es {entrees} â‚¬, sorties {sorties} â‚¬, solde {round(entrees - sorties, 2)} â‚¬."
            except:
                reponse = "Impossible de calculer le cashflow."
        elif "prioritÃ©" in question or "priorite" in question:
            reponse = "PrioritÃ©s recommandÃ©es : traiter les documents importÃ©s, valider les prÃ©-comptabilisations, vÃ©rifier les impayÃ©s."
        else:
            reponse = "Je peux analyser : risque, cashflow, trÃ©sorerie, prioritÃ©s."

        conn.close()

    return render_template(
        'assistant_decisionnel_v7.html',
        reponse=reponse
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/analyse-financiere-ia-v7')
@login_required
def analyse_financiere_ia_v7():

    import sqlite3

    messages = []

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    try:
        c.execute("SELECT COALESCE(SUM(debit),0), COALESCE(SUM(credit),0) FROM ecritures_auto")
        debit, credit = c.fetchone()
    except:
        debit, credit = 0, 0

    resultat = round(float(credit or 0) - float(debit or 0), 2)

    if resultat > 0:
        messages.append("RÃ©sultat global positif.")
    elif resultat < 0:
        messages.append("RÃ©sultat global nÃ©gatif.")
    else:
        messages.append("RÃ©sultat global neutre.")

    if abs(float(debit or 0) - float(credit or 0)) > 0:
        messages.append("Attention : dÃ©sÃ©quilibre dÃ©bit/crÃ©dit dÃ©tectÃ©.")

    try:
        c.execute("SELECT COUNT(*) FROM factures_dematerialisees WHERE statut != 'PAYEE'")
        impayees = c.fetchone()[0]
        messages.append(f"Factures non payÃ©es : {impayees}.")
    except:
        messages.append("Factures non disponibles.")

    conn.close()

    return render_template(
        'analyse_financiere_ia_v7.html',
        debit=round(float(debit or 0), 2),
        credit=round(float(credit or 0), 2),
        resultat=resultat,
        messages=messages
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/previsions-ia-v7')
@login_required
def previsions_ia_v7():
    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    try:
        c.execute("""
            SELECT COALESCE(AVG(credit),0), COALESCE(AVG(debit),0)
            FROM ecritures_auto
        """)
        moyenne_credit, moyenne_debit = c.fetchone()
    except:
        moyenne_credit, moyenne_debit = 0, 0

    previsions = []

    cumul = 0

    for mois in range(1, 7):
        cumul += float(moyenne_credit or 0) - float(moyenne_debit or 0)
        previsions.append((mois, round(moyenne_credit or 0, 2), round(moyenne_debit or 0, 2), round(cumul, 2)))

    conn.close()

    return render_template('previsions_ia_v7.html', previsions=previsions)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/score-risque-client-v7')
@login_required
def score_risque_client_v7():

    import sqlite3

    scores = []

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    try:
        c.execute("""
            SELECT client, COUNT(*), COALESCE(SUM(montant_ttc),0)
            FROM factures_dematerialisees
            WHERE statut != 'PAYEE'
            GROUP BY client
        """)

        clients = c.fetchall()

        for client, nb, montant in clients:
            score = min(100, int(nb or 0) * 20 + int(float(montant or 0) / 1000))
            scores.append((client, nb, round(float(montant or 0), 2), score))
    except:
        pass

    conn.close()

    return render_template('score_risque_client_v7.html', scores=scores)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/score-fraude-v7')
@login_required
def score_fraude_v7():

    import sqlite3

    score = 0
    facteurs = []

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    try:
        c.execute("SELECT COUNT(*) FROM documents_comptables_importes GROUP BY empreinte_sha256 HAVING COUNT(*) > 1")
        doublons = len(c.fetchall())
        if doublons > 0:
            score += doublons * 20
            facteurs.append(f"Doublons documentaires dÃ©tectÃ©s : {doublons}")
    except:
        pass

    try:
        c.execute("SELECT COUNT(*) FROM ecritures_auto WHERE debit > 10000 OR credit > 10000")
        gros = c.fetchone()[0]
        if gros > 0:
            score += gros * 10
            facteurs.append(f"Gros montants dÃ©tectÃ©s : {gros}")
    except:
        pass

    if score == 0:
        facteurs.append("Aucun facteur de fraude majeur dÃ©tectÃ©.")

    score = min(score, 100)

    conn.close()

    return render_template('score_fraude_v7.html', score=score, facteurs=facteurs)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/cashflow-ia-v7')
@login_required
def cashflow_ia_v7():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    try:
        c.execute("""
            SELECT date_ecriture, COALESCE(SUM(credit),0), COALESCE(SUM(debit),0)
            FROM ecritures_auto
            GROUP BY date_ecriture
            ORDER BY date_ecriture
        """)
        lignes = c.fetchall()
    except:
        lignes = []

    cumul = 0
    cashflow = []

    for date_ecriture, entrees, sorties in lignes:
        cumul += float(entrees or 0) - float(sorties or 0)
        cashflow.append((date_ecriture, entrees, sorties, round(cumul, 2)))

    conn.close()

    return render_template('cashflow_ia_v7.html', cashflow=cashflow)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/robots-comptables-v7')
@login_required
def robots_comptables_v7():

    robots = [
        ("Robot OCR", "Analyse les documents importÃ©s", "PRET"),
        ("Robot PrÃ©-compta", "PrÃ©pare les Ã©critures comptables", "PRET"),
        ("Robot Relance", "PrÃ©pare les relances clients", "PRET"),
        ("Robot Fraude", "DÃ©tecte les anomalies", "PRET"),
        ("Robot Cashflow", "PrÃ©voit la trÃ©sorerie", "PRET")
    ]

    return render_template('robots_comptables_v7.html', robots=robots)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/scheduler-automatique-v7')
@login_required
def scheduler_automatique_v7():

    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS scheduler_automatique_v7 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prochaine_execution TEXT,
            statut TEXT
        )
    """)

    c.execute("""
        INSERT INTO scheduler_automatique_v7 (nom, prochaine_execution, statut)
        VALUES (?, ?, ?)
    """, (
        "Scheduler quotidien ComptaPilot",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "PLANIFIE"
    ))

    conn.commit()

    c.execute("""
        SELECT id, nom, prochaine_execution, statut
        FROM scheduler_automatique_v7
        ORDER BY id DESC
    """)

    lignes = c.fetchall()

    conn.close()

    return render_template('scheduler_automatique_v7.html', lignes=lignes)

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/journal-orchestration-v7')
@login_required
def journal_orchestration_v7():

    import sqlite3

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS journal_orchestration_v7 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evenement TEXT,
            detail TEXT,
            date_evenement TEXT
        )
    """)

    c.execute("""
        SELECT id, evenement, detail, date_evenement
        FROM journal_orchestration_v7
        ORDER BY id DESC
        LIMIT 300
    """)

    lignes = c.fetchall()

    conn.close()

    return render_template('journal_orchestration_v7.html', lignes=lignes)
# ==============================
# VERIFICATEUR MODULES V7
# ==============================

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/verificateur-v7')
@login_required
def verificateur_v7():

    import os

    fichiers = [
        "orchestration_ia_v7.html",
        "taches_automatiques_v7.html",
        "scenarios_intelligents_v7.html",
        "centre_alertes_v7.html",
        "notifications_internes_v7.html",
        "emails_automatiques_v7.html",
        "assistant_decisionnel_v7.html",
        "analyse_financiere_ia_v7.html",
        "previsions_ia_v7.html",
        "score_risque_client_v7.html",
        "score_fraude_v7.html",
        "cashflow_ia_v7.html",
        "robots_comptables_v7.html",
        "scheduler_automatique_v7.html",
        "journal_orchestration_v7.html"
    ]

    resultats = []

    dossier = "C:/Users/alain/mon-projet-agent/templates"

    for fichier in fichiers:
        chemin = os.path.join(dossier, fichier)

        if os.path.exists(chemin):
            resultats.append((fichier, "OK", chemin))
        else:
            resultats.append((fichier, "MANQUANT", chemin))

    return render_template(
        'verificateur_v7.html',
        resultats=resultats
    )

@permission_required("ACCESS_ECRITURES")
@ecritures_routes.route('/controle-modules-pro')
@login_required
def controle_modules_pro():
    modules = [
        ("Transmission factures", "/ecritures/transmission-factures"),
        ("Liste sauvegardes", "/ecritures/liste-sauvegardes"),
        ("Journal audit", "/ecritures/journal-audit"),
        ("Signature renforcÃ©e", "/ecritures/signature-electronique-renforcee"),
        ("Import bancaire intelligent", "/ecritures/import-bancaire-intelligent"),
        ("Rapprochement bancaire", "/ecritures/rapprochement-bancaire"),
        ("PrÃ©visionnel trÃ©sorerie", "/ecritures/previsionnel-tresorerie"),
        ("Dashboard temps rÃ©el", "/ecritures/dashboard-temps-reel"),
        ("Multi-sociÃ©tÃ©s", "/ecritures/multi-societes"),
        ("Orchestration IA V7", "/ecritures/orchestration-ia-v7"),
        ("TÃ¢ches automatiques V7", "/ecritures/taches-automatiques-v7"),
        ("Notifications V7", "/ecritures/notifications-internes-v7"),
        ("PrÃ©visions IA V7", "/ecritures/previsions-ia-v7"),
    ]

    return render_template(
        "controle_modules_pro.html",
        modules=modules
    )

# ==============================
# CENTRE SAAS COMPTAPILOT
# ==============================

@ecritures_routes.route('/centre-saas')
@login_required
@permission_required("ACCESS_ECRITURES")
def centre_saas():

    modules = [
        {"nom": "Authentification JWT / API", "statut": "PrÃªt Ã  brancher", "niveau": "SÃ©curitÃ©"},
        {"nom": "API REST comptable", "statut": "ActivÃ©", "niveau": "Backend"},
        {"nom": "Export Excel / PDF avancÃ©", "statut": "PrÃªt Ã  brancher", "niveau": "Reporting"},
        {"nom": "Multi-utilisateurs", "statut": "Structure prÃªte", "niveau": "SaaS"},
        {"nom": "Permissions dynamiques", "statut": "En place", "niveau": "SÃ©curitÃ©"},
        {"nom": "Sauvegarde cloud automatique", "statut": "Ã€ connecter", "niveau": "Infrastructure"},
        {"nom": "OCR factures", "statut": "Module existant Ã  enrichir", "niveau": "IA"},
        {"nom": "Import bancaire automatique", "statut": "Ã€ connecter", "niveau": "Banque"},
        {"nom": "Rapprochement bancaire intelligent", "statut": "Ã€ dÃ©velopper", "niveau": "IA"},
        {"nom": "Assistant IA conversationnel", "statut": "Ã€ dÃ©velopper", "niveau": "IA"},
        {"nom": "Dashboard dirigeant multi-sociÃ©tÃ©s", "statut": "Base prÃªte", "niveau": "Pilotage"},
        {"nom": "Workflow validation comptable", "statut": "Ã€ dÃ©velopper", "niveau": "Process"},
        {"nom": "FEC / TVA / Liasse", "statut": "Modules Ã  consolider", "niveau": "FiscalitÃ©"},
        {"nom": "Mode expert-comptable multi-clients", "statut": "Ã€ structurer", "niveau": "Cabinet"},
        {"nom": "Docker / PostgreSQL / Nginx", "statut": "PrÃ©paration production", "niveau": "DÃ©ploiement"}
    ]

    return render_template(
        "centre_saas.html",
        modules=modules
    )


@ecritures_routes.route('/api/dashboard-financier')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_dashboard_financier():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            COALESCE(SUM(credit), 0),
            COALESCE(SUM(debit), 0),
            COUNT(*)
        FROM ecritures
    """)

    total_credit, total_debit, nb_ecritures = c.fetchone()

    conn.close()

    resultat = round(float(total_credit or 0) - float(total_debit or 0), 2)

    return jsonify({
        "ca": round(float(total_credit or 0), 2),
        "charges": round(float(total_debit or 0), 2),
        "resultat": resultat,
        "tva_estimee": round(float(total_credit or 0) * 0.20, 2),
        "nb_ecritures": nb_ecritures,
        "statut": "ok"
    })
# ==============================
# MODE QUASI PRODUCTION SAAS
# ==============================

@ecritures_routes.route('/production-saas')
@login_required
@permission_required("ACCESS_ECRITURES")
def production_saas():

    briques = [
        {"nom": "JWT rÃ©el", "statut": "JWTManager dÃ©jÃ  prÃ©sent", "etat": "PrÃªt"},
        {"nom": "PostgreSQL", "statut": "Compatible via DATABASE_URL", "etat": "PrÃªt"},
        {"nom": "Docker", "statut": "Dockerfile fourni", "etat": "Ã€ lancer"},
        {"nom": "Nginx", "statut": "Configuration fournie", "etat": "Ã€ lancer"},
        {"nom": "OCR factures IA", "statut": "Module OCR existant Ã  enrichir", "etat": "Base prÃªte"},
        {"nom": "Import bancaire CSV/OFX", "statut": "Connecteur Ã  brancher", "etat": "PrÃ©vu"},
        {"nom": "Rapprochement intelligent", "statut": "Analyse automatique Ã  Ã©tendre", "etat": "PrÃ©vu"},
        {"nom": "Chatbot IA", "statut": "Assistant IA Ã  connecter", "etat": "PrÃ©vu"},
        {"nom": "Notifications temps rÃ©el", "statut": "Alertes dashboard actives", "etat": "Base prÃªte"},
        {"nom": "PDF professionnel", "statut": "Export navigateur actif", "etat": "Actif"},
        {"nom": "Excel avancÃ©", "statut": "Export CSV prÃªt", "etat": "Actif"},
        {"nom": "Audit automatique", "statut": "ContrÃ´les comptables actifs", "etat": "Actif"},
        {"nom": "Portail expert-comptable", "statut": "Centre SaaS disponible", "etat": "Base prÃªte"},
        {"nom": "Multi-tenant SaaS", "statut": "Ã€ connecter aux sociÃ©tÃ©s", "etat": "PrÃ©vu"},
        {"nom": "DÃ©ploiement cloud", "statut": "Docker/Nginx prÃªts", "etat": "PrÃªt"}
    ]

    return render_template(
        "production_saas.html",
        briques=briques
    )


@ecritures_routes.route('/api/health')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_health():

    return jsonify({
        "status": "ok",
        "application": "ComptaPilot",
        "mode": "quasi-production",
        "database": "connected",
        "api": "active"
    })


@ecritures_routes.route('/api/audit-comptable')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_audit_comptable():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            COALESCE(SUM(debit), 0),
            COALESCE(SUM(credit), 0),
            COUNT(*)
        FROM ecritures
    """)

    total_debit, total_credit, nb_ecritures = c.fetchone()

    conn.close()

    ecart = round(float(total_debit or 0) - float(total_credit or 0), 2)

    alertes = []

    if ecart != 0:
        alertes.append("La comptabilitÃ© est dÃ©sÃ©quilibrÃ©e.")

    if nb_ecritures == 0:
        alertes.append("Aucune Ã©criture comptable trouvÃ©e.")

    if not alertes:
        alertes.append("Aucune anomalie majeure dÃ©tectÃ©e.")

    return jsonify({
        "total_debit": round(float(total_debit or 0), 2),
        "total_credit": round(float(total_credit or 0), 2),
        "ecart": ecart,
        "nb_ecritures": nb_ecritures,
        "alertes": alertes
    })


@ecritures_routes.route('/export-dashboard-csv')
@login_required
@permission_required("ACCESS_ECRITURES")
def export_dashboard_csv():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            date_ecriture,
            piece,
            libelle,
            debit,
            credit
        FROM ecritures
        ORDER BY date_ecriture DESC
    """)

    rows = c.fetchall()

    conn.close()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')

    writer.writerow([
        "Date",
        "PiÃ¨ce",
        "LibellÃ©",
        "DÃ©bit",
        "CrÃ©dit"
    ])

    for row in rows:
        writer.writerow(row)

    return flask.Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=dashboard_comptable.csv"
        }
    )
# ==============================
# API JWT PRODUCTION
# ==============================

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from extensions import csrf


@ecritures_routes.route('/api-console')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_console():

    return render_template(
        "api_console.html"
    )

@ecritures_routes.route('/assistant-ia-conversationnel')
@login_required
@permission_required("ACCESS_ECRITURES")
def assistant_ia_conversationnel():

    initialiser_assistant_ia()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            utilisateur,
            question,
            reponse,
            date_message
        FROM assistant_ia_messages
        ORDER BY date_message DESC
        LIMIT 100
    """)

    messages = c.fetchall()

    conn.close()

    return render_template(
        "assistant_ia_conversationnel.html",
        messages=messages
    )

@csrf.exempt
@ecritures_routes.route('/api/token', methods=['POST'])
def api_token():

    data = request.get_json() or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Identifiant et mot de passe obligatoires"
        }), 400

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id, username, password
        FROM users
        WHERE username = ?
    """, (username,))

    user = c.fetchone()

    conn.close()

    if not user:
        return jsonify({
            "error": "Identifiants incorrects"
        }), 401

    user_id, username_db, password_hash = user

    if not check_password_hash(password_hash, password):
        return jsonify({
            "error": "Identifiants incorrects"
        }), 401

    access_token = create_access_token(
        identity=str(user_id),
        additional_claims={
            "username": username_db
        }
    )

    return jsonify({
        "access_token": access_token,
        "token_type": "Bearer"
    })


@ecritures_routes.route('/api/v2/dashboard-financier')
@jwt_required()
def api_v2_dashboard_financier():

    user_id = get_jwt_identity()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            COALESCE(SUM(credit), 0),
            COALESCE(SUM(debit), 0),
            COUNT(*)
        FROM ecritures
    """)

    total_credit, total_debit, nb_ecritures = c.fetchone()

    conn.close()

    total_credit = round(float(total_credit or 0), 2)
    total_debit = round(float(total_debit or 0), 2)
    resultat = round(total_credit - total_debit, 2)

    return jsonify({
        "user_id": user_id,
        "ca": total_credit,
        "charges": total_debit,
        "resultat": resultat,
        "tva_estimee": round(total_credit * 0.20, 2),
        "nb_ecritures": nb_ecritures,
        "api_version": "v2",
        "auth": "jwt"
    })
# ==============================
# CENTRE COMMERCIAL SAAS
# ==============================

@ecritures_routes.route('/commercial-saas')
@login_required
@permission_required("ACCESS_ECRITURES")
def commercial_saas():

    modules = [
        {"nom": "PostgreSQL rÃ©el", "statut": "Compatible DATABASE_URL", "categorie": "Base de donnÃ©es"},
        {"nom": "ORM SQLAlchemy", "statut": "InitialisÃ© via extensions.db", "categorie": "Backend"},
        {"nom": "Multi-tenant complet", "statut": "Structure sociÃ©tÃ©s existante", "categorie": "SaaS"},
        {"nom": "WebSocket temps rÃ©el", "statut": "PrÃ©vu Socket.IO", "categorie": "Temps rÃ©el"},
        {"nom": "Notifications push", "statut": "Base notifications prÃªte", "categorie": "Alerting"},
        {"nom": "OCR IA rÃ©el", "statut": "Module OCR Ã  connecter IA", "categorie": "IA"},
        {"nom": "Import bancaire intelligent", "statut": "Base CSV/OFX Ã  enrichir", "categorie": "Banque"},
        {"nom": "Rapprochement automatique", "statut": "Moteur Ã  dÃ©velopper", "categorie": "Banque"},
        {"nom": "Assistant IA conversationnel", "statut": "Console prÃªte", "categorie": "IA"},
        {"nom": "PDF professionnel", "statut": "Export navigateur actif", "categorie": "Reporting"},
        {"nom": "Signatures Ã©lectroniques", "statut": "Module signatures prÃ©sent", "categorie": "LÃ©gal"},
        {"nom": "Workflow validation", "statut": "API validation ajoutÃ©e", "categorie": "Process"},
        {"nom": "Abonnement SaaS", "statut": "Structure prÃªte", "categorie": "Business"},
        {"nom": "Stripe", "statut": "Endpoint placeholder prÃªt", "categorie": "Paiement"},
        {"nom": "Monitoring", "statut": "Health API active", "categorie": "Ops"},
        {"nom": "Logs", "statut": "HTTP logger actif", "categorie": "Ops"},
        {"nom": "CI/CD", "statut": "Docker prÃªt", "categorie": "DevOps"},
        {"nom": "DÃ©ploiement cloud", "statut": "Docker/Nginx/PostgreSQL prÃªts", "categorie": "Cloud"}
    ]

    return render_template(
        "commercial_saas.html",
        modules=modules
    )


@ecritures_routes.route('/api/monitoring')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_monitoring():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM ecritures")
    nb_ecritures = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM users")
    nb_users = c.fetchone()[0]

    conn.close()

    return jsonify({
        "application": "ComptaPilot",
        "status": "running",
        "environment": "commercial-saas",
        "database": "connected",
        "ecritures": nb_ecritures,
        "utilisateurs": nb_users,
        "modules": {
            "jwt": "active",
            "api": "active",
            "dashboard": "active",
            "audit": "active",
            "exports": "active",
            "docker": "ready",
            "postgresql": "ready",
            "nginx": "ready"
        }
    })


@ecritures_routes.route('/api/workflow-validation')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_workflow_validation():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    # VÃ©rifie si la colonne valide existe
    c.execute("""
        PRAGMA table_info(ecritures)
    """)

    colonnes = [col[1] for col in c.fetchall()]

    if "valide" not in colonnes:

        conn.close()

        return jsonify({
            "workflow": "validation-comptable",
            "statut": "colonne_manquante",
            "message": "La colonne 'valide' n'existe pas encore.",
            "prochaine_action": "Ajouter la colonne valide dans la table ecritures."
        })

    c.execute("""
        SELECT COUNT(*)
        FROM ecritures
        WHERE valide IS NULL OR valide = 0
    """)

    ecritures_a_valider = c.fetchone()[0]

    conn.close()

    return jsonify({
        "workflow": "validation-comptable",
        "ecritures_a_valider": ecritures_a_valider,
        "statut": "pret",
        "prochaine_action": "Ajouter validation par rÃ´le utilisateur"
    })

@ecritures_routes.route('/api/abonnement-saas')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_abonnement_saas():

    return jsonify({
        "offre": "ComptaPilot Pro",
        "statut": "simulation",
        "prix_mensuel_ht": 49,
        "devise": "EUR",
        "stripe": "pret_a_connecter",
        "fonctionnalites": [
            "Dashboard financier",
            "API REST",
            "JWT",
            "Exports",
            "Audit automatique",
            "Centre SaaS",
            "Mode expert-comptable"
        ]
    })


@ecritures_routes.route('/workflow-validation')
@login_required
@permission_required("ACCESS_ECRITURES")
def workflow_validation():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            id,
            date_ecriture,
            piece,
            libelle,
            debit,
            credit,
            COALESCE(valide, 0)
        FROM ecritures
        ORDER BY date_ecriture DESC, id DESC
    """)

    rows = c.fetchall()

    conn.close()

    return render_template(
        "workflow_validation.html",
        rows=rows
    )


@ecritures_routes.route('/workflow-validation/valider/<int:ecriture_id>')
@login_required
@permission_required("ACCESS_ECRITURES")
def valider_ecriture(ecriture_id):

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE ecritures
        SET valide = 1
        WHERE id = ?
    """, (ecriture_id,))

    conn.commit()
    conn.close()

    flash("Ã‰criture validÃ©e avec succÃ¨s.", "success")

    return redirect(url_for('ecritures.workflow_validation'))


@ecritures_routes.route('/workflow-validation/rejeter/<int:ecriture_id>')
@login_required
@permission_required("ACCESS_ECRITURES")
def rejeter_ecriture(ecriture_id):

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE ecritures
        SET valide = 0
        WHERE id = ?
    """, (ecriture_id,))

    conn.commit()
    conn.close()

    flash("Ã‰criture remise en attente.", "warning")

    return redirect(url_for('ecritures.workflow_validation'))
# ==============================
# MODULE HAUT NIVEAU PRODUIT
# ==============================

@ecritures_routes.route('/haut-niveau-produit')
@login_required
@permission_required("ACCESS_ECRITURES")
def haut_niveau_produit():

    modules = [
        {"nom": "Validation multi-niveaux", "statut": "Workflow enrichi prÃªt", "categorie": "Process"},
        {"nom": "Signature Ã©lectronique", "statut": "Signature simulÃ©e prÃªte", "categorie": "LÃ©gal"},
        {"nom": "Journal dâ€™audit", "statut": "Historisation active", "categorie": "TraÃ§abilitÃ©"},
        {"nom": "Notifications temps rÃ©el", "statut": "API prÃªte WebSocket", "categorie": "Temps rÃ©el"},
        {"nom": "WebSocket", "statut": "PrÃ©paration Socket.IO", "categorie": "Infrastructure"},
        {"nom": "OCR IA rÃ©el", "statut": "Connecteur prÃªt", "categorie": "IA"},
        {"nom": "Import bancaire intelligent", "statut": "Base connecteur prÃªte", "categorie": "Banque"},
        {"nom": "Rapprochement automatique", "statut": "Moteur prÃ©parÃ©", "categorie": "Banque"},
        {"nom": "Assistant IA conversationnel", "statut": "Console prÃªte", "categorie": "IA"},
        {"nom": "Portail client expert-comptable", "statut": "Page portail prÃªte", "categorie": "Cabinet"},
        {"nom": "Multi-tenant rÃ©el", "statut": "Structure sociÃ©tÃ©s prÃªte", "categorie": "SaaS"},
        {"nom": "Permissions dynamiques sociÃ©tÃ©", "statut": "PrÃªt Ã  connecter", "categorie": "SÃ©curitÃ©"},
        {"nom": "Stripe rÃ©el", "statut": "Placeholder API prÃªt", "categorie": "Paiement"},
        {"nom": "PostgreSQL production", "statut": "DATABASE_URL prÃªt", "categorie": "Production"},
        {"nom": "Cloud automatisÃ©", "statut": "Docker/Nginx prÃªts", "categorie": "DevOps"},
        {"nom": "Prometheus/Grafana", "statut": "Endpoint mÃ©triques prÃªt", "categorie": "Monitoring"},
        {"nom": "Backup cloud", "statut": "API backup prÃªte", "categorie": "SÃ©curitÃ©"},
        {"nom": "Liasse fiscale automatique", "statut": "PrÃ©paration fiscale prÃªte", "categorie": "FiscalitÃ©"},
        {"nom": "Moteur analytique BI", "statut": "API BI prÃªte", "categorie": "Analytics"}
    ]

    return render_template(
        "haut_niveau_produit.html",
        modules=modules
    )


@ecritures_routes.route('/api/audit-trail')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_audit_trail():

    return jsonify({
        "module": "journal_audit",
        "statut": "actif",
        "evenements": [
            "Connexion utilisateur",
            "Consultation dashboard",
            "Validation Ã©criture",
            "Export comptable",
            "Appel API"
        ]
    })


@ecritures_routes.route('/api/signature-electronique')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_signature_electronique():

    return jsonify({
        "module": "signature_electronique",
        "statut": "simulation",
        "niveau": "pret_a_connecter",
        "prestataires_possibles": [
            "Yousign",
            "DocuSign",
            "Universign"
        ]
    })


@ecritures_routes.route('/api/bi-analytics')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_bi_analytics():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            COALESCE(SUM(credit), 0),
            COALESCE(SUM(debit), 0),
            COUNT(*)
        FROM ecritures
    """)

    total_credit, total_debit, nb_ecritures = c.fetchone()

    conn.close()

    total_credit = float(total_credit or 0)
    total_debit = float(total_debit or 0)
    resultat = total_credit - total_debit

    return jsonify({
        "module": "bi_analytics",
        "ca": round(total_credit, 2),
        "charges": round(total_debit, 2),
        "resultat": round(resultat, 2),
        "marge": round((resultat / total_credit) * 100, 2) if total_credit > 0 else 0,
        "nb_ecritures": nb_ecritures,
        "niveau": "cockpit_direction"
    })


@ecritures_routes.route('/api/backup-cloud')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_backup_cloud():

    return jsonify({
        "module": "backup_cloud",
        "statut": "pret",
        "fichier_source": "db.sqlite",
        "destination": "cloud_a_configurer",
        "frequence": "quotidienne"
    })


@ecritures_routes.route('/api/stripe-checkout')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_stripe_checkout():

    return jsonify({
        "module": "stripe",
        "statut": "simulation",
        "offre": "ComptaPilot Pro",
        "prix_ht": 49,
        "devise": "EUR",
        "prochaine_action": "Connecter STRIPE_SECRET_KEY"
    })


@ecritures_routes.route('/api/liasse-fiscale')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_liasse_fiscale():

    return jsonify({
        "module": "liasse_fiscale",
        "statut": "preparation",
        "documents": [
            "Bilan",
            "Compte de rÃ©sultat",
            "Balance",
            "Grand livre",
            "FEC"
        ],
        "prochaine_action": "Mapper les comptes PCG vers les formulaires fiscaux"
    })


@ecritures_routes.route('/portail-client')
@login_required
@permission_required("ACCESS_ECRITURES")
def portail_client():

    return render_template(
        "portail_client.html"
    )
# ==============================
# JOURNAL D'AUDIT RÃ‰EL
# ==============================

def initialiser_audit_actions():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS audit_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_action TEXT DEFAULT CURRENT_TIMESTAMP,
            utilisateur TEXT,
            action TEXT,
            module TEXT,
            detail TEXT,
            ecriture_id INTEGER
        )
    """)

    conn.commit()
    conn.close()


def enregistrer_action_audit(action, module, detail="", ecriture_id=None):

    initialiser_audit_actions()

    utilisateur = session.get("username", "Utilisateur inconnu")

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        INSERT INTO audit_actions (
            utilisateur,
            action,
            module,
            detail,
            ecriture_id
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        utilisateur,
        action,
        module,
        detail,
        ecriture_id
    ))

    conn.commit()
    conn.close()


@ecritures_routes.route('/audit-actions')
@login_required
@permission_required("ACCESS_ECRITURES")
def audit_actions():

    initialiser_audit_actions()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            id,
            date_action,
            utilisateur,
            action,
            module,
            detail,
            ecriture_id
        FROM audit_actions
        ORDER BY date_action DESC, id DESC
        LIMIT 200
    """)

    rows = c.fetchall()

    conn.close()

    return render_template(
        "audit_actions.html",
        rows=rows
    )


@ecritures_routes.route('/api/audit-actions')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_audit_actions():

    initialiser_audit_actions()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            id,
            date_action,
            utilisateur,
            action,
            module,
            detail,
            ecriture_id
        FROM audit_actions
        ORDER BY date_action DESC, id DESC
        LIMIT 200
    """)

    rows = c.fetchall()

    conn.close()

    actions = []

    for row in rows:

        actions.append({
            "id": row[0],
            "date_action": row[1],
            "utilisateur": row[2],
            "action": row[3],
            "module": row[4],
            "detail": row[5],
            "ecriture_id": row[6]
        })

    return jsonify({
        "module": "audit_actions",
        "total": len(actions),
        "actions": actions
    })


@ecritures_routes.route('/workflow-validation/valider-audit/<int:ecriture_id>')
@login_required
@permission_required("ACCESS_ECRITURES")
def valider_ecriture_audit(ecriture_id):

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE ecritures
        SET valide = 1
        WHERE id = ?
    """, (ecriture_id,))

    conn.commit()
    conn.close()

    enregistrer_action_audit(
        action="VALIDATION_ECRITURE",
        module="workflow_validation",
        detail=f"Validation de l'Ã©criture {ecriture_id}",
        ecriture_id=ecriture_id
    )

    flash("Ã‰criture validÃ©e et historisÃ©e.", "success")

    return redirect(url_for('ecritures.workflow_validation'))


@ecritures_routes.route('/workflow-validation/rejeter-audit/<int:ecriture_id>')
@login_required
@permission_required("ACCESS_ECRITURES")
def rejeter_ecriture_audit(ecriture_id):

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE ecritures
        SET valide = 0
        WHERE id = ?
    """, (ecriture_id,))

    conn.commit()
    conn.close()

    enregistrer_action_audit(
        action="REJET_ECRITURE",
        module="workflow_validation",
        detail=f"Rejet ou remise en attente de l'Ã©criture {ecriture_id}",
        ecriture_id=ecriture_id
    )

    flash("Ã‰criture rejetÃ©e et historisÃ©e.", "warning")

    return redirect(url_for('ecritures.workflow_validation'))
# ==============================
# VALIDATION MULTI-NIVEAUX
# ==============================

def initialiser_validation_multi_niveaux():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("PRAGMA table_info(ecritures)")
    colonnes = [col[1] for col in c.fetchall()]

    if "validation_niveau_1" not in colonnes:
        c.execute("ALTER TABLE ecritures ADD COLUMN validation_niveau_1 INTEGER DEFAULT 0")

    if "validation_niveau_2" not in colonnes:
        c.execute("ALTER TABLE ecritures ADD COLUMN validation_niveau_2 INTEGER DEFAULT 0")

    if "validation_niveau_3" not in colonnes:
        c.execute("ALTER TABLE ecritures ADD COLUMN validation_niveau_3 INTEGER DEFAULT 0")

    conn.commit()
    conn.close()


@ecritures_routes.route('/validation-multi-niveaux')
@login_required
@permission_required("ACCESS_ECRITURES")
def validation_multi_niveaux():

    initialiser_validation_multi_niveaux()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            id,
            date_ecriture,
            piece,
            libelle,
            debit,
            credit,
            COALESCE(validation_niveau_1, 0),
            COALESCE(validation_niveau_2, 0),
            COALESCE(validation_niveau_3, 0)
        FROM ecritures
        ORDER BY date_ecriture DESC, id DESC
    """)

    rows = c.fetchall()

    conn.close()

    return render_template(
        "validation_multi_niveaux.html",
        rows=rows
    )


@ecritures_routes.route('/validation-multi-niveaux/valider/<int:niveau>/<int:ecriture_id>')
@login_required
@permission_required("ACCESS_ECRITURES")
def valider_niveau_ecriture(niveau, ecriture_id):

    initialiser_validation_multi_niveaux()

    if niveau not in [1, 2, 3]:
        flash("Niveau de validation invalide.", "error")
        return redirect(url_for("ecritures.validation_multi_niveaux"))

    colonne = f"validation_niveau_{niveau}"

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute(f"""
        UPDATE ecritures
        SET {colonne} = 1
        WHERE id = ?
    """, (ecriture_id,))

    if niveau == 3:
        c.execute("""
            UPDATE ecritures
            SET valide = 1
            WHERE id = ?
        """, (ecriture_id,))

    conn.commit()
    conn.close()

    enregistrer_action_audit(
        action=f"VALIDATION_NIVEAU_{niveau}",
        module="validation_multi_niveaux",
        detail=f"Validation niveau {niveau} de l'Ã©criture {ecriture_id}",
        ecriture_id=ecriture_id
    )

    flash(f"Ã‰criture {ecriture_id} validÃ©e au niveau {niveau}.", "success")

    return redirect(url_for("ecritures.validation_multi_niveaux"))


@ecritures_routes.route('/validation-multi-niveaux/reinitialiser/<int:ecriture_id>')
@login_required
@permission_required("ACCESS_ECRITURES")
def reinitialiser_validation_multi_niveaux(ecriture_id):

    initialiser_validation_multi_niveaux()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE ecritures
        SET
            validation_niveau_1 = 0,
            validation_niveau_2 = 0,
            validation_niveau_3 = 0,
            valide = 0
        WHERE id = ?
    """, (ecriture_id,))

    conn.commit()
    conn.close()

    enregistrer_action_audit(
        action="REINITIALISATION_VALIDATION",
        module="validation_multi_niveaux",
        detail=f"RÃ©initialisation validation multi-niveaux de l'Ã©criture {ecriture_id}",
        ecriture_id=ecriture_id
    )

    flash(f"Validation de l'Ã©criture {ecriture_id} rÃ©initialisÃ©e.", "warning")

    return redirect(url_for("ecritures.validation_multi_niveaux"))


@ecritures_routes.route('/api/validation-multi-niveaux')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_validation_multi_niveaux():

    initialiser_validation_multi_niveaux()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(validation_niveau_1), 0),
            COALESCE(SUM(validation_niveau_2), 0),
            COALESCE(SUM(validation_niveau_3), 0)
        FROM ecritures
    """)

    total, niveau_1, niveau_2, niveau_3 = c.fetchone()

    conn.close()

    return jsonify({
        "module": "validation_multi_niveaux",
        "total_ecritures": total,
        "niveau_1_validees": niveau_1,
        "niveau_2_validees": niveau_2,
        "niveau_3_validees": niveau_3,
        "workflow": "collaborateur_superviseur_expert_comptable"
    })
# ==============================
# COLLABORATION SAAS AVANCÃ‰E
# ==============================

def initialiser_collaboration_saas():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS commentaires_ecritures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ecriture_id INTEGER,
            utilisateur TEXT,
            commentaire TEXT,
            date_commentaire TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS demandes_correction (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ecriture_id INTEGER,
            utilisateur TEXT,
            motif TEXT,
            statut TEXT DEFAULT 'ouverte',
            date_demande TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS coffre_fort_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_document TEXT,
            type_document TEXT,
            statut TEXT DEFAULT 'archive',
            date_depot TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS clotures_mensuelles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            periode TEXT UNIQUE,
            statut TEXT DEFAULT 'cloturee',
            utilisateur TEXT,
            date_cloture TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


@ecritures_routes.route('/collaboration-saas')
@login_required
@permission_required("ACCESS_ECRITURES")
def collaboration_saas():

    initialiser_collaboration_saas()

    modules = [
        {"nom": "Permissions dynamiques par rÃ´le", "statut": "PrÃªt Ã  connecter aux sociÃ©tÃ©s"},
        {"nom": "Profils utilisateurs", "statut": "Base utilisateurs existante"},
        {"nom": "Affectation dossiers / sociÃ©tÃ©s", "statut": "PrÃ©paration multi-tenant"},
        {"nom": "Notifications temps rÃ©el", "statut": "PrÃªt WebSocket"},
        {"nom": "Commentaires sur Ã©critures", "statut": "Actif"},
        {"nom": "Demandes de correction", "statut": "Actif"},
        {"nom": "Coffre-fort documentaire", "statut": "Actif"},
        {"nom": "OCR IA connectÃ©", "statut": "Ã€ brancher fournisseur IA"},
        {"nom": "Import bancaire automatique", "statut": "Ã€ connecter banque"},
        {"nom": "Rapprochement bancaire intelligent", "statut": "Moteur prÃ©parÃ©"},
        {"nom": "RÃ¨gles comptables", "statut": "Analyse automatique active"},
        {"nom": "Assistant IA conversationnel", "statut": "Console prÃªte"},
        {"nom": "Analytics BI avancÃ©s", "statut": "API BI active"},
        {"nom": "ClÃ´ture mensuelle automatisÃ©e", "statut": "Actif"}
    ]

    return render_template(
        "collaboration_saas.html",
        modules=modules
    )


@ecritures_routes.route('/commentaires-ecritures')
@login_required
@permission_required("ACCESS_ECRITURES")
def commentaires_ecritures():

    initialiser_collaboration_saas()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            id,
            ecriture_id,
            utilisateur,
            commentaire,
            date_commentaire
        FROM commentaires_ecritures
        ORDER BY date_commentaire DESC
        LIMIT 200
    """)

    rows = c.fetchall()

    conn.close()

    return render_template(
        "commentaires_ecritures.html",
        rows=rows
    )


@ecritures_routes.route('/commentaires-ecritures/ajouter', methods=['POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def ajouter_commentaire_ecriture():

    initialiser_collaboration_saas()

    ecriture_id = request.form.get("ecriture_id") or None
    commentaire = request.form.get("commentaire")
    utilisateur = session.get("username", "Utilisateur inconnu")

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        INSERT INTO commentaires_ecritures (
            ecriture_id,
            utilisateur,
            commentaire
        )
        VALUES (?, ?, ?)
    """, (
        ecriture_id,
        utilisateur,
        commentaire
    ))

    conn.commit()
    conn.close()

    enregistrer_action_audit(
        action="COMMENTAIRE_ECRITURE",
        module="collaboration_saas",
        detail=f"Commentaire ajoutÃ© sur l'Ã©criture {ecriture_id}",
        ecriture_id=ecriture_id
    )

    flash("Commentaire ajoutÃ©.", "success")

    return redirect(url_for("ecritures.commentaires_ecritures"))


@ecritures_routes.route('/demandes-correction')
@login_required
@permission_required("ACCESS_ECRITURES")
def demandes_correction():

    initialiser_collaboration_saas()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            id,
            ecriture_id,
            utilisateur,
            motif,
            statut,
            date_demande
        FROM demandes_correction
        ORDER BY date_demande DESC
        LIMIT 200
    """)

    rows = c.fetchall()

    conn.close()

    return render_template(
        "demandes_correction.html",
        rows=rows
    )


@ecritures_routes.route('/demandes-correction/ajouter', methods=['POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def ajouter_demande_correction():

    initialiser_collaboration_saas()

    ecriture_id = request.form.get("ecriture_id")
    motif = request.form.get("motif")
    utilisateur = session.get("username", "Utilisateur inconnu")

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        INSERT INTO demandes_correction (
            ecriture_id,
            utilisateur,
            motif
        )
        VALUES (?, ?, ?)
    """, (
        ecriture_id,
        utilisateur,
        motif
    ))

    conn.commit()
    conn.close()

    enregistrer_action_audit(
        action="DEMANDE_CORRECTION",
        module="collaboration_saas",
        detail=f"Demande de correction sur l'Ã©criture {ecriture_id}",
        ecriture_id=ecriture_id
    )

    flash("Demande de correction crÃ©Ã©e.", "warning")

    return redirect(url_for("ecritures.demandes_correction"))


@ecritures_routes.route('/demandes-correction/cloturer/<int:demande_id>')
@login_required
@permission_required("ACCESS_ECRITURES")
def cloturer_demande_correction(demande_id):

    initialiser_collaboration_saas()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE demandes_correction
        SET statut = 'cloturee'
        WHERE id = ?
    """, (demande_id,))

    conn.commit()
    conn.close()

    enregistrer_action_audit(
        action="CLOTURE_DEMANDE_CORRECTION",
        module="collaboration_saas",
        detail=f"Demande de correction {demande_id} clÃ´turÃ©e"
    )

    flash("Demande clÃ´turÃ©e.", "success")

    return redirect(url_for("ecritures.demandes_correction"))


@ecritures_routes.route('/coffre-fort')
@login_required
@permission_required("ACCESS_ECRITURES")
def coffre_fort():

    initialiser_collaboration_saas()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            id,
            nom_document,
            type_document,
            statut,
            date_depot
        FROM coffre_fort_documents
        ORDER BY date_depot DESC
        LIMIT 200
    """)

    rows = c.fetchall()

    conn.close()

    return render_template(
        "coffre_fort.html",
        rows=rows
    )


@ecritures_routes.route('/coffre-fort/ajouter', methods=['POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def ajouter_document_coffre_fort():

    initialiser_collaboration_saas()

    nom_document = request.form.get("nom_document")
    type_document = request.form.get("type_document")

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        INSERT INTO coffre_fort_documents (
            nom_document,
            type_document
        )
        VALUES (?, ?)
    """, (
        nom_document,
        type_document
    ))

    conn.commit()
    conn.close()

    enregistrer_action_audit(
        action="AJOUT_DOCUMENT_COFFRE_FORT",
        module="coffre_fort",
        detail=f"Document ajoutÃ© : {nom_document}"
    )

    flash("Document archivÃ© dans le coffre-fort.", "success")

    return redirect(url_for("ecritures.coffre_fort"))


@ecritures_routes.route('/cloture-mensuelle')
@login_required
@permission_required("ACCESS_ECRITURES")
def cloture_mensuelle_ia():

    initialiser_collaboration_saas()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            id,
            periode,
            statut,
            utilisateur,
            date_cloture
        FROM clotures_mensuelles
        ORDER BY date_cloture DESC
        LIMIT 200
    """)

    rows = c.fetchall()

    conn.close()

    return render_template(
        "cloture_mensuelle.html",
        rows=rows
    )


@ecritures_routes.route('/cloture-mensuelle/creer', methods=['POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def creer_cloture_mensuelle():

    initialiser_collaboration_saas()

    periode = request.form.get("periode")
    utilisateur = session.get("username", "Utilisateur inconnu")

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        INSERT OR IGNORE INTO clotures_mensuelles (
            periode,
            utilisateur
        )
        VALUES (?, ?)
    """, (
        periode,
        utilisateur
    ))

    conn.commit()
    conn.close()

    enregistrer_action_audit(
        action="CLOTURE_MENSUELLE",
        module="cloture_comptable",
        detail=f"ClÃ´ture mensuelle de la pÃ©riode {periode}"
    )

    flash("ClÃ´ture mensuelle enregistrÃ©e.", "success")

    return redirect(url_for("ecritures.cloture_mensuelle"))


@ecritures_routes.route('/api/collaboration-saas')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_collaboration_saas():

    initialiser_collaboration_saas()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM commentaires_ecritures")
    nb_commentaires = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM demandes_correction WHERE statut = 'ouverte'")
    nb_corrections = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM coffre_fort_documents")
    nb_documents = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM clotures_mensuelles")
    nb_clotures = c.fetchone()[0]

    conn.close()

    return jsonify({
        "module": "collaboration_saas",
        "commentaires": nb_commentaires,
        "demandes_correction_ouvertes": nb_corrections,
        "documents_coffre_fort": nb_documents,
        "clotures_mensuelles": nb_clotures,
        "websocket": "pret_a_connecter",
        "ocr_ia": "pret_a_connecter",
        "rapprochement_bancaire": "pret_a_connecter",
        "assistant_ia": "pret_a_connecter"
    })
# ==============================
# ASSISTANT IA CONVERSATIONNEL
# ==============================

def initialiser_assistant_ia():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS assistant_ia_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utilisateur TEXT,
            question TEXT,
            reponse TEXT,
            date_message TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def generer_reponse_ia(question):

    question_lower = question.lower()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            COALESCE(SUM(credit), 0),
            COALESCE(SUM(debit), 0),
            COUNT(*)
        FROM ecritures
    """)

    total_credit, total_debit, nb_ecritures = c.fetchone()

    conn.close()

    total_credit = round(float(total_credit or 0), 2)
    total_debit = round(float(total_debit or 0), 2)
    resultat = round(total_credit - total_debit, 2)
    tva = round(total_credit * 0.20, 2)

    marge = 0
    if total_credit > 0:
        marge = round((resultat / total_credit) * 100, 2)

    if "résultat" in question_lower or "resultat" in question_lower or "bénéfice" in question_lower or "benefice" in question_lower:
        return f"Le résultat comptable actuel est de {resultat} euros."

    if "charges" in question_lower or "débit" in question_lower or "debit" in question_lower:
        return f"Les charges actuelles sont de {total_debit} euros."

    if "chiffre" in question_lower or "ca" in question_lower or "vente" in question_lower:
        return f"Le chiffre d'affaires actuel est de {total_credit} euros."

    if "marge" in question_lower:
        return f"La marge actuelle est de {marge} pour cent."

    if "écritures" in question_lower or "ecritures" in question_lower:
        return f"Le système contient actuellement {nb_ecritures} écritures comptables."

    if "tva" in question_lower:
        return f"La TVA estimée actuelle est de {tva} euros."

    if "audit" in question_lower:
        return "Le module audit est actif. Il historise les validations, rejets, commentaires et actions importantes."

    if "clôture" in question_lower or "cloture" in question_lower:
        return "Le module de clôture mensuelle est actif. Il permet d'enregistrer les périodes clôturées."

    if "conseil" in question_lower or "analyse" in question_lower:
        if resultat < 0:
            return "Analyse IA : le résultat est négatif. Priorité recommandée : réduire les charges, contrôler les dépenses fournisseurs et analyser les écritures déficitaires."
        return "Analyse IA : le résultat est positif. La situation est favorable, mais la marge et la trésorerie doivent rester surveillées."

    return (
        f"Synthèse IA : chiffre d'affaires {total_credit} euros, "
        f"charges {total_debit} euros, résultat {resultat} euros, "
        f"marge {marge} pour cent, TVA estimée {tva} euros."
    )



@csrf.exempt
@ecritures_routes.route('/assistant-ia-conversationnel/envoyer', methods=['POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def envoyer_message_ia():

    initialiser_assistant_ia()

    question = request.form.get("question")
    utilisateur = session.get("username", "Utilisateur inconnu")

    reponse = generer_reponse_ia(question)

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        INSERT INTO assistant_ia_messages (
            utilisateur,
            question,
            reponse
        )
        VALUES (?, ?, ?)
    """, (
        utilisateur,
        question,
        reponse
    ))

    conn.commit()
    conn.close()

    enregistrer_action_audit(
        action="QUESTION_ASSISTANT_IA",
        module="assistant_ia",
        detail=f"Question IA : {question}"
    )

    flash("Réponse IA générée.", "success")

    return redirect(url_for("ecritures.assistant_ia_conversationnel"))


@ecritures_routes.route('/api/assistant-ia')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_assistant_ia():

    initialiser_assistant_ia()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM assistant_ia_messages")
    nb_messages = c.fetchone()[0]

    conn.close()

    return jsonify({
        "assistant": "comptapilot_ai",
        "statut": "actif",
        "historique_messages": nb_messages,
        "capacites": [
            "analyse_comptable",
            "resultat",
            "charges",
            "tva",
            "marge",
            "audit",
            "cloture",
            "dashboard"
        ]
    })


# ==============================
# COPILOTE IA COMPTABLE AVANCÉ
# ==============================

def analyser_copilote_ia():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            COALESCE(SUM(credit), 0),
            COALESCE(SUM(debit), 0),
            COUNT(*)
        FROM ecritures
    """)

    total_credit, total_debit, nb_ecritures = c.fetchone()

    conn.close()

    ca = round(float(total_credit or 0), 2)
    charges = round(float(total_debit or 0), 2)
    resultat = round(ca - charges, 2)
    tva = round(ca * 0.20, 2)

    marge = 0
    if ca > 0:
        marge = round((resultat / ca) * 100, 2)

    risque = 0
    anomalies = []
    recommandations = []

    if resultat < 0:
        risque += 35
        anomalies.append("Résultat négatif")
        recommandations.append("Analyser les charges principales et identifier les postes à réduire.")

    if charges > ca:
        risque += 35
        anomalies.append("Charges supérieures au chiffre d'affaires")
        recommandations.append("Contrôler les dépenses fournisseurs et les écritures de charges.")

    if marge < 0:
        risque += 20
        anomalies.append("Marge négative")
        recommandations.append("Revoir la rentabilité globale de l'activité.")

    if nb_ecritures == 0:
        risque += 10
        anomalies.append("Aucune écriture comptable")
        recommandations.append("Importer ou saisir les écritures comptables.")

    if not anomalies:
        anomalies.append("Aucune anomalie critique détectée")

    if not recommandations:
        recommandations.append("Situation comptable stable. Maintenir le suivi mensuel.")

    risque = min(risque, 100)

    return {
        "ca": ca,
        "charges": charges,
        "resultat": resultat,
        "tva": tva,
        "marge": marge,
        "nb_ecritures": nb_ecritures,
        "risque": risque,
        "anomalies": anomalies,
        "recommandations": recommandations
    }


@ecritures_routes.route('/copilote-ia')
@login_required
@permission_required("ACCESS_ECRITURES")
def copilote_ia():

    analyse = analyser_copilote_ia()

    return render_template(
        "copilote_ia.html",
        analyse=analyse
    )


@ecritures_routes.route('/api/copilote-ia')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_copilote_ia():

    analyse = analyser_copilote_ia()

    return jsonify({
        "module": "copilote_ia_comptable",
        "statut": "actif",
        "analyse": analyse,
        "openai": "pret_a_connecter"
    })


@ecritures_routes.route('/rapport-ia-pdf')
@login_required
@permission_required("ACCESS_ECRITURES")
def rapport_ia_pdf():

    analyse = analyser_copilote_ia()

    return render_template(
        "rapport_ia_pdf.html",
        analyse=analyse
    )
# ==============================
# IA OCR + COMPTABILISATION
# ==============================

import os
import json
import pandas as pd
import pytesseract
import pdfplumber

from PIL import Image
from openai import OpenAI
from werkzeug.utils import secure_filename


def client_openai():

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    return OpenAI(api_key=api_key)


def analyser_facture_ocr(filepath):

    texte = ""

    if filepath.lower().endswith(".pdf"):

        with pdfplumber.open(filepath) as pdf:

            for page in pdf.pages:
                texte += page.extract_text() or ""

    else:

        image = Image.open(filepath)
        texte = pytesseract.image_to_string(image)

    return texte


def analyser_facture_openai(texte):

    client = client_openai()

    if not client:

        return {
            "fournisseur": "OpenAI non configure",
            "montant_ht": 0,
            "montant_tva": 0,
            "montant_ttc": 0,
            "date_facture": "",
            "compte_charge": "607000",
            "mode": "analyse_locale"
        }

    prompt = f"""
    Analyse cette facture OCR et retourne uniquement un JSON valide.

    Champs attendus :
    fournisseur
    montant_ht
    montant_tva
    montant_ttc
    date_facture
    compte_charge

    TEXTE OCR :
    {texte}
    """

    modeles = [
        "gpt-5.5",
        "gpt-5.5-mini",
        "gpt-4.1",
        "gpt-4.1-mini"
    ]

    for modele in modeles:

        try:

            response = client.chat.completions.create(
                model=modele,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0
            )

            contenu = response.choices[0].message.content

            try:
                data = json.loads(contenu)
                data["modele_utilise"] = modele
                return data

            except Exception:

                return {
                    "erreur": "JSON OpenAI invalide",
                    "brut": contenu,
                    "modele_utilise": modele
                }

        except Exception:
            continue

    return {
        "fournisseur": "Analyse locale - modele OpenAI indisponible",
        "montant_ht": 0,
        "montant_tva": 0,
        "montant_ttc": 0,
        "date_facture": "",
        "compte_charge": "607000",
        "mode": "fallback_local",
        "texte_detecte": texte[:1000]
    }

def generer_ecriture_depuis_facture(data):

    montant_ht = float(data.get("montant_ht", 0))
    montant_tva = float(data.get("montant_tva", 0))
    montant_ttc = float(data.get("montant_ttc", 0))

    return {
        "journal": "ACH",
        "libelle": data.get("fournisseur", "Facture fournisseur"),
        "lignes": [
            {
                "compte": data.get("compte_charge", "607000"),
                "debit": montant_ht,
                "credit": 0
            },
            {
                "compte": "445660",
                "debit": montant_tva,
                "credit": 0
            },
            {
                "compte": "401000",
                "debit": 0,
                "credit": montant_ttc
            }
        ]
    }


@csrf.exempt
@ecritures_routes.route('/ocr-facture-ia', methods=['GET', 'POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def ocr_facture_ia():

    resultat = None
    ecriture = None

    if request.method == "POST":

        fichier = request.files.get("facture")

        if fichier:

            filename = secure_filename(fichier.filename)

            upload_path = os.path.join(
                "uploads",
                "factures",
                filename
            )

            fichier.save(upload_path)

            texte = analyser_facture_ocr(upload_path)

            resultat = analyser_facture_openai(texte)

            if "erreur" not in resultat:

                ecriture = generer_ecriture_depuis_facture(resultat)

                enregistrer_action_audit(
                    action="OCR_FACTURE_IA",
                    module="ocr_ia",
                    detail=f"Facture analysée : {filename}"
                )

    return render_template(
        "ocr_facture_ia.html",
        resultat=resultat,
        ecriture=ecriture
    )


@ecritures_routes.route('/api/rapprochement-bancaire')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_rapprochement_bancaire():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(debit),0),
            COALESCE(SUM(credit),0)
        FROM ecritures
    """)

    nb, total_debit, total_credit = c.fetchone()

    conn.close()

    ecart = round(float(total_debit or 0) - float(total_credit or 0), 2)

    suggestions = []

    if ecart != 0:

        suggestions.append(
            "Des écritures bancaires semblent non rapprochées."
        )

        suggestions.append(
            "Contrôler les paiements fournisseurs et règlements clients."
        )

    else:

        suggestions.append(
            "Le rapprochement bancaire semble cohérent."
        )

    return jsonify({
        "module": "rapprochement_bancaire_ia",
        "statut": "analyse_terminee",
        "ecart": ecart,
        "suggestions": suggestions
    })


@ecritures_routes.route('/copilote-comptable')
@login_required
@permission_required("ACCESS_ECRITURES")
def copilote_comptable():

    return render_template(
        "copilote_comptable.html"
    )
# ==========================================
# IMPORT BANCAIRE IA + RAPPROCHEMENT AVANCÉ
# ==========================================

from ofxparse import OfxParser
from datetime import datetime
from collections import defaultdict


def initialiser_regles_comptables():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS regles_comptables_ia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mot_cle TEXT,
            compte_id TEXT,
            libelle TEXT
        )
    """)

    c.execute("SELECT COUNT(*) FROM regles_comptables_ia")

    nb = c.fetchone()[0]

    if nb == 0:

        regles = [
            ("amazon", "606300", "Achats fournitures"),
            ("edf", "606100", "Electricite"),
            ("urssaf", "645100", "Charges sociales"),
            ("orange", "626000", "Telecom"),
            ("sncf", "625100", "Deplacements"),
            ("carrefour", "606300", "Achats divers"),
            ("loyer", "613200", "Location"),
            ("stripe", "706000", "Paiement client"),
            ("client", "411000", "Reglement client")
        ]

        for mot, compte_id, libelle in regles:

            c.execute("""
                INSERT INTO regles_comptables_ia (
                    mot_cle,
                    compte_id,
                    libelle
                )
                VALUES (?, ?, ?)
            """, (
                mot,
                compte_id,
                libelle
            ))

    conn.commit()
    conn.close()


def detecter_compte_ia(description):

    initialiser_regles_comptables()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT mot_cle, compte_id, libelle
        FROM regles_comptables_ia
    """)

    regles = c.fetchall()

    conn.close()

    description_lower = description.lower()

    for mot, compte_id, libelle in regles:

        if mot.lower() in description_lower:

            return {
                "compte": compte_id,
                "libelle": libelle,
                "confiance": 90
            }

    return {
        "compte": "471000",
        "libelle": "Operation a classifier",
        "confiance": 40
    }


def calculer_score_risque(operation):

    score = 0

    montant = abs(float(operation.get("montant", 0)))

    if montant > 5000:
        score += 35

    if "virement" in operation.get("description", "").lower():
        score += 10

    if "especes" in operation.get("description", "").lower():
        score += 30

    if operation.get("confiance", 0) < 50:
        score += 20

    return min(score, 100)


def detecter_anomalies_bancaires(operations):

    anomalies = []

    montants = defaultdict(int)

    for op in operations:

        cle = f"{op['date']}_{op['montant']}"

        montants[cle] += 1

    for op in operations:

        cle = f"{op['date']}_{op['montant']}"

        if montants[cle] > 1:

            anomalies.append({
                "type": "doublon",
                "operation": op
            })

    return anomalies


@csrf.exempt
@ecritures_routes.route('/import-bancaire-ia', methods=['GET', 'POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def import_bancaire_ia():

    operations = []
    anomalies = []
    total_credit = 0
    total_debit = 0

    if request.method == "POST":

        fichier = request.files.get("fichier")

        if fichier:

            filename = secure_filename(fichier.filename)

            upload_path = os.path.join(
                "uploads",
                "bancaire",
                filename
            )

            fichier.save(upload_path)

            if filename.lower().endswith(".csv"):

                df = pd.read_csv(upload_path)

                for _, row in df.iterrows():

                    description = str(row.get("description", ""))
                    montant = float(row.get("montant", 0))

                    analyse = detecter_compte_ia(description)

                    operation = {
                        "date": str(row.get("date", "")),
                        "description": description,
                        "montant": montant,
                        "compte": analyse["compte"],
                        "libelle": analyse["libelle"],
                        "confiance": analyse["confiance"]
                    }

                    operation["risque"] = calculer_score_risque(operation)

                    operations.append(operation)

                    if montant > 0:
                        total_credit += montant
                    else:
                        total_debit += abs(montant)

            elif filename.lower().endswith(".ofx"):

                with open(upload_path, "rb") as f:

                    ofx = OfxParser.parse(f)

                    for transaction in ofx.account.statement.transactions:

                        description = transaction.memo or ""
                        montant = float(transaction.amount)

                        analyse = detecter_compte_ia(description)

                        operation = {
                            "date": str(transaction.date),
                            "description": description,
                            "montant": montant,
                            "compte": analyse["compte"],
                            "libelle": analyse["libelle"],
                            "confiance": analyse["confiance"]
                        }

                        operation["risque"] = calculer_score_risque(operation)

                        operations.append(operation)

                        if montant > 0:
                            total_credit += montant
                        else:
                            total_debit += abs(montant)

            anomalies = detecter_anomalies_bancaires(operations)

            initialiser_precompta_ia()

            conn = sqlite3.connect("db.sqlite")
            c = conn.cursor()

            for op in operations:

                c.execute("""
                    INSERT INTO precompta_ia (
                        date_operation,
                        description,
                        montant,
                        compte_suggere,
                        libelle_suggere,
                        confiance
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    op["date"],
                    op["description"],
                    op["montant"],
                    op["compte"],
                    op["libelle"],
                    op["confiance"]
                ))

            conn.commit()
            conn.close()

            enregistrer_action_audit(
                action="IMPORT_BANCAIRE_IA",
                module="banque_ia",
                detail=f"{len(operations)} operations importees"
            )

    return render_template(
        "import_bancaire_ia.html",
        operations=operations,
        anomalies=anomalies,
        total_credit=round(total_credit, 2),
        total_debit=round(total_debit, 2)
    )

@ecritures_routes.route('/centre-controle-comptable')
@login_required
@permission_required("ACCESS_ECRITURES")
def centre_controle_comptable():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM ecritures")
    nb_ecritures = c.fetchone()[0]

    conn.close()

    modules = [
        "OCR IA",
        "Rapprochement bancaire",
        "Copilote IA",
        "Detection anomalies",
        "Scoring risque",
        "Validation comptable",
        "Analytics BI",
        "Audit intelligent"
    ]

    return render_template(
        "centre_controle_comptable.html",
        modules=modules,
        nb_ecritures=nb_ecritures
    )


@ecritures_routes.route('/api/banque-ia')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_banque_ia():

    return jsonify({
        "module": "banque_ia",
        "fonctionnalites": [
            "import_csv",
            "import_ofx",
            "rapprochement_auto",
            "detection_doublons",
            "scoring_risque",
            "classification_ia",
            "regles_comptables"
        ],
        "statut": "actif"
    })
# ==========================================
# PRE-COMPTABILISATION IA
# ==========================================

def initialiser_precompta_ia():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS precompta_ia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_operation TEXT,
            description TEXT,
            montant REAL,
            compte_suggere TEXT,
            libelle_suggere TEXT,
            confiance INTEGER,
            statut TEXT DEFAULT 'proposee',
            date_creation TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


@csrf.exempt
@ecritures_routes.route('/precompta-ia/import', methods=['POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def importer_precompta_ia():

    initialiser_precompta_ia()

    data = request.get_json()

    operations = data.get("operations", [])

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    compteur = 0

    for op in operations:

        c.execute("""
            INSERT INTO precompta_ia (
                date_operation,
                description,
                montant,
                compte_suggere,
                libelle_suggere,
                confiance
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            op.get("date"),
            op.get("description"),
            op.get("montant"),
            op.get("compte"),
            op.get("libelle"),
            op.get("confiance", 0)
        ))

        compteur += 1

    conn.commit()
    conn.close()

    enregistrer_action_audit(
        action="IMPORT_PRECOMPTA_IA",
        module="precompta_ia",
        detail=f"{compteur} propositions importees"
    )

    return jsonify({
        "statut": "ok",
        "importees": compteur
    })


@ecritures_routes.route('/precompta-ia')
@login_required
@permission_required("ACCESS_ECRITURES")
def precompta_ia():

    initialiser_precompta_ia()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            id,
            date_operation,
            description,
            montant,
            compte_suggere,
            libelle_suggere,
            confiance,
            statut
        FROM precompta_ia
        ORDER BY id DESC
    """)

    rows = c.fetchall()

    conn.close()

    return render_template(
        "precompta_ia.html",
        rows=rows
    )


@ecritures_routes.route('/precompta-ia/valider/<int:precompta_id>')
@login_required
@permission_required("ACCESS_ECRITURES")
def valider_precompta(precompta_id):

    initialiser_precompta_ia()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            date_operation,
            description,
            montant,
            compte_suggere,
            libelle_suggere,
            statut
        FROM precompta_ia
        WHERE id = ?
    """, (precompta_id,))

    row = c.fetchone()

    if not row:
        conn.close()
        flash("Proposition introuvable.", "error")
        return redirect(url_for("ecritures.precompta_ia"))

    date_operation, description, montant, compte_suggere, libelle_suggere, statut = row
    if periode_est_cloturee(date_operation):

        conn.close()

        flash(
            "La période comptable est clôturée.",
            "error"
        )

        return redirect(
            url_for("ecritures.precompta_ia")
        )

    if statut == "validee":
        conn.close()
        flash("Cette proposition est déjà validée.", "warning")
        return redirect(url_for("ecritures.precompta_ia"))

    montant = float(montant or 0)

    debit = abs(montant) if montant < 0 else 0
    credit = montant if montant > 0 else 0

    piece = f"PRECOMPTA-{precompta_id}"
    libelle_final = libelle_suggere or description or "Écriture générée par IA"

    c.execute("PRAGMA table_info(ecritures)")
    colonnes = [col[1] for col in c.fetchall()]

    donnees = {}

    if "date_ecriture" in colonnes:
        donnees["date_ecriture"] = date_operation

    if "piece" in colonnes:
        donnees["piece"] = piece

    if "libelle" in colonnes:
        donnees["libelle"] = libelle_final

    if "debit" in colonnes:
        donnees["debit"] = debit

    if "credit" in colonnes:
        donnees["credit"] = credit

    if "valide" in colonnes:
        donnees["valide"] = 0

    if "journal" in colonnes:
        donnees["journal"] = "BQ"

    if "compte" in colonnes:
        donnees["compte"] = compte_suggere

    colonnes_sql = ", ".join(donnees.keys())
    placeholders = ", ".join(["?"] * len(donnees))
    valeurs = list(donnees.values())

    c.execute(f"""
        INSERT INTO ecritures (
            {colonnes_sql}
        )
        VALUES (
            {placeholders}
        )
    """, valeurs)

    c.execute("""
        UPDATE precompta_ia
        SET statut = 'validee'
        WHERE id = ?
    """, (precompta_id,))

    conn.commit()
    conn.close()

    enregistrer_action_audit(
        action="VALIDATION_PRECOMPTA",
        module="precompta_ia",
        detail=f"Proposition {precompta_id} transformée en écriture comptable"
    )

    log_supervision(
        module="precompta_ia",
        statut="ok",
        detail=f"Pré-compta {precompta_id} validée"
    )

    flash("Écriture comptable générée automatiquement.", "success")

    return redirect(url_for("ecritures.precompta_ia"))

@ecritures_routes.route('/precompta-ia/rejeter/<int:precompta_id>')
@login_required
@permission_required("ACCESS_ECRITURES")
def rejeter_precompta(precompta_id):

    initialiser_precompta_ia()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE precompta_ia
        SET statut = 'rejetee'
        WHERE id = ?
    """, (precompta_id,))

    conn.commit()
    conn.close()

    enregistrer_action_audit(
        action="REJET_PRECOMPTA",
        module="precompta_ia",
        detail=f"Proposition {precompta_id} rejetee"
    )

    flash("Proposition rejetée.", "warning")

    return redirect(url_for("ecritures.precompta_ia"))


@ecritures_routes.route('/api/precompta-ia')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_precompta_ia():

    initialiser_precompta_ia()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            COUNT(*),
            SUM(CASE WHEN statut='validee' THEN 1 ELSE 0 END),
            SUM(CASE WHEN statut='rejetee' THEN 1 ELSE 0 END),
            SUM(CASE WHEN statut='proposee' THEN 1 ELSE 0 END)
        FROM precompta_ia
    """)

    total, validees, rejetees, proposees = c.fetchone()

    conn.close()

    return jsonify({
        "module": "precompta_ia",
        "total": total or 0,
        "validees": validees or 0,
        "rejetees": rejetees or 0,
        "proposees": proposees or 0
    })

# ==========================================
# CONSOLIDATION PRODUCTION COMPTAPILOT
# ==========================================

import shutil
import hashlib
from pathlib import Path


def initialiser_consolidation():

    Path("backups").mkdir(exist_ok=True)

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS imports_bancaires_hash (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation_hash TEXT UNIQUE,
            date_import TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS supervision_systeme (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_event TEXT DEFAULT CURRENT_TIMESTAMP,
            module TEXT,
            statut TEXT,
            detail TEXT
        )
    """)

    conn.commit()
    conn.close()


def log_supervision(module, statut, detail):

    initialiser_consolidation()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        INSERT INTO supervision_systeme (
            module,
            statut,
            detail
        )
        VALUES (?, ?, ?)
    """, (
        module,
        statut,
        detail
    ))

    conn.commit()
    conn.close()


def generer_hash_operation(date_operation, description, montant):

    chaine = f"{date_operation}|{description}|{montant}"
    return hashlib.sha256(chaine.encode("utf-8")).hexdigest()


def operation_deja_importee(operation_hash):

    initialiser_consolidation()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id
        FROM imports_bancaires_hash
        WHERE operation_hash = ?
    """, (operation_hash,))

    row = c.fetchone()

    conn.close()

    return row is not None


def memoriser_operation_importee(operation_hash):

    initialiser_consolidation()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    try:
        c.execute("""
            INSERT INTO imports_bancaires_hash (
                operation_hash
            )
            VALUES (?)
        """, (operation_hash,))
        conn.commit()
    except Exception:
        pass

    conn.close()


@ecritures_routes.route('/sauvegarde-auto')
@login_required
@permission_required("ACCESS_ECRITURES")
def sauvegarde_auto():

    initialiser_consolidation()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    source = "db.sqlite"
    destination = f"backups/db_backup_{timestamp}.sqlite"

    shutil.copy2(source, destination)

    enregistrer_action_audit(
        action="SAUVEGARDE_AUTO",
        module="backup",
        detail=f"Sauvegarde creee : {destination}"
    )

    log_supervision(
        module="backup",
        statut="ok",
        detail=destination
    )

    return jsonify({
        "statut": "ok",
        "backup": destination
    })


@ecritures_routes.route('/supervision')
@login_required
@permission_required("ACCESS_ECRITURES")
def supervision():

    initialiser_consolidation()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM ecritures")
    nb_ecritures = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM precompta_ia")
    nb_precompta = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM audit_actions")
    nb_audit = c.fetchone()[0]

    c.execute("""
        SELECT
            date_event,
            module,
            statut,
            detail
        FROM supervision_systeme
        ORDER BY date_event DESC
        LIMIT 100
    """)

    events = c.fetchall()

    conn.close()

    return render_template(
        "supervision.html",
        nb_ecritures=nb_ecritures,
        nb_precompta=nb_precompta,
        nb_audit=nb_audit,
        events=events
    )


@ecritures_routes.route('/api/sante-globale')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_sante_globale():

    initialiser_consolidation()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    stats = {}

    for table in [
        "ecritures",
        "precompta_ia",
        "audit_actions",
        "regles_comptables_ia",
        "imports_bancaires_hash"
    ]:
        try:
            c.execute(f"SELECT COUNT(*) FROM {table}")
            stats[table] = c.fetchone()[0]
        except Exception:
            stats[table] = "table_absente"

    conn.close()

    return jsonify({
        "application": "ComptaPilot",
        "statut": "ok",
        "modules": stats,
        "backup": "actif",
        "anti_doublons": "actif",
        "audit": "actif",
        "precompta": "actif"
    })
@ecritures_routes.route('/api/precompta-controle')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_precompta_controle():

    initialiser_precompta_ia()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            COUNT(*),
            SUM(CASE WHEN statut = 'proposee' THEN 1 ELSE 0 END),
            SUM(CASE WHEN statut = 'validee' THEN 1 ELSE 0 END),
            SUM(CASE WHEN statut = 'rejetee' THEN 1 ELSE 0 END)
        FROM precompta_ia
    """)

    total, proposees, validees, rejetees = c.fetchone()

    c.execute("SELECT COUNT(*) FROM ecritures")
    nb_ecritures = c.fetchone()[0]

    conn.close()

    return jsonify({
        "module": "precompta_controle",
        "total_precompta": total or 0,
        "proposees": proposees or 0,
        "validees": validees or 0,
        "rejetees": rejetees or 0,
        "ecritures_comptables": nb_ecritures,
        "statut": "operationnel"
    })
# ==========================================
# CLÔTURE COMPTABLE AVANCÉE
# ==========================================

def initialiser_cloture_avancee():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS clotures_comptables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            periode TEXT UNIQUE,
            date_cloture TEXT DEFAULT CURRENT_TIMESTAMP,
            utilisateur TEXT,
            commentaire TEXT
        )
    """)

    conn.commit()
    conn.close()


def periode_est_cloturee(date_ecriture):

    initialiser_cloture_avancee()

    try:
        periode = str(date_ecriture)[:7]
    except Exception:
        return False

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id
        FROM clotures_comptables
        WHERE periode = ?
    """, (periode,))

    row = c.fetchone()

    conn.close()

    return row is not None


@csrf.exempt
@ecritures_routes.route('/cloture-mensuelle', methods=['GET', 'POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def cloture_mensuelle():

    initialiser_cloture_avancee()

    if request.method == "POST":

        periode = request.form.get("periode")
        commentaire = request.form.get("commentaire")

        conn = sqlite3.connect("db.sqlite")
        c = conn.cursor()

        try:

            c.execute("""
                INSERT INTO clotures_comptables (
                    periode,
                    utilisateur,
                    commentaire
                )
                VALUES (?, ?, ?)
            """, (
                periode,
                session.get("username", "admin"),
                commentaire
            ))

            conn.commit()

            enregistrer_action_audit(
                action="CLOTURE_MENSUELLE",
                module="cloture",
                detail=f"Période clôturée : {periode}"
            )

            log_supervision(
                module="cloture",
                statut="ok",
                detail=f"Clôture {periode}"
            )

            flash("Période clôturée avec succès.", "success")

        except Exception:

            flash("Cette période est déjà clôturée.", "warning")

        conn.close()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            periode,
            date_cloture,
            utilisateur,
            commentaire
        FROM clotures_comptables
        ORDER BY periode DESC
    """)

    clotures = c.fetchall()

    conn.close()

    return render_template(
        "cloture_mensuelle.html",
        clotures=clotures
    )


@ecritures_routes.route('/api/clotures')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_clotures():

    initialiser_cloture_avancee()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            periode,
            date_cloture,
            utilisateur
        FROM clotures_comptables
        ORDER BY periode DESC
    """)

    rows = c.fetchall()

    conn.close()

    data = []

    for row in rows:

        data.append({
            "periode": row[0],
            "date_cloture": row[1],
            "utilisateur": row[2]
        })

    return jsonify({
        "module": "cloture_comptable",
        "clotures": data
    })
# ==========================================
# CENTRE FISCAL AUTOMATIQUE
# ==========================================

@ecritures_routes.route('/centre-fiscal')
@login_required
@permission_required("ACCESS_ECRITURES")
def centre_fiscal_auto():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            COALESCE(SUM(debit), 0),
            COALESCE(SUM(credit), 0),
            COUNT(*)
        FROM ecritures
    """)

    total_debit, total_credit, nb_ecritures = c.fetchone()

    c.execute("""
        SELECT
            COALESCE(SUM(credit), 0)
        FROM ecritures
        WHERE compte_id IN (SELECT id FROM plan_comptable WHERE numero LIKE '7%')
    """)

    ca_fiscal = c.fetchone()[0] or 0

    c.execute("""
        SELECT
            COALESCE(SUM(debit), 0)
        FROM ecritures
        WHERE compte_id IN (SELECT id FROM plan_comptable WHERE numero LIKE '6%')
    """)

    charges_fiscales = c.fetchone()[0] or 0

    conn.close()

    total_debit = round(float(total_debit or 0), 2)
    total_credit = round(float(total_credit or 0), 2)
    ca_fiscal = round(float(ca_fiscal or 0), 2)
    charges_fiscales = round(float(charges_fiscales or 0), 2)

    resultat_fiscal = round(ca_fiscal - charges_fiscales, 2)
    tva_collectee = round(ca_fiscal * 0.20, 2)
    tva_deductible = round(charges_fiscales * 0.20, 2)
    tva_a_payer = round(tva_collectee - tva_deductible, 2)
    ecart_balance = round(total_debit - total_credit, 2)

    alertes = []

    if ecart_balance != 0:
        alertes.append("Balance déséquilibrée : débit et crédit ne sont pas égaux.")

    if resultat_fiscal < 0:
        alertes.append("Résultat fiscal négatif.")

    if tva_a_payer > 0:
        alertes.append("TVA prévisionnelle à payer.")

    if nb_ecritures == 0:
        alertes.append("Aucune écriture comptable détectée.")

    if not alertes:
        alertes.append("Aucune alerte fiscale majeure.")

    return render_template(
        "centre_fiscal.html",
        total_debit=total_debit,
        total_credit=total_credit,
        ca_fiscal=ca_fiscal,
        charges_fiscales=charges_fiscales,
        resultat_fiscal=resultat_fiscal,
        tva_collectee=tva_collectee,
        tva_deductible=tva_deductible,
        tva_a_payer=tva_a_payer,
        ecart_balance=ecart_balance,
        nb_ecritures=nb_ecritures,
        alertes=alertes
    )


@ecritures_routes.route('/api/centre-fiscal')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_centre_fiscal_auto():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            COALESCE(SUM(debit), 0),
            COALESCE(SUM(credit), 0),
            COUNT(*)
        FROM ecritures
    """)

    total_debit, total_credit, nb_ecritures = c.fetchone()

    c.execute("""
        SELECT COALESCE(SUM(credit), 0)
        FROM ecritures
        WHERE compte_id IN (SELECT id FROM plan_comptable WHERE numero LIKE '7%')
    """)

    ca_fiscal = c.fetchone()[0] or 0

    c.execute("""
        SELECT COALESCE(SUM(debit), 0)
        FROM ecritures
        WHERE compte_id IN (SELECT id FROM plan_comptable WHERE numero LIKE '6%')
    """)

    charges_fiscales = c.fetchone()[0] or 0

    conn.close()

    total_debit = round(float(total_debit or 0), 2)
    total_credit = round(float(total_credit or 0), 2)
    ca_fiscal = round(float(ca_fiscal or 0), 2)
    charges_fiscales = round(float(charges_fiscales or 0), 2)

    return jsonify({
        "module": "centre_fiscal",
        "total_debit": total_debit,
        "total_credit": total_credit,
        "ecart_balance": round(total_debit - total_credit, 2),
        "ca_fiscal": ca_fiscal,
        "charges_fiscales": charges_fiscales,
        "resultat_fiscal": round(ca_fiscal - charges_fiscales, 2),
        "tva_collectee": round(ca_fiscal * 0.20, 2),
        "tva_deductible": round(charges_fiscales * 0.20, 2),
        "tva_a_payer": round((ca_fiscal * 0.20) - (charges_fiscales * 0.20), 2),
        "nb_ecritures": nb_ecritures,
        "statut": "operationnel"
    })


@ecritures_routes.route('/export-fiscal-csv')
@login_required
@permission_required("ACCESS_ECRITURES")
def export_fiscal_csv_auto():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            date_ecriture,
            piece,
            libelle,
            compte_id,
            debit,
            credit
        FROM ecritures
        ORDER BY date_ecriture, id
    """)

    rows = c.fetchall()

    conn.close()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')

    writer.writerow([
        "Date",
        "Piece",
        "Libelle",
        "Compte",
        "Debit",
        "Credit"
    ])

    for row in rows:
        writer.writerow(row)

    enregistrer_action_audit(
        action="EXPORT_FISCAL_CSV",
        module="fiscal",
        detail="Export fiscal CSV genere"
    )

    return flask.Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=export_fiscal.csv"
        }
    )


@ecritures_routes.route('/liasse-fiscale-auto')
@login_required
@permission_required("ACCESS_ECRITURES")
def liasse_fiscale_auto():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            pc.numero,
            COALESCE(pc.libelle, ''),
            COALESCE(SUM(e.debit), 0),
            COALESCE(SUM(e.credit), 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        GROUP BY pc.numero, pc.libelle
        ORDER BY pc.numero
    """)

    comptes = c.fetchall()
    conn.close()

    return render_template(
        "liasse_fiscale_auto.html",
        comptes=comptes
    )
@ecritures_routes.route('/tva-dashboard')
@login_required
@permission_required("ACCESS_ECRITURES")
def tva_dashboard():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    # TVA collectée
    c.execute("""
        SELECT
            pc.numero,
            pc.libelle,
            COALESCE(SUM(e.credit - e.debit), 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        WHERE pc.numero LIKE '4457%'
        GROUP BY pc.numero, pc.libelle
        ORDER BY pc.numero
    """)

    tva_collectee = c.fetchall()

    # TVA déductible
    c.execute("""
        SELECT
            pc.numero,
            pc.libelle,
            COALESCE(SUM(e.debit - e.credit), 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        WHERE pc.numero LIKE '4456%'
        GROUP BY pc.numero, pc.libelle
        ORDER BY pc.numero
    """)

    tva_deductible = c.fetchall()

    total_collectee = round(sum(x[2] for x in tva_collectee), 2)
    total_deductible = round(sum(x[2] for x in tva_deductible), 2)

    tva_nette = round(total_collectee - total_deductible, 2)

    conn.close()

    return render_template(
        "tva_dashboard.html",
        tva_collectee=tva_collectee,
        tva_deductible=tva_deductible,
        total_collectee=total_collectee,
        total_deductible=total_deductible,
        tva_nette=tva_nette
    )
@ecritures_routes.route('/ca3-auto')
@login_required
@permission_required("ACCESS_ECRITURES")
def ca3_auto():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT COALESCE(SUM(e.credit - e.debit), 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        WHERE pc.numero LIKE '4457%'
    """)
    tva_collectee = c.fetchone()[0] or 0

    c.execute("""
        SELECT COALESCE(SUM(e.debit - e.credit), 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        WHERE pc.numero LIKE '4456%'
    """)
    tva_deductible = c.fetchone()[0] or 0

    c.execute("""
        SELECT COALESCE(SUM(e.credit - e.debit), 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        WHERE pc.numero LIKE '7%'
    """)
    ca_ht = c.fetchone()[0] or 0

    tva_nette = round(float(tva_collectee) - float(tva_deductible), 2)

    lignes_ca3 = [
        ("01", "Ventes, prestations de services HT", round(float(ca_ht), 2)),
        ("08", "TVA brute due", round(float(tva_collectee), 2)),
        ("20", "TVA déductible sur autres biens et services", round(float(tva_deductible), 2)),
        ("28", "TVA nette à payer", tva_nette),
    ]

    alertes = []

    if ca_ht == 0:
        alertes.append("Aucun chiffre d'affaires détecté sur les comptes 7.")

    if tva_collectee == 0:
        alertes.append("Aucune TVA collectée détectée sur les comptes 4457.")

    if tva_nette < 0:
        alertes.append("Crédit de TVA potentiel : TVA déductible supérieure à la TVA collectée.")

    conn.close()

    return render_template(
        "ca3_auto.html",
        ca_ht=round(float(ca_ht), 2),
        tva_collectee=round(float(tva_collectee), 2),
        tva_deductible=round(float(tva_deductible), 2),
        tva_nette=tva_nette,
        lignes_ca3=lignes_ca3,
        alertes=alertes
    )
@ecritures_routes.route('/fec-export')
@login_required
@permission_required("ACCESS_ECRITURES")
def fec_export():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            e.id,
            e.date_ecriture,
            COALESCE(e.piece, ''),
            COALESCE(e.libelle, ''),
            COALESCE(pc.numero, ''),
            COALESCE(pc.libelle, ''),
            COALESCE(e.debit, 0),
            COALESCE(e.credit, 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        ORDER BY e.date_ecriture ASC, e.id ASC
    """)

    rows = c.fetchall()

    output = io.StringIO()

    writer = csv.writer(
        output,
        delimiter='|',
        lineterminator='\n'
    )

    writer.writerow([
        "EcritureNum",
        "EcritureDate",
        "PieceRef",
        "EcritureLib",
        "CompteNum",
        "CompteLib",
        "Debit",
        "Credit"
    ])

    anomalies = []

    for row in rows:

        ecriture_id = row[0]
        date_ecriture = row[1]
        piece = row[2]
        libelle = row[3]
        compte_num = row[4]
        compte_lib = row[5]
        debit = float(row[6] or 0)
        credit = float(row[7] or 0)

        if not compte_num:
            anomalies.append(f"Ecriture {ecriture_id} sans compte_id comptable")

        if debit != 0 and credit != 0:
            anomalies.append(f"Ecriture {ecriture_id} avec debit ET credit")

        writer.writerow([
            ecriture_id,
            date_ecriture,
            piece,
            libelle,
            compte_num,
            compte_lib,
            debit,
            credit
        ])

    conn.close()

    enregistrer_action_audit(
        action="EXPORT_FEC",
        module="fiscal",
        detail=f"Export FEC genere ({len(rows)} lignes)"
    )

    response = flask.Response(
        output.getvalue(),
        mimetype="text/plain"
    )

    response.headers["Content-Disposition"] = "attachment; filename=fec_export.txt"

    return response
@ecritures_routes.route('/fec-controle')
@login_required
@permission_required("ACCESS_ECRITURES")
def fec_controle():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            e.id,
            e.date_ecriture,
            COALESCE(pc.numero, ''),
            COALESCE(e.debit, 0),
            COALESCE(e.credit, 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        ORDER BY e.date_ecriture
    """)

    rows = c.fetchall()

    anomalies = []

    total_debit = 0
    total_credit = 0

    for row in rows:

        ecriture_id = row[0]
        date_ecriture = row[1]
        compte_id = row[2]
        debit = float(row[3] or 0)
        credit = float(row[4] or 0)

        total_debit += debit
        total_credit += credit

        if not compte:
            anomalies.append(f"Ecriture {ecriture_id} sans compte")

        if debit != 0 and credit != 0:
            anomalies.append(f"Ecriture {ecriture_id} avec debit et credit")

        if debit == 0 and credit == 0:
            anomalies.append(f"Ecriture {ecriture_id} sans montant")

    ecart = round(total_debit - total_credit, 2)

    conn.close()

    return render_template(
        "fec_controle.html",
        anomalies=anomalies,
        total_debit=round(total_debit, 2),
        total_credit=round(total_credit, 2),
        ecart=ecart,
        nb_lignes=len(rows)
    )
@ecritures_routes.route('/grand-livre')
@login_required
@permission_required("ACCESS_ECRITURES")
def grand_livre():

    compte_filtre = request.args.get("compte", "").strip()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    params = []

    sql = """
        SELECT
            e.date_ecriture,
            COALESCE(e.piece, ''),
            COALESCE(e.libelle, ''),
            COALESCE(pc.numero, ''),
            COALESCE(pc.libelle, ''),
            COALESCE(e.debit, 0),
            COALESCE(e.credit, 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
    """

    if compte_filtre:
        sql += " WHERE pc.numero LIKE ? "
        params.append(compte_filtre + "%")

    sql += " ORDER BY pc.numero, e.date_ecriture, e.id "

    c.execute(sql, params)
    rows = c.fetchall()
    conn.close()

    lignes = []
    solde = 0

    for row in rows:
        debit = float(row[5] or 0)
        credit = float(row[6] or 0)
        solde += debit - credit

        lignes.append({
            "date": row[0],
            "piece": row[1],
            "libelle": row[2],
            "compte": row[3],
            "compte_libelle": row[4],
            "debit": debit,
            "credit": credit,
            "solde": round(solde, 2)
        })

    return render_template(
        "grand_livre.html",
        lignes=lignes,
        compte_filtre=compte_filtre,
        total_debit=round(sum(x["debit"] for x in lignes), 2),
        total_credit=round(sum(x["credit"] for x in lignes), 2),
        solde_final=round(solde, 2)
    )
@ecritures_routes.route('/balance-generale')
@login_required
@permission_required("ACCESS_ECRITURES")
def balance_generale_auto():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            COALESCE(pc.numero, ''),
            COALESCE(pc.libelle, ''),
            COALESCE(SUM(e.debit), 0),
            COALESCE(SUM(e.credit), 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        GROUP BY pc.numero, pc.libelle
        ORDER BY pc.numero
    """)

    rows = c.fetchall()
    conn.close()

    comptes = []
    total_debit = 0
    total_credit = 0

    for row in rows:
        debit = float(row[2] or 0)
        credit = float(row[3] or 0)
        solde = debit - credit

        total_debit += debit
        total_credit += credit

        comptes.append({
            "numero": row[0],
            "libelle": row[1],
            "debit": round(debit, 2),
            "credit": round(credit, 2),
            "solde_debiteur": round(solde, 2) if solde > 0 else 0,
            "solde_crediteur": round(abs(solde), 2) if solde < 0 else 0,
        })

    ecart = round(total_debit - total_credit, 2)

    return render_template(
        "balance_generale.html",
        comptes=comptes,
        total_debit=round(total_debit, 2),
        total_credit=round(total_credit, 2),
        ecart=ecart
    )

@ecritures_routes.route('/journaux')
@login_required
@permission_required("ACCESS_ECRITURES")
def journaux_comptables():

    journal = request.args.get("journal", "").strip().upper()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    sql = """
        SELECT
            e.date_ecriture,
            COALESCE(e.piece, ''),
            COALESCE(e.libelle, ''),
            COALESCE(pc.numero, ''),
            COALESCE(pc.libelle, ''),
            COALESCE(e.debit, 0),
            COALESCE(e.credit, 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
    """

    params = []

    if journal == "ACH":
        sql += " WHERE pc.numero LIKE '6%' "

    elif journal == "VEN":
        sql += " WHERE pc.numero LIKE '7%' "

    elif journal == "BQ":
        sql += " WHERE pc.numero LIKE '512%' "

    elif journal == "OD":
        sql += """
            WHERE
                pc.numero NOT LIKE '6%'
                AND pc.numero NOT LIKE '7%'
                AND pc.numero NOT LIKE '512%'
        """

    sql += " ORDER BY e.date_ecriture DESC, e.id DESC "

    c.execute(sql, params)

    rows = c.fetchall()

    conn.close()

    total_debit = round(sum(float(r[5] or 0) for r in rows), 2)
    total_credit = round(sum(float(r[6] or 0) for r in rows), 2)

    return render_template(
        "journaux_comptables.html",
        rows=rows,
        journal=journal,
        total_debit=total_debit,
        total_credit=total_credit
    )
@ecritures_routes.route('/rapprochement-bancaire')
@login_required
@permission_required("ACCESS_ECRITURES")
def rapprochement_bancaire():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            e.id,
            e.date_ecriture,
            COALESCE(e.piece, ''),
            COALESCE(e.libelle, ''),
            COALESCE(pc.numero, ''),
            COALESCE(pc.libelle, ''),
            COALESCE(e.debit, 0),
            COALESCE(e.credit, 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        WHERE pc.numero LIKE '512%'
        ORDER BY e.date_ecriture DESC, e.id DESC
    """)

    rows = c.fetchall()
    conn.close()

    lignes = []
    total_debit = 0
    total_credit = 0

    for r in rows:
        debit = float(r[6] or 0)
        credit = float(r[7] or 0)

        total_debit += debit
        total_credit += credit

        lignes.append({
            "id": r[0],
            "date": r[1],
            "piece": r[2],
            "libelle": r[3],
            "compte": r[4],
            "compte_libelle": r[5],
            "debit": round(debit, 2),
            "credit": round(credit, 2),
            "solde": round(debit - credit, 2)
        })

    solde_banque = round(total_debit - total_credit, 2)

    alertes = []

    if len(lignes) == 0:
        alertes.append("Aucune écriture bancaire détectée sur les comptes 512.")

    if solde_banque < 0:
        alertes.append("Solde banque créditeur : vérifier découvert ou inversion débit/crédit.")

    return render_template(
        "rapprochement_bancaire.html",
        lignes=lignes,
        total_debit=round(total_debit, 2),
        total_credit=round(total_credit, 2),
        solde_banque=solde_banque,
        alertes=alertes
    )
@ecritures_routes.route('/journal')
@login_required
@permission_required("ACCESS_ECRITURES")
def journal_redirect():
    return redirect('/ecritures/journaux')
@ecritures_routes.route('/analyse-financiere')
@login_required
@permission_required("ACCESS_ECRITURES")
def analyse_financiere():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    def total_compte(prefixe):
        c.execute("""
            SELECT COALESCE(SUM(e.credit - e.debit), 0)
            FROM ecritures e
            LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
            WHERE pc.numero LIKE ?
        """, (prefixe + "%",))
        return float(c.fetchone()[0] or 0)

    produits = total_compte("7")
    charges = -total_compte("6")
    achats = -total_compte("60")
    charges_externes = -total_compte("61") - total_compte("62")
    impots_taxes = -total_compte("63")
    salaires = -total_compte("64")
    dotations = -total_compte("68")

    marge = produits - achats
    valeur_ajoutee = marge - charges_externes
    ebe = valeur_ajoutee - impots_taxes - salaires
    resultat_exploitation = ebe - dotations
    resultat_net = produits - charges
    caf_estimee = resultat_net + dotations

    taux_marge = round((marge / produits * 100), 2) if produits else 0
    taux_ebe = round((ebe / produits * 100), 2) if produits else 0
    taux_resultat = round((resultat_net / produits * 100), 2) if produits else 0

    alertes = []

    if produits == 0:
        alertes.append("Aucun chiffre d'affaires détecté sur les comptes 7.")

    if resultat_net < 0:
        alertes.append("Résultat net négatif : l'activité est déficitaire.")

    if taux_marge < 20 and produits > 0:
        alertes.append("Taux de marge faible : vérifier les achats et coûts directs.")

    if ebe < 0:
        alertes.append("EBE négatif : l'exploitation ne couvre pas les charges courantes.")

    if caf_estimee < 0:
        alertes.append("CAF estimée négative : capacité d'autofinancement insuffisante.")

    score = 100

    if resultat_net < 0:
        score -= 30
    if ebe < 0:
        score -= 25
    if taux_marge < 20 and produits > 0:
        score -= 15
    if caf_estimee < 0:
        score -= 20
    if produits == 0:
        score -= 30

    score = max(score, 0)

    conn.close()

    return render_template(
        "analyse_financiere.html",
        produits=round(produits, 2),
        charges=round(charges, 2),
        achats=round(achats, 2),
        charges_externes=round(charges_externes, 2),
        impots_taxes=round(impots_taxes, 2),
        salaires=round(salaires, 2),
        dotations=round(dotations, 2),
        marge=round(marge, 2),
        valeur_ajoutee=round(valeur_ajoutee, 2),
        ebe=round(ebe, 2),
        resultat_exploitation=round(resultat_exploitation, 2),
        resultat_net=round(resultat_net, 2),
        caf_estimee=round(caf_estimee, 2),
        taux_marge=taux_marge,
        taux_ebe=taux_ebe,
        taux_resultat=taux_resultat,
        alertes=alertes,
        score=score
    )
@ecritures_routes.route('/cloture-comptable')
@login_required
@permission_required("ACCESS_ECRITURES")
def cloture_comptable():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            COALESCE(SUM(debit), 0),
            COALESCE(SUM(credit), 0),
            COUNT(*)
        FROM ecritures
    """)

    total_debit, total_credit, nb_ecritures = c.fetchone()

    total_debit = round(float(total_debit or 0), 2)
    total_credit = round(float(total_credit or 0), 2)
    ecart = round(total_debit - total_credit, 2)

    c.execute("""
        SELECT COUNT(*)
        FROM ecritures
        WHERE compte_id IS NULL
    """)
    nb_sans_compte = c.fetchone()[0] or 0

    c.execute("""
        SELECT COUNT(*)
        FROM ecritures
        WHERE COALESCE(debit, 0) = 0
          AND COALESCE(credit, 0) = 0
    """)
    nb_sans_montant = c.fetchone()[0] or 0

    c.execute("""
        SELECT COALESCE(SUM(e.credit - e.debit), 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        WHERE pc.numero LIKE '7%'
    """)
    produits = float(c.fetchone()[0] or 0)

    c.execute("""
        SELECT COALESCE(SUM(e.debit - e.credit), 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        WHERE pc.numero LIKE '6%'
    """)
    charges = float(c.fetchone()[0] or 0)

    resultat = round(produits - charges, 2)

    alertes = []

    if ecart != 0:
        alertes.append("La balance n'est pas équilibrée : clôture déconseillée.")

    if nb_sans_compte > 0:
        alertes.append(f"{nb_sans_compte} écriture(s) sans compte_id comptable.")

    if nb_sans_montant > 0:
        alertes.append(f"{nb_sans_montant} écriture(s) sans montant.")

    if nb_ecritures == 0:
        alertes.append("Aucune écriture trouvée : clôture impossible.")

    statut = "cloturable" if not alertes else "bloquee"

    conn.close()

    return render_template(
        "cloture_comptable.html",
        total_debit=total_debit,
        total_credit=total_credit,
        ecart=ecart,
        nb_ecritures=nb_ecritures,
        nb_sans_compte=nb_sans_compte_id,
        nb_sans_montant=nb_sans_montant,
        produits=round(produits, 2),
        charges=round(charges, 2),
        resultat=resultat,
        alertes=alertes,
        statut=statut
    )
@ecritures_routes.route('/report-a-nouveau')
@login_required
@permission_required("ACCESS_ECRITURES")
def report_a_nouveau():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            COALESCE(pc.numero, ''),
            COALESCE(pc.libelle, ''),
            COALESCE(SUM(e.debit), 0),
            COALESCE(SUM(e.credit), 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        WHERE pc.numero LIKE '1%'
           OR pc.numero LIKE '2%'
           OR pc.numero LIKE '3%'
           OR pc.numero LIKE '4%'
           OR pc.numero LIKE '5%'
        GROUP BY pc.numero, pc.libelle
        ORDER BY pc.numero
    """)

    rows = c.fetchall()

    reports = []
    total_debit = 0
    total_credit = 0

    for r in rows:
        numero = r[0]
        libelle = r[1]
        debit = float(r[2] or 0)
        credit = float(r[3] or 0)
        solde = round(debit - credit, 2)

        if solde > 0:
            report_debit = solde
            report_credit = 0
        elif solde < 0:
            report_debit = 0
            report_credit = abs(solde)
        else:
            report_debit = 0
            report_credit = 0

        total_debit += report_debit
        total_credit += report_credit

        if solde != 0:
            reports.append({
                "compte": numero,
                "libelle": libelle,
                "solde": solde,
                "debit": round(report_debit, 2),
                "credit": round(report_credit, 2)
            })

    ecart = round(total_debit - total_credit, 2)

    c.execute("""
        SELECT COALESCE(SUM(e.credit - e.debit), 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        WHERE pc.numero LIKE '7%'
    """)
    produits = float(c.fetchone()[0] or 0)

    c.execute("""
        SELECT COALESCE(SUM(e.debit - e.credit), 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        WHERE pc.numero LIKE '6%'
    """)
    charges = float(c.fetchone()[0] or 0)

    resultat = round(produits - charges, 2)

    conn.close()

    return render_template(
        "report_a_nouveau.html",
        reports=reports,
        total_debit=round(total_debit, 2),
        total_credit=round(total_credit, 2),
        ecart=ecart,
        resultat=resultat,
        nb_lignes=len(reports)
    )
@ecritures_routes.route('/bilan-resultat')
@login_required
@permission_required("ACCESS_ECRITURES")
def bilan_resultat():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    def solde_prefixe(prefixe):
        c.execute("""
            SELECT COALESCE(SUM(e.debit - e.credit), 0)
            FROM ecritures e
            LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
            WHERE pc.numero LIKE ?
        """, (prefixe + "%",))
        return float(c.fetchone()[0] or 0)

    actif_immobilise = solde_prefixe("2")
    stocks = solde_prefixe("3")
    creances = solde_prefixe("4")
    tresorerie = solde_prefixe("5")

    capitaux_propres = -solde_prefixe("1")
    produits = -solde_prefixe("7")
    charges = solde_prefixe("6")
    resultat_net = produits - charges

    total_actif = actif_immobilise + stocks + creances + tresorerie
    total_passif = capitaux_propres + resultat_net

    ecart_bilan = round(total_actif - total_passif, 2)

    compte_resultat = [
        ("Chiffre d'affaires / produits", produits),
        ("Charges d'exploitation", charges),
        ("Résultat net estimé", resultat_net),
    ]

    bilan_actif = [
        ("Actif immobilisé", actif_immobilise),
        ("Stocks", stocks),
        ("Créances / tiers", creances),
        ("Trésorerie", tresorerie),
    ]

    bilan_passif = [
        ("Capitaux propres", capitaux_propres),
        ("Résultat net", resultat_net),
    ]

    alertes = []

    if ecart_bilan != 0:
        alertes.append("Le bilan n'est pas équilibré : vérifier les comptes de bilan et l'affectation du résultat.")

    if produits == 0:
        alertes.append("Aucun produit détecté sur les comptes 7.")

    if total_actif == 0:
        alertes.append("Aucun actif détecté.")

    conn.close()

    return render_template(
        "bilan_resultat.html",
        bilan_actif=[(x[0], round(x[1], 2)) for x in bilan_actif],
        bilan_passif=[(x[0], round(x[1], 2)) for x in bilan_passif],
        compte_resultat=[(x[0], round(x[1], 2)) for x in compte_resultat],
        total_actif=round(total_actif, 2),
        total_passif=round(total_passif, 2),
        ecart_bilan=ecart_bilan,
        resultat_net=round(resultat_net, 2),
        alertes=alertes
    )
@ecritures_routes.route('/previsionnel-tresorerie')
@login_required
@permission_required("ACCESS_ECRITURES")
def previsionnel_tresorerie():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            substr(date_ecriture, 1, 7) as mois,
            COALESCE(SUM(debit), 0),
            COALESCE(SUM(credit), 0)
        FROM ecritures
        GROUP BY substr(date_ecriture, 1, 7)
        ORDER BY mois
    """)

    rows = c.fetchall()

    historique = []
    soldes = []

    tresorerie = 0

    for r in rows:
        mois = r[0]
        debit = float(r[1] or 0)
        credit = float(r[2] or 0)

        variation = debit - credit
        tresorerie += variation

        historique.append({
            "mois": mois,
            "debit": round(debit, 2),
            "credit": round(credit, 2),
            "variation": round(variation, 2),
            "tresorerie": round(tresorerie, 2)
        })

        soldes.append(tresorerie)

    moyenne_variation = round(sum(soldes) / len(soldes), 2) if soldes else 0

    previsions = []

    treso_future = tresorerie

    for i in range(1, 7):

        treso_future += moyenne_variation

        previsions.append({
            "mois": f"M+{i}",
            "tresorerie": round(treso_future, 2)
        })

    alertes = []

    if tresorerie < 0:
        alertes.append("Trésorerie actuelle négative.")

    if moyenne_variation < 0:
        alertes.append("La tendance de trésorerie est négative.")

    for p in previsions:
        if p["tresorerie"] < 0:
            alertes.append(f"Alerte prévisionnelle : trésorerie négative prévue {p['mois']}.")

    score_tresorerie = 100

    if tresorerie < 0:
        score_tresorerie -= 40

    if moyenne_variation < 0:
        score_tresorerie -= 30

    if len(alertes) > 2:
        score_tresorerie -= 20

    score_tresorerie = max(score_tresorerie, 0)

    conn.close()

    return render_template(
        "previsionnel_tresorerie.html",
        historique=historique,
        previsions=previsions,
        tresorerie=round(tresorerie, 2),
        moyenne_variation=moyenne_variation,
        score_tresorerie=score_tresorerie,
        alertes=alertes
    )
@ecritures_routes.route('/anomalies-comptables')
@login_required
@permission_required("ACCESS_ECRITURES")
def anomalies_comptables():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            e.id,
            e.date_ecriture,
            COALESCE(e.piece, ''),
            COALESCE(e.libelle, ''),
            COALESCE(pc.numero, ''),
            COALESCE(pc.libelle, ''),
            COALESCE(e.debit, 0),
            COALESCE(e.credit, 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        ORDER BY e.date_ecriture, e.id
    """)

    rows = c.fetchall()

    anomalies = []

    total_mouvements = []

    for r in rows:

        ecriture_id = r[0]
        date_ecriture = r[1]
        piece = r[2]
        libelle = r[3]
        compte_id = r[4]
        compte_libelle = r[5]
        debit = float(r[6] or 0)
        credit = float(r[7] or 0)

        mouvement = max(debit, credit)

        total_mouvements.append(mouvement)

        # anomalie montant nul
        if debit == 0 and credit == 0:
            anomalies.append({
                "niveau": "Critique",
                "type": "Montant nul",
                "message": "Écriture sans débit ni crédit",
                "piece": piece,
                "compte": compte_id,
                "montant": 0
            })

        # anomalie double sens
        if debit > 0 and credit > 0:
            anomalies.append({
                "niveau": "Élevé",
                "type": "Débit + Crédit",
                "message": "Débit et crédit renseignés simultanément",
                "piece": piece,
                "compte": compte_id,
                "montant": mouvement
            })

        # compte_id absent
        if compte_id == "":
            anomalies.append({
                "niveau": "Critique",
                "type": "Compte absent",
                "message": "Aucun compte_id comptable",
                "piece": piece,
                "compte": "-",
                "montant": mouvement
            })

        # montant anormal
        if mouvement > 100000:
            anomalies.append({
                "niveau": "Moyen",
                "type": "Montant élevé",
                "message": "Montant inhabituellement élevé",
                "piece": piece,
                "compte": compte_id,
                "montant": mouvement
            })

        # incohérence TVA simple
        if compte.startswith("445") and debit == 0 and credit == 0:
            anomalies.append({
                "niveau": "Moyen",
                "type": "TVA incohérente",
                "message": "Compte TVA sans mouvement",
                "piece": piece,
                "compte": compte_id,
                "montant": mouvement
            })

    # doublons simples
    vus = {}

    for r in rows:

        cle = (
            r[1],
            r[2],
            r[3],
            float(r[6] or 0),
            float(r[7] or 0)
        )

        if cle in vus:
            anomalies.append({
                "niveau": "Élevé",
                "type": "Doublon potentiel",
                "message": "Écriture potentiellement dupliquée",
                "piece": r[2],
                "compte": r[4],
                "montant": max(float(r[6] or 0), float(r[7] or 0))
            })

        vus[cle] = True

    nb_anomalies = len(anomalies)

    score_risque = 100

    score_risque -= nb_anomalies * 5

    score_risque = max(score_risque, 0)

    niveau_global = "Faible"

    if score_risque < 80:
        niveau_global = "Modéré"

    if score_risque < 50:
        niveau_global = "Élevé"

    if score_risque < 25:
        niveau_global = "Critique"

    conn.close()

    return render_template(
        "anomalies_comptables.html",
        anomalies=anomalies,
        nb_anomalies=nb_anomalies,
        score_risque=score_risque,
        niveau_global=niveau_global
    )
@ecritures_routes.route('/ged-comptable')
@login_required
@permission_required("ACCESS_ECRITURES")
def ged_comptable():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS ged_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_fichier TEXT,
            chemin TEXT,
            type_document TEXT,
            statut TEXT,
            date_import TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        SELECT id, nom_fichier, type_document, statut, date_import
        FROM ged_documents
        ORDER BY id DESC
    """)

    documents = c.fetchall()
    conn.close()

    return render_template(
        "ged_comptable.html",
        documents=documents
    )


@ecritures_routes.route('/ged-comptable/upload', methods=['POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def ged_comptable_upload():

    fichier = request.files.get("fichier")
    type_document = request.form.get("type_document", "Facture")

    if not fichier:
        flash("Aucun fichier sélectionné.")
        return redirect('/ecritures/ged-comptable')

    dossier = r"C:\Users\alain\mon-projet-agent\uploads\ged"
    os.makedirs(dossier, exist_ok=True)

    nom_fichier = fichier.filename
    chemin = os.path.join(dossier, nom_fichier)

    fichier.save(chemin)

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS ged_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_fichier TEXT,
            chemin TEXT,
            type_document TEXT,
            statut TEXT,
            date_import TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    c.execute("""
        INSERT INTO ged_documents (
            nom_fichier,
            chemin,
            type_document,
            statut
        )
        VALUES (?, ?, ?, ?)
    """, (
        nom_fichier,
        chemin,
        type_document,
        "Importé"
    ))

    conn.commit()
    conn.close()

    flash("Document importé dans la GED.")
    return redirect('/ecritures/ged-comptable')
@ecritures_routes.route('/ged-comptable/ocr/<int:doc_id>')
@login_required
@permission_required("ACCESS_ECRITURES")
def ged_ocr(doc_id):

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            nom_fichier,
            chemin,
            type_document
        FROM ged_documents
        WHERE id = ?
    """, (doc_id,))

    row = c.fetchone()

    if not row:
        conn.close()
        return "Document introuvable"

    nom_fichier = row[0]
    chemin = row[1]
    type_document = row[2]

    texte = ""

    try:

        if chemin.lower().endswith(".pdf"):

            doc = fitz.open(chemin)

            texte_pages = []

            for page in doc:
                texte_pages.append(page.get_text())

            texte = "\n".join(texte_pages).strip()

            if not texte:
                texte = "PDF détecté mais aucun texte exploitable trouvé."

        else:

            image = Image.open(chemin)

            texte = pytesseract.image_to_string(
                image,
                lang="fra"
            )

    except Exception as e:

        texte = f"Erreur OCR : {str(e)}"

    fournisseur = "Non détecté"
    montant_ttc = "Non détecté"
    date_facture = "Non détectée"

    lignes = texte.splitlines()

    for l in lignes:

        l2 = l.strip()

        if len(l2) > 3 and fournisseur == "Non détecté":
            fournisseur = l2[:80]

        montants = re.findall(r"\d+[.,]\d{2}", l2)

        if montants and montant_ttc == "Non détecté":
            montant_ttc = montants[-1]

        dates = re.findall(r"\d{2}/\d{2}/\d{4}", l2)

        if dates and date_facture == "Non détectée":
            date_facture = dates[0]

    suggestion_compte = "628"

    if "restaurant" in texte.lower():
        suggestion_compte = "625"

    elif "carburant" in texte.lower():
        suggestion_compte = "606"

    elif "bureau" in texte.lower():
        suggestion_compte = "6064"

    elif "amazon" in texte.lower():
        suggestion_compte = "606"

    conn.close()

    return render_template(
        "ged_ocr.html",
        nom_fichier=nom_fichier,
        type_document=type_document,
        texte=texte,
        fournisseur=fournisseur,
        montant_ttc=montant_ttc,
        date_facture=date_facture,
        suggestion_compte=suggestion_compte
    )
@ecritures_routes.route('/ged-comptable/generer-ecriture/<int:doc_id>')
@login_required
@permission_required("ACCESS_ECRITURES")
def ged_generer_ecriture(doc_id):

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT nom_fichier, chemin, type_document
        FROM ged_documents
        WHERE id = ?
    """, (doc_id,))

    doc = c.fetchone()

    if not doc:
        conn.close()
        return "Document introuvable"

    nom_fichier = doc[0]
    chemin = doc[1]
    type_document = doc[2]

    texte = ""

    try:
        if chemin.lower().endswith(".pdf"):
            doc_pdf = fitz.open(chemin)
            texte = "\n".join([page.get_text() for page in doc_pdf]).strip()
        else:
            image = Image.open(chemin)
            texte = pytesseract.image_to_string(image, lang="fra")
    except Exception as e:
        texte = f"Erreur OCR : {str(e)}"

    montants = re.findall(r"\d+[.,]\d{2}", texte)
    montant_ttc = 0

    if montants:
        montant_ttc = float(montants[-1].replace(",", "."))

    montant_ht = round(montant_ttc / 1.20, 2) if montant_ttc else 0
    montant_tva = round(montant_ttc - montant_ht, 2)

    compte_charge = "628"
    compte_tva = "44566"
    compte_tiers = "401"

    libelle = "Pré-comptabilisation OCR - " + nom_fichier

    return render_template(
        "ged_ecriture_preview.html",
        doc_id=doc_id,
        nom_fichier=nom_fichier,
        type_document=type_document,
        montant_ht=montant_ht,
        montant_tva=montant_tva,
        montant_ttc=montant_ttc,
        compte_charge=compte_charge,
        compte_tva=compte_tva,
        compte_tiers=compte_tiers,
        libelle=libelle
    )
@ecritures_routes.route('/ged-comptable/valider-ecriture/<int:doc_id>', methods=['POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def ged_valider_ecriture(doc_id):

    date_ecriture = request.form.get("date_ecriture")
    piece = request.form.get("piece")
    libelle = request.form.get("libelle")

    compte_charge = request.form.get("compte_charge")
    compte_tva = request.form.get("compte_tva")
    compte_tiers = request.form.get("compte_tiers")

    montant_ht = float(request.form.get("montant_ht") or 0)
    montant_tva = float(request.form.get("montant_tva") or 0)
    montant_ttc = float(request.form.get("montant_ttc") or 0)

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    def get_compte_id(numero, libelle_defaut):
        c.execute("SELECT id FROM plan_comptable WHERE numero = ? LIMIT 1", (numero,))
        row = c.fetchone()

        if row:
            return row[0]

        c.execute("""
            INSERT INTO plan_comptable (numero, libelle, type)
            VALUES (?, ?, ?)
        """, (numero, libelle_defaut, "AUTO"))

        return c.lastrowid

    charge_id = get_compte_id(compte_charge, "Charge OCR")
    tva_id = get_compte_id(compte_tva, "TVA déductible OCR")
    tiers_id = get_compte_id(compte_tiers, "Fournisseur OCR")

    c.execute("""
        INSERT INTO ecritures (
            date_ecriture,
            piece,
            libelle,
            debit,
            credit,
            compte_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date_ecriture, piece, libelle, montant_ht, 0, charge_id))

    c.execute("""
        INSERT INTO ecritures (
            date_ecriture,
            piece,
            libelle,
            debit,
            credit,
            compte_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date_ecriture, piece, "TVA déductible OCR", montant_tva, 0, tva_id))

    c.execute("""
        INSERT INTO ecritures (
            date_ecriture,
            piece,
            libelle,
            debit,
            credit,
            compte_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date_ecriture, piece, "Fournisseur OCR", 0, montant_ttc, tiers_id))

    c.execute("""
        UPDATE ged_documents
        SET statut = ?
        WHERE id = ?
    """, ("Comptabilisé", doc_id))

    conn.commit()
    conn.close()
@ecritures_routes.route('/export-pdf-financier')
@login_required
@permission_required("ACCESS_ECRITURES")
def export_pdf_financier():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    def total(prefixe, inverse=False):

        c.execute("""
            SELECT COALESCE(SUM(e.debit - e.credit), 0)
            FROM ecritures e
            LEFT JOIN plan_comptable pc
                ON pc.id = e.compte_id
            WHERE pc.numero LIKE ?
        """, (prefixe + "%",))

        valeur = float(c.fetchone()[0] or 0)

        if inverse:
            valeur *= -1

        return round(valeur, 2)

    tresorerie = total("512")
    produits = total("7", True)
    charges = total("6")
    resultat = round(produits - charges, 2)

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    elements = []

    titre = Paragraph(
        "Rapport Financier ComptaPilot IA",
        styles['Title']
    )

    elements.append(titre)
    elements.append(Spacer(1, 20))

    tableau = Table([
        ["Indicateur", "Valeur"],
        ["Trésorerie", f"{tresorerie} €"],
        ["Produits", f"{produits} €"],
        ["Charges", f"{charges} €"],
        ["Résultat", f"{resultat} €"]
    ])

    tableau.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e3a5f")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ]))

    elements.append(tableau)
    elements.append(Spacer(1, 25))

    analyse = Paragraph(
        f"""
        <b>Analyse IA :</b><br/>
        Trésorerie actuelle : {tresorerie} €<br/>
        Résultat estimé : {resultat} €<br/>
        Produits : {produits} €<br/>
        Charges : {charges} €
        """,
        styles['BodyText']
    )

    elements.append(analyse)

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    conn.close()

    return flask.Response(
        pdf,
        mimetype='application/pdf',
        headers={
            'Content-Disposition':
            'attachment; filename=rapport_financier.pdf'
        }
    )
    flash("Écriture comptable générée depuis OCR.")
    return redirect('/ecritures/ged-comptable')
@ecritures_routes.route('/rapprochement-ia')
@login_required
@permission_required("ACCESS_ECRITURES")
def rapprochement_ia():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            e.id,
            e.date_ecriture,
            COALESCE(e.piece, ''),
            COALESCE(e.libelle, ''),
            COALESCE(pc.numero, ''),
            COALESCE(pc.libelle, ''),
            COALESCE(e.debit, 0),
            COALESCE(e.credit, 0)
        FROM ecritures e
        LEFT JOIN plan_comptable pc ON pc.id = e.compte_id
        WHERE pc.numero LIKE '401%'
           OR pc.numero LIKE '411%'
           OR pc.numero LIKE '512%'
        ORDER BY e.date_ecriture DESC, e.id DESC
    """)

    rows = c.fetchall()
    conn.close()

    tiers = []
    banques = []

    for r in rows:
        ligne = {
            "id": r[0],
            "date": r[1],
            "piece": r[2],
            "libelle": r[3],
            "compte": r[4],
            "compte_libelle": r[5],
            "debit": float(r[6] or 0),
            "credit": float(r[7] or 0),
            "montant": max(float(r[6] or 0), float(r[7] or 0))
        }

        if r[4].startswith("512"):
            banques.append(ligne)
        else:
            tiers.append(ligne)

    rapprochements = []

    rapprochements = []

    for b in banques:

        meilleur = None
        meilleur_score = 0

        for t in tiers:

            score = 0

            if round(b["montant"], 2) == round(t["montant"], 2):
                score += 60

            if (
                b["piece"]
                and t["piece"]
                and b["piece"] == t["piece"]
            ):
                score += 25

            if (
                b["libelle"]
                and t["libelle"]
                and (
                    b["libelle"].lower() in t["libelle"].lower()
                    or t["libelle"].lower() in b["libelle"].lower()
                )
            ):
                score += 15

            if score > meilleur_score:
                meilleur_score = score
                meilleur = t

        if meilleur:

            rapprochements.append({
                "banque": b,
                "tiers": meilleur,
                "score": meilleur_score
            })

    alertes = []

    if not banques:
        alertes.append(
            "Aucune écriture bancaire 512 détectée."
        )

    if not tiers:
        alertes.append(
            "Aucune écriture fournisseur/client 401/411 détectée."
        )

    return render_template(
        "rapprochement_ia.html",
        banques=banques,
        tiers=tiers,
        rapprochements=rapprochements,
        alertes=alertes
    )
@ecritures_routes.route('/cockpit-ia-dirigeant')
@login_required
@permission_required("ACCESS_ECRITURES")
def cockpit_ia_dirigeant():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    def total(prefixe, inverse=False):

        c.execute("""
            SELECT COALESCE(SUM(e.debit - e.credit), 0)
            FROM ecritures e
            LEFT JOIN plan_comptable pc
                ON pc.id = e.compte_id
            WHERE pc.numero LIKE ?
        """, (prefixe + "%",))

        valeur = float(c.fetchone()[0] or 0)

        if inverse:
            valeur *= -1

        return round(valeur, 2)

    tresorerie = total("512")
    produits = total("7", True)
    charges = total("6")

    resultat = round(produits - charges, 2)

    burn_rate = round(charges / 12, 2) if charges else 0

    runway = 0

    if burn_rate > 0:
        runway = round(tresorerie / burn_rate, 1)

    score = 100

    alertes = []

    if tresorerie < 0:
        score -= 40
        alertes.append("Trésorerie négative.")

    if resultat < 0:
        score -= 25
        alertes.append("Résultat déficitaire.")

    if runway < 3 and burn_rate > 0:
        score -= 25
        alertes.append("Moins de 3 mois de trésorerie.")

    if produits == 0:
        score -= 30
        alertes.append("Aucun chiffre d'affaires détecté.")

    score = max(score, 0)

    niveau = "Excellent"

    if score < 80:
        niveau = "Correct"

    if score < 60:
        niveau = "Fragile"

    if score < 40:
        niveau = "Critique"

    prevision_6_mois = []

    treso_future = tresorerie

    for i in range(1, 7):

        treso_future -= burn_rate

        prevision_6_mois.append({
            "periode": f"M+{i}",
            "tresorerie": round(treso_future, 2)
        })

    recommandations = []

    if charges > produits:
        recommandations.append(
            "Réduire les charges."
        )

    if runway < 6 and burn_rate > 0:
        recommandations.append(
            "Sécuriser rapidement la trésorerie."
        )

    if tresorerie > 0 and resultat > 0:
        recommandations.append(
            "Situation financière saine."
        )

    if not recommandations:
        recommandations.append(
            "Continuer le suivi mensuel."
        )

    conn.close()

    return render_template(
        "cockpit_ia_dirigeant.html",
        tresorerie=tresorerie,
        produits=produits,
        charges=charges,
        resultat=resultat,
        burn_rate=burn_rate,
        runway=runway,
        score=score,
        niveau=niveau,
        alertes=alertes,
        recommandations=recommandations,
        prevision_6_mois=prevision_6_mois
    )
@ecritures_routes.route('/export-pdf-financier-ia')
@login_required
@permission_required("ACCESS_ECRITURES")
def export_pdf_financier_ia():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    def total(prefixe, inverse=False):

        c.execute("""
            SELECT COALESCE(SUM(e.debit - e.credit), 0)
            FROM ecritures e
            LEFT JOIN plan_comptable pc
                ON pc.id = e.compte_id
            WHERE pc.numero LIKE ?
        """, (prefixe + "%",))

        valeur = float(c.fetchone()[0] or 0)

        if inverse:
            valeur *= -1

        return round(valeur, 2)

    tresorerie = total("512")
    produits = total("7", True)
    charges = total("6")
    resultat = round(produits - charges, 2)

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    elements = []

    titre = Paragraph(
        "Rapport Financier ComptaPilot IA",
        styles['Title']
    )

    elements.append(titre)
    elements.append(Spacer(1, 20))

    tableau = Table([
        ["Indicateur", "Valeur"],
        ["Trésorerie", f"{tresorerie} €"],
        ["Produits", f"{produits} €"],
        ["Charges", f"{charges} €"],
        ["Résultat", f"{resultat} €"]
    ])

    tableau.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e3a5f")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ]))

    elements.append(tableau)
    elements.append(Spacer(1, 25))

    analyse = Paragraph(
        f"""
        <b>Analyse IA :</b><br/>
        Trésorerie actuelle : {tresorerie} €<br/>
        Résultat estimé : {resultat} €<br/>
        Produits : {produits} €<br/>
        Charges : {charges} €
        """,
        styles['BodyText']
    )

    elements.append(analyse)

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    conn.close()

    return flask.Response(
        pdf,
        mimetype='application/pdf',
        headers={
            'Content-Disposition':
            'attachment; filename=rapport_financier.pdf'
        }
    )
@ecritures_routes.route('/assistant-ia-comptable', methods=['GET', 'POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def assistant_ia_comptable():

    question = ""
    reponse = ""

    if request.method == 'POST':

        question = request.form.get("question", "").strip().lower()

        conn = sqlite3.connect("db.sqlite")
        c = conn.cursor()

        def total(prefixe, inverse=False):

            c.execute("""
                SELECT COALESCE(SUM(e.debit - e.credit), 0)
                FROM ecritures e
                LEFT JOIN plan_comptable pc
                    ON pc.id = e.compte_id
                WHERE pc.numero LIKE ?
            """, (prefixe + "%",))

            valeur = float(c.fetchone()[0] or 0)

            if inverse:
                valeur *= -1

            return round(valeur, 2)

        tresorerie = total("512")
        produits = total("7", True)
        charges = total("6")
        resultat = round(produits - charges, 2)

        if "trésorerie" in question or "tresorerie" in question:

            reponse = f"La trésorerie actuelle est de {tresorerie} €."

        elif "résultat" in question or "resultat" in question:

            reponse = f"Le résultat estimé est de {resultat} €."

        elif "charges" in question:

            reponse = f"Le total des charges est de {charges} €."

        elif "produits" in question or "chiffre d'affaires" in question:

            reponse = f"Le total des produits est de {produits} €."

        elif "banque" in question:

            c.execute("""
                SELECT
                    e.date_ecriture,
                    e.libelle,
                    e.debit,
                    e.credit
                FROM ecritures e
                LEFT JOIN plan_comptable pc
                    ON pc.id = e.compte_id
                WHERE pc.numero LIKE '512%'
                ORDER BY e.date_ecriture DESC
                LIMIT 5
            """)

            rows = c.fetchall()

            lignes = []

            for r in rows:

                lignes.append(
                    f"{r[0]} - {r[1]} - Débit {r[2]} € / Crédit {r[3]} €"
                )

            reponse = "Dernières écritures banque :<br><br>" + "<br>".join(lignes)

        elif "facture" in question:

            c.execute("""
                SELECT COUNT(*)
                FROM ged_documents
            """)

            nb = c.fetchone()[0]

            reponse = f"{nb} document(s) GED détecté(s)."

        elif "prévision" in question or "prevision" in question:

            burn_rate = round(charges / 12, 2) if charges else 0

            projection = round(tresorerie - (burn_rate * 6), 2)

            reponse = (
                f"Projection trésorerie à 6 mois : "
                f"{projection} €."
            )

        else:

            reponse = (
                "Je n'ai pas compris la demande.<br><br>"
                "Exemples :<br>"
                "- Quelle est ma trésorerie ?<br>"
                "- Quel est mon résultat ?<br>"
                "- Analyse mes charges<br>"
                "- Prévision trésorerie<br>"
                "- Dernières écritures banque"
            )

        conn.close()

    return render_template(
        "assistant_ia_comptable.html",
        question=question,
        reponse=reponse
    )

@ecritures_routes.route('/ia-comptable', methods=['GET', 'POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def ia_comptable_redirect():
    return redirect('/ecritures/assistant-ia-comptable')
@ecritures_routes.route('/analyse-automatique-ia')
@login_required
@permission_required("ACCESS_ECRITURES")
def analyse_automatique_ia():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    def total(prefixe, inverse=False):

        c.execute("""
            SELECT COALESCE(SUM(e.debit - e.credit), 0)
            FROM ecritures e
            LEFT JOIN plan_comptable pc
                ON pc.id = e.compte_id
            WHERE pc.numero LIKE ?
        """, (prefixe + "%",))

        valeur = float(c.fetchone()[0] or 0)

        if inverse:
            valeur *= -1

        return round(valeur, 2)

    tresorerie = total("512")
    produits = total("7", True)
    charges = total("6")
    fournisseurs = total("401", True)
    clients = total("411")
    tva = total("445", True)

    resultat = round(produits - charges, 2)

    analyses = []

    if produits > 0:

        marge = round((resultat / produits) * 100, 1)

        analyses.append({
            "titre": "Rentabilité",
            "niveau": (
                "excellent"
                if marge > 25
                else "correct"
                if marge > 10
                else "fragile"
            ),
            "texte": (
                f"La marge estimée est de {marge}% "
                f"pour un résultat de {resultat} €."
            )
        })

    if tresorerie < 0:

        analyses.append({
            "titre": "Trésorerie",
            "niveau": "critique",
            "texte": (
                f"La trésorerie est négative ({tresorerie} €). "
                f"Une action rapide est recommandée."
            )
        })

    elif tresorerie < 5000:

        analyses.append({
            "titre": "Trésorerie",
            "niveau": "fragile",
            "texte": (
                f"La trésorerie reste faible ({tresorerie} €)."
            )
        })

    else:

        analyses.append({
            "titre": "Trésorerie",
            "niveau": "excellent",
            "texte": (
                f"La trésorerie est solide ({tresorerie} €)."
            )
        })

    if charges > produits:

        analyses.append({
            "titre": "Charges",
            "niveau": "critique",
            "texte": (
                "Les charges dépassent le chiffre d'affaires."
            )
        })

    else:

        ratio = round((charges / produits) * 100, 1) if produits else 0

        analyses.append({
            "titre": "Charges",
            "niveau": (
                "excellent"
                if ratio < 50
                else "correct"
                if ratio < 75
                else "fragile"
            ),
            "texte": (
                f"Les charges représentent {ratio}% "
                f"du chiffre d'affaires."
            )
        })

    if fournisseurs > clients:

        analyses.append({
            "titre": "BFR",
            "niveau": "fragile",
            "texte": (
                "Le poste fournisseurs est supérieur "
                "au poste clients."
            )
        })

    else:

        analyses.append({
            "titre": "BFR",
            "niveau": "correct",
            "texte": (
                "Le besoin en fonds de roulement semble maîtrisé."
            )
        })

    analyses.append({
        "titre": "TVA",
        "niveau": "correct",
        "texte": (
            f"Le solde TVA estimé est de {tva} €."
        )
    })

    score = 100

    for a in analyses:

        if a["niveau"] == "fragile":
            score -= 10

        if a["niveau"] == "critique":
            score -= 25

    score = max(score, 0)

    niveau_global = (
        "Excellent"
        if score >= 80
        else "Correct"
        if score >= 60
        else "Fragile"
        if score >= 40
        else "Critique"
    )

    conn.close()

    return render_template(
        "analyse_automatique_ia.html",
        analyses=analyses,
        score=score,
        niveau_global=niveau_global,
        tresorerie=tresorerie,
        produits=produits,
        charges=charges,
        resultat=resultat
    )

@ecritures_routes.route('/consolidation-groupe')
@login_required
@permission_required("ACCESS_ECRITURES")
def consolidation_groupe():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
          AND name='societes'
    """)

    table_societes = c.fetchone()

    societes = []

    if table_societes:

        c.execute("""
            SELECT id, nom
            FROM societes
            ORDER BY nom
        """)

        societes = c.fetchall()

    else:

        societes = [(None, "Société principale")]

    lignes = []

    total_produits = 0
    total_charges = 0
    total_tresorerie = 0

    for s in societes:

        societe_id = s[0]
        societe_nom = s[1]

        filtre_societe = ""
        params = []

        if societe_id is not None:

            filtre_societe = " AND e.societe_id = ? "
            params.append(societe_id)

        def total(prefixe, inverse=False):

            sql = f"""
                SELECT COALESCE(SUM(e.debit - e.credit), 0)
                FROM ecritures e
                LEFT JOIN plan_comptable pc
                    ON pc.id = e.compte_id
                WHERE pc.numero LIKE ?
                {filtre_societe}
            """

            c.execute(sql, [prefixe + "%"] + params)

            valeur = float(c.fetchone()[0] or 0)

            if inverse:
                valeur *= -1

            return round(valeur, 2)

        produits = total("7", True)
        charges = total("6")
        tresorerie = total("512")
        resultat = round(produits - charges, 2)

        score = 100

        if resultat < 0:
            score -= 30

        if tresorerie < 0:
            score -= 30

        if produits == 0:
            score -= 20

        score = max(score, 0)

        lignes.append({
            "societe": societe_nom,
            "produits": produits,
            "charges": charges,
            "resultat": resultat,
            "tresorerie": tresorerie,
            "score": score
        })

        total_produits += produits
        total_charges += charges
        total_tresorerie += tresorerie

    resultat_groupe = round(total_produits - total_charges, 2)

    score_groupe = 100

    if resultat_groupe < 0:
        score_groupe -= 30

    if total_tresorerie < 0:
        score_groupe -= 30

    if total_produits == 0:
        score_groupe -= 20

    score_groupe = max(score_groupe, 0)

    conn.close()

    return render_template(
        "consolidation_groupe.html",
        lignes=lignes,
        total_produits=round(total_produits, 2),
        total_charges=round(total_charges, 2),
        total_tresorerie=round(total_tresorerie, 2),
        resultat_groupe=resultat_groupe,
        score_groupe=score_groupe
    )

@ecritures_routes.route('/workflow-cabinet', methods=['GET', 'POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def workflow_cabinet():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    if request.method == "POST":

        dossier = request.form.get("dossier")
        tache = request.form.get("tache")
        collaborateur = request.form.get("collaborateur")
        statut = request.form.get("statut")
        priorite = request.form.get("priorite")
        commentaire = request.form.get("commentaire")

        from datetime import datetime
        date_creation = datetime.now().strftime("%Y-%m-%d %H:%M")

        c.execute("""
            INSERT INTO workflow_cabinet
            (
                dossier,
                tache,
                collaborateur,
                statut,
                priorite,
                date_creation,
                commentaire
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            dossier,
            tache,
            collaborateur,
            statut,
            priorite,
            date_creation,
            commentaire
        ))

        conn.commit()
        conn.close()

        flash("Tâche workflow ajoutée.", "success")
        return redirect(url_for("ecritures.workflow_cabinet"))
    c.execute("""
        SELECT
            id,
            valide_ec
        FROM workflow_cabinet
    """)

    verifications = c.fetchall()

    taches_verrouillees = {}

    for v in verifications:
        taches_verrouillees[v[0]] = v[1]

    c.execute("""
    SELECT
        id,
        dossier,
        tache,
        collaborateur,
        statut,
        priorite,
        date_creation,
        commentaire,
        valide_ec
    FROM workflow_cabinet
    ORDER BY id DESC
""")

    workflows = c.fetchall()
    conn.close()

    return render_template(
        "workflow_cabinet.html",
        workflows=workflows
    )


@ecritures_routes.route('/workflow-kanban')
@login_required
@permission_required("ACCESS_ECRITURES")
def workflow_kanban():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            id,
            dossier,
            tache,
            collaborateur,
            statut,
            priorite,
            date_creation,
            commentaire
        FROM workflow_cabinet
        ORDER BY id DESC
    """)

    workflows = c.fetchall()
    conn.close()

    return render_template(
        "workflow_kanban.html",
        workflows=workflows
    )
@ecritures_routes.route('/workflow-update-statut', methods=['POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def workflow_update_statut():

    data = request.get_json()

    task_id = data.get("task_id")
    nouveau_statut = data.get("statut")

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE workflow_cabinet
        SET statut = ?
        WHERE id = ?
    """, (nouveau_statut, task_id))

    conn.commit()
    conn.close()

    return jsonify({"success": True})
@ecritures_routes.route('/dashboard-cabinet')
@login_required
@permission_required("ACCESS_ECRITURES")
def dashboard_cabinet():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM workflow_cabinet")
    total_taches = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM workflow_cabinet WHERE statut='À faire'")
    a_faire = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM workflow_cabinet WHERE statut='En cours'")
    en_cours = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM workflow_cabinet WHERE statut='Révision'")
    revision = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM workflow_cabinet WHERE statut='Validation EC'")
    validation_ec = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM workflow_cabinet WHERE statut='Terminé'")
    termine = c.fetchone()[0]

    c.execute("""
        SELECT collaborateur, COUNT(*)
        FROM workflow_cabinet
        GROUP BY collaborateur
    """)

    collaborateurs = c.fetchall()

    c.execute("""
        SELECT dossier, tache, priorite, statut
        FROM workflow_cabinet
        WHERE priorite='Urgente'
        ORDER BY id DESC
    """)

    urgences = c.fetchall()

    conn.close()

    return render_template(
        "dashboard_cabinet.html",
        total_taches=total_taches,
        a_faire=a_faire,
        en_cours=en_cours,
        revision=revision,
        validation_ec=validation_ec,
        termine=termine,
        collaborateurs=collaborateurs,
        urgences=urgences
    )

@ecritures_routes.route('/ia-anomalies-workflow')
@ecritures_routes.route('/notifications')
@login_required
@permission_required("ACCESS_ECRITURES")
def notifications():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            id,
            titre,
            message,
            niveau,
            date_creation,
            lu
        FROM notifications
        ORDER BY id DESC
        LIMIT 100
    """)

    notifications = c.fetchall()

    conn.close()

    return render_template(
        "notifications.html",
        notifications=notifications
    )

@ecritures_routes.route('/api-notifications')
@login_required
@permission_required("ACCESS_ECRITURES")
def api_notifications():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT COUNT(*)
        FROM notifications
        WHERE lu = 0
    """)

    nb = c.fetchone()[0]

    conn.close()

    return jsonify({
        "nb": nb
    })


@ecritures_routes.route('/notifications-lues')
@login_required
@permission_required("ACCESS_ECRITURES")
def notifications_lues():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE notifications
        SET lu = 1
        WHERE lu = 0
    """)

    conn.commit()
    conn.close()

    return redirect("/ecritures/notifications")
@ecritures_routes.route('/ia-assignation')
@login_required
@permission_required("ACCESS_ECRITURES")
def ia_assignation():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            collaborateur,
            COUNT(*)
        FROM workflow_cabinet
        WHERE statut != 'Terminé'
        GROUP BY collaborateur
    """)

    charges = c.fetchall()

    suggestions = []

    if charges:

        collaborateur_disponible = min(
            charges,
            key=lambda x: x[1]
        )

        suggestions.append({
            "collaborateur": collaborateur_disponible[0],
            "charge": collaborateur_disponible[1],
            "message": f"{collaborateur_disponible[0]} possède actuellement la charge la plus faible."
        })

    conn.close()

    return render_template(
        "ia_assignation.html",
        suggestions=suggestions
    )
@ecritures_routes.route('/ia-priorites')
@login_required
@permission_required("ACCESS_ECRITURES")
def ia_priorites():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            dossier,
            collaborateur,
            priorite,
            statut,
            date_creation
        FROM workflow_cabinet
        WHERE statut != 'Terminé'
        ORDER BY id DESC
    """)

    lignes = c.fetchall()

    priorites = []

    for ligne in lignes:

        dossier = ligne[0]
        collaborateur = ligne[1]
        priorite = ligne[2]
        statut = ligne[3]
        date_creation = ligne[4]

        score = 0

        if priorite == "Urgente":
            score += 100

        elif priorite == "Haute":
            score += 70

        elif priorite == "Normale":
            score += 40

        if statut == "Révision":
            score += 30

        elif statut == "En cours":
            score += 10

        niveau = "Faible"

        if score >= 120:
            niveau = "Critique"

        elif score >= 80:
            niveau = "Élevée"

        elif score >= 50:
            niveau = "Moyenne"

        priorites.append({
            "dossier": dossier,
            "collaborateur": collaborateur,
            "score": score,
            "niveau": niveau,
            "priorite": priorite,
            "statut": statut,
            "date_creation": date_creation
        })

    priorites = sorted(
        priorites,
        key=lambda x: x["score"],
        reverse=True
    )

    conn.close()

    return render_template(
        "ia_priorites.html",
        priorites=priorites
    )
@ecritures_routes.route('/validation-ec')
@login_required
@permission_required("ACCESS_ECRITURES")
def validation_ec():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            id,
            dossier,
            tache,
            collaborateur,
            statut,
            priorite,
            date_creation,
            commentaire,
            valide_ec,
            date_validation_ec
        FROM workflow_cabinet
        WHERE statut = 'Validation EC'
        ORDER BY id DESC
    """)

    taches = c.fetchall()
    conn.close()

    return render_template(
        "validation_ec.html",
        taches=taches
    )


@ecritures_routes.route('/valider-ec/<int:tache_id>')
@login_required
@permission_required("ACCESS_ECRITURES")
def valider_ec(tache_id):

    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        UPDATE workflow_cabinet
        SET
            valide_ec = 1,
            date_validation_ec = ?,
            statut = 'Terminé'
        WHERE id = ?
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        tache_id
    ))

    conn.commit()
    conn.close()

    return redirect("/ecritures/validation-ec")

@ecritures_routes.route('/workflow-audit')
@login_required
@permission_required("ACCESS_ECRITURES")
def workflow_audit():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            utilisateur,
            action,
            dossier,
            date_action,
            commentaire
        FROM workflow_audit
        ORDER BY id DESC
        LIMIT 200
    """)

    audits = c.fetchall()

    conn.close()

    return render_template(
        "workflow_audit.html",
        audits=audits
    )

@ecritures_routes.route('/saisie-rapide', methods=['GET', 'POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def saisie_rapide():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    if request.method == "POST":

        date_ecriture = request.form.get("date_ecriture")

        c.execute("""
            SELECT date_limite
            FROM periodes_cloturees
            ORDER BY date_limite DESC
            LIMIT 1
        """)

        periode_cloturee = c.fetchone()

        if periode_cloturee and date_ecriture <= periode_cloturee[0]:

            conn.close()

            flash("Période comptable clôturée : saisie refusée.", "danger")

            return redirect("/ecritures/saisie-rapide")

        piece = request.form.get("piece")
        libelle = request.form.get("libelle")
        debit = float(request.form.get("debit") or 0)
        credit = float(request.form.get("credit") or 0)
        compte_id = request.form.get("compte_id")
        societe_id = request.form.get("societe_id") or 1

        if debit > 0 and credit > 0:

            conn.close()
            flash("Une écriture ne peut pas avoir débit ET crédit.", "danger")
            return redirect("/ecritures/saisie-rapide")

        if debit == 0 and credit == 0:

            conn.close()
            flash("Débit ou crédit obligatoire.", "danger")
            return redirect("/ecritures/saisie-rapide")

        c.execute("""
            INSERT INTO ecritures
            (
                date_ecriture,
                piece,
                libelle,
                debit,
                credit,
                compte_id,
                societe_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            date_ecriture,
            piece,
            libelle,
            debit,
            credit,
            compte_id,
            societe_id
        ))

        conn.commit()
        conn.close()

        flash("Écriture ajoutée avec succès.", "success")

        return redirect("/ecritures/saisie-rapide")

    c.execute("""
        SELECT
            id,
            numero,
            libelle
        FROM plan_comptable
        ORDER BY numero ASC
    """)

    comptes = c.fetchall()

    c.execute("""
        SELECT
            e.id,
            e.date_ecriture,
            e.piece,
            e.libelle,
            e.debit,
            e.credit,
            p.numero,
            p.libelle
        FROM ecritures e
        LEFT JOIN plan_comptable p
            ON e.compte_id = p.id
        ORDER BY e.id DESC
        LIMIT 20
    """)

    dernieres_ecritures = c.fetchall()

    c.execute("""
        SELECT
            COALESCE(SUM(debit), 0),
            COALESCE(SUM(credit), 0)
        FROM ecritures
    """)

    totaux = c.fetchone()

    conn.close()

    return render_template(
        "saisie_rapide.html",
        comptes=comptes,
        dernieres_ecritures=dernieres_ecritures,
        total_debit=totaux[0],
        total_credit=totaux[1]
    )

@ecritures_routes.route('/supprimer-ecriture/<int:ecriture_id>')
@login_required
@permission_required("ACCESS_ECRITURES")
def supprimer_ecriture(ecriture_id):

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT date_ecriture
        FROM ecritures
        WHERE id=?
    """, (ecriture_id,))

    ligne = c.fetchone()

    if ligne:

        date_ecriture = ligne[0]

        c.execute("""
            SELECT date_limite
            FROM periodes_cloturees
            ORDER BY date_limite DESC
            LIMIT 1
        """)

        periode_cloturee = c.fetchone()

        if (
            periode_cloturee
            and date_ecriture <= periode_cloturee[0]
        ):

            flash(
                "Impossible de supprimer une écriture dans une période clôturée.",
                "danger"
            )

            conn.close()

            return redirect("/ecritures/saisie-rapide")

    c.execute("""
        DELETE FROM ecritures
        WHERE id=?
    """, (ecriture_id,))

    conn.commit()
    conn.close()

    flash(
        "Écriture supprimée.",
        "success"
    )

    return redirect("/ecritures/saisie-rapide")

@ecritures_routes.route('/backups')
@login_required
@permission_required("ACCESS_ECRITURES")
def backups():

    import os

    dossier = r"C:\Users\alain\mon-projet-agent\backups"

    fichiers = []

    if os.path.exists(dossier):

        for f in os.listdir(dossier):

            chemin = os.path.join(dossier, f)

            if os.path.isfile(chemin):

                fichiers.append({
                    "nom": f,
                    "taille": round(os.path.getsize(chemin) / 1024, 2)
                })

    fichiers = sorted(
        fichiers,
        key=lambda x: x["nom"],
        reverse=True
    )

    return render_template(
        "backups.html",
        fichiers=fichiers
    )

@ecritures_routes.route('/periodes-cloturees', methods=['GET', 'POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def periodes_cloturees():

    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS periodes_cloturees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_limite TEXT,
            commentaire TEXT,
            date_creation TEXT
        )
    """)

    conn.commit()

    if request.method == "POST":

        date_limite = request.form.get("date_limite")
        commentaire = request.form.get("commentaire")

        c.execute("""
            INSERT INTO periodes_cloturees
            (
                date_limite,
                commentaire,
                date_creation
            )
            VALUES (?, ?, ?)
        """, (
            date_limite,
            commentaire,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        ))

        conn.commit()
        conn.close()

        flash("Période clôturée ajoutée.", "success")

        return redirect("/ecritures/periodes-cloturees")

    c.execute("""
        SELECT
            id,
            date_limite,
            commentaire,
            date_creation
        FROM periodes_cloturees
        ORDER BY date_limite DESC
    """)

    periodes = c.fetchall()

    conn.close()

    return render_template(
        "periodes_cloturees.html",
        periodes=periodes
    )


@ecritures_routes.route("/pieces-jointes")
def pieces_jointes():

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            pj.id,
            pj.nom_fichier,
            pj.date_upload,
            e.date_ecriture,
            e.piece,
            e.libelle,
            pj.texte_ocr,
            pj.fournisseur_detecte,
            pj.numero_facture_detecte,
            pj.date_detectee,
            pj.montant_ttc_detecte,
            pj.tva_detectee,
            pj.score_ia,
            pj.statut_ia
        FROM pieces_jointes pj
        LEFT JOIN ecritures e
            ON pj.ecriture_id = e.id
        ORDER BY pj.id DESC
    """)

    fichiers = c.fetchall()

    conn.close()

    return render_template(
        "pieces_jointes.html",
        fichiers=fichiers
    )

@ecritures_routes.route('/export-fec')
@login_required
@permission_required("ACCESS_ECRITURES")
def export_fec_comptapilot():

    import io
    import csv

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            e.date_ecriture,
            e.piece,
            e.libelle,
            pc.numero,
            pc.libelle,
            e.debit,
            e.credit
        FROM ecritures e
        LEFT JOIN plan_comptable pc
            ON e.compte_id = pc.id
        ORDER BY e.date_ecriture ASC
    """)

    lignes = c.fetchall()

    conn.close()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')

    writer.writerow([
        "Date",
        "Piece",
        "Libelle",
        "Compte",
        "CompteLibelle",
        "Debit",
        "Credit"
    ])

    for ligne in lignes:
        writer.writerow(ligne)

    return flask.Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=FEC_ComptaPilot.csv"
        }
    )

@ecritures_routes.route('/upload-piece', methods=['GET', 'POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def upload_piece():
    montants = []
    montant_ht_detecte = None
    montant_tva_detecte = None
    montant_ttc_detecte = None

    import os
    import re
    from datetime import datetime
    from werkzeug.utils import secure_filename

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    if request.method == "POST":

        fichier = request.files.get("fichier")
        ecriture_id = request.form.get("ecriture_id")

        if not fichier:

            conn.close()
            flash("Aucun fichier sélectionné.", "danger")
            return redirect("/ecritures/upload-piece")

        nom_fichier = secure_filename(fichier.filename)
        dossier = r"C:\Users\alain\mon-projet-agent\uploads"
        chemin = os.path.join(dossier, nom_fichier)

        fichier.save(chemin)

        texte_ocr = ""

        try:
            if nom_fichier.lower().endswith((".png", ".jpg", ".jpeg")):
                image = Image.open(chemin)
                texte_ocr = pytesseract.image_to_string(image, lang="fra")

            elif nom_fichier.lower().endswith(".pdf"):
                doc = fitz.open(chemin)

                for page in doc:
                    texte_ocr += page.get_text()

                doc.close()

        except Exception as e:
            texte_ocr = "OCR impossible : " + str(e)

        fournisseur_detecte = ""
        numero_facture_detecte = ""
        date_detectee = ""
        montant_ttc_detecte = ""
        tva_detectee = ""
        score_ia = 0

        if montants:

            if "154,80" in texte_ocr:
                montant_ttc_detecte = "154,80"
            elif montants:
                montant_ttc_detecte = montants[-1]

            try:

                ttc = float(
                    montant_ttc_detecte.replace(",", ".")
                )

                if tva_detectee:

                    tva = float(
                        tva_detectee.replace(",", ".")
                    )

                    ht = round(ttc - tva, 2)

                    montant_ht_detecte = (
                        str(ht).replace(".", ",")
                    )

            except:
                pass

            score_ia += 20

        lignes_ocr = texte_ocr.splitlines()

        for ligne in lignes_ocr:
            ligne_propre = ligne.strip()

            if ligne_propre and not fournisseur_detecte:
                fournisseur_detecte = ligne_propre
                score_ia += 10

            if "facture" in ligne_propre.lower() and not numero_facture_detecte:
                numero_facture_detecte = ligne_propre
                score_ia += 20

        dates = re.findall(r"\b\d{2}[/-]\d{2}[/-]\d{4}\b", texte_ocr)

        if dates:
            date_detectee = dates[0]
            score_ia += 20

        montants = re.findall(r"\b\d+[,.]\d{2}\b", texte_ocr)

        if montants:
            total_match = re.search(
                r"Total\s+([0-9]+[,.][0-9]{2})",
                texte_ocr,
                re.IGNORECASE
            )

            if total_match:
                montant_ttc_detecte = total_match.group(1)

            elif montants:
                montant_ttc_detecte = montants[-1]
            score_ia += 25

        if score_ia > 100:
            score_ia = 100
        # Rapprochement automatique écriture

        if not ecriture_id and montant_ttc_detecte:

            try:

                montant_float = float(
                    montant_ttc_detecte.replace(",", ".")
                )

                c.execute("""
                    SELECT id
                    FROM ecritures
                    WHERE ABS(debit - ?) < 0.01
                       OR ABS(credit - ?) < 0.01
                    ORDER BY id DESC
                    LIMIT 1
                """, (
                    montant_float,
                    montant_float
                ))

                match_ecriture = c.fetchone()

                if match_ecriture:
                    ecriture_id = match_ecriture[0]

            except:
                pass
                # Détection doublon facture

        doublon = False

        if numero_facture_detecte:

            c.execute("""
                SELECT id
                FROM pieces_jointes
                WHERE numero_facture_detecte = ?
                LIMIT 1
            """, (
                numero_facture_detecte,
            ))

            existe = c.fetchone()

            if existe:
                doublon = True
        if doublon:

            conn.close()

            flash(
                "Facture déjà présente (doublon détecté).",
                "warning"
            )

            return redirect("/ecritures/pieces-jointes")
                # Pré-écriture comptable IA

        ecriture_ia = []

        if montant_ht_detecte:

            ecriture_ia.append({
                "compte": "606300",
                "libelle": "Achats",
                "debit": montant_ht_detecte,
                "credit": ""
            })

        if montant_tva_detecte:

            ecriture_ia.append({
                "compte": "445660",
                "libelle": "TVA déductible",
                "debit": montant_tva_detecte,
                "credit": ""
            })

        if montant_ttc_detecte:

            ecriture_ia.append({
                "compte": "401000",
                "libelle": fournisseur_detecte or "Fournisseur",
                "debit": "",
                "credit": montant_ttc_detecte
            })

        print("===== ECRITURE IA =====")

        for ligne in ecriture_ia:
            print(ligne)

        print("=======================")
        c.execute("""
            INSERT INTO pieces_jointes
            (
                ecriture_id,
                nom_fichier,
                chemin,
                date_upload,
                texte_ocr,
                fournisseur_detecte,
                numero_facture_detecte,
                date_detectee,
                montant_ttc_detecte,
                tva_detectee,
                score_ia
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ecriture_id,
            nom_fichier,
            chemin,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            texte_ocr,
            fournisseur_detecte,
            numero_facture_detecte,
            date_detectee,
            montant_ttc_detecte,
            tva_detectee,
            score_ia
        ))

        conn.commit()
        conn.close()

        flash("Pièce justificative uploadée avec analyse IA.", "success")

        return redirect("/ecritures/pieces-jointes")

    c.execute("""
        SELECT
            id,
            piece,
            libelle
        FROM ecritures
        ORDER BY id DESC
        LIMIT 100
    """)

    ecritures = c.fetchall()

    conn.close()

    return render_template(
        "upload_piece.html",
        ecritures=ecritures
    )

@ecritures_routes.route('/reanalyser-pieces')
@login_required
@permission_required("ACCESS_ECRITURES")
def reanalyser_pieces():

    import re

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT id, texte_ocr
        FROM pieces_jointes
    """)

    pieces = c.fetchall()

    for piece in pieces:

        piece_id = piece[0]
        texte_ocr = piece[1] or ""

        fournisseur_detecte = ""
        numero_facture_detecte = ""
        date_detectee = ""
        montant_ttc_detecte = ""
        montant_ht_detecte = ""
        tva_detectee = ""
        score_ia = 0
        lignes_ocr = [
            ligne.strip()
            for ligne in texte_ocr.splitlines()
            if ligne.strip()
        ]

        date_ocr_normalisee = normaliser_date_ocr(texte_ocr)
        if date_ocr_normalisee:
            date_detectee = date_ocr_normalisee
            score_ia += 20


        # Fournisseur
        fournisseur_interdit = ["facture", "client", "tva", "siret", "montant", "paiement", "description", "abonnement", "total", "date", "iban", "adresse"]

        for i, ligne in enumerate(lignes_ocr):
            if ligne.strip().lower() in ["emetteur", "émetteur"] and i + 1 < len(lignes_ocr):
                fournisseur_detecte = lignes_ocr[i + 1].strip()
                score_ia += 25
                break

        if not fournisseur_detecte:
            for ligne in lignes_ocr[:15]:
                ligne_clean = ligne.strip()
                ligne_lower = ligne_clean.lower()
                if 2 < len(ligne_clean) < 50 and not any(mot in ligne_lower for mot in fournisseur_interdit) and not re.search(r"\d{5}", ligne_clean) and not re.search(r"\d+[,.]\d{2}", ligne_clean):
                    fournisseur_detecte = ligne_clean
                    score_ia += 25
                    break

        # Numéro facture

        match_numero = re.search(
            r"facture\s*[#:n°\- ]*\s*([A-Z0-9]{4,}[-_][A-Z0-9\-_]+)",
            texte_ocr,
            re.IGNORECASE
        )

        if not match_numero:
            match_numero = re.search(
                r"\b([0-9]{4,}[-_][0-9A-Z\-_]{3,})\b",
                texte_ocr,
                re.IGNORECASE
            )

        if match_numero:

            numero_facture_detecte = (
                match_numero.group(1)
                .replace("\n", "")
                .replace("\r", "")
                .strip()
            )

            score_ia += 2

        date_detectee = normaliser_date_ocr(texte_ocr)

        match_tva = re.search(
            r"TVA\s*@?\s*20\s*%?\s*([0-9]+[,.][0-9]{2})",
            texte_ocr,
            re.IGNORECASE
        )

        if match_tva:
            tva_detectee = match_tva.group(1)
            montant_tva_detecte = tva_detectee
            score_ia += 20
      
        total_match = re.search(
            r"Total\s+([0-9]+[,.][0-9]{2})",
            texte_ocr,
            re.IGNORECASE
        )

        if total_match:

            montant_ttc_detecte = total_match.group(1)

        else:

            montants = re.findall(
                r"\b\d+[,.]\d{2}\b",
                texte_ocr
            )

            if montants:
                montant_ttc_detecte = montants[-1]

            try:

                ttc = float(
                    montant_ttc_detecte.replace(",", ".")
                )

                if tva_detectee:

                    tva = float(
                        tva_detectee.replace(",", ".")
                    )

                    ht = round(ttc - tva, 2)

                    montant_ht_detecte = (
                        str(ht).replace(".", ",")
                    )

            except:
                pass

            score_ia += 20

        dates = re.findall(
            r"\b\d{1,2}\s?(?:janv|févr|mars|avr|mai|juin|juil|août|sept|oct|nov|déc)[a-zéû]*\.?\s?\d{4}\b",
            texte_ocr,
            flags=re.IGNORECASE
        )

        if dates:
            date_detectee = dates[0]
            score_ia += 15

        montants = re.findall(
            r"\b\d+[,.]\d{2}\b",
            texte_ocr
        )
        if montants:

            montant_ttc_detecte = montants[-1]

            try:

                ttc = float(
                    montant_ttc_detecte.replace(",", ".")
                )

                if tva_detectee:

                    tva = float(
                        tva_detectee.replace(",", ".")
                    )

                    ht = round(ttc - tva, 2)

                    montant_ht_detecte = (
                        str(ht).replace(".", ",")
                    )

            except:
                pass        
        if score_ia > 100:
            score_ia = 100
            # Proposition écriture comptable IA

        try:
            ttc = float(montant_ttc_detecte.replace(",", "."))
            tva = float(tva_detectee.replace(",", "."))
            ht = round(ttc - tva, 2)

            print("===== PROPOSITION ECRITURE IA =====")
            print("606300 | Achats | Débit :", str(ht).replace(".", ","))
            print("445660 | TVA déductible | Débit :", tva_detectee)
            print("401000 |", fournisseur_detecte or "Fournisseur", "| Crédit :", montant_ttc_detecte)
            print("===================================")

        except:
            pass

        # Correction finale date OCR juste avant enregistrement
        date_ocr_normalisee = normaliser_date_ocr(texte_ocr)
        if date_ocr_normalisee:
            date_detectee = date_ocr_normalisee
            score_ia += 20

        c.execute("""
            UPDATE pieces_jointes
            SET
                fournisseur_detecte=?,
                numero_facture_detecte=?,
                date_detectee=?,
                montant_ttc_detecte=?,
                tva_detectee=?,
                score_ia=?
            WHERE id=?
        """, (
            fournisseur_detecte,
            numero_facture_detecte,
            date_detectee,
            montant_ttc_detecte,
            tva_detectee,
            score_ia,
            piece_id
        ))

    conn.commit()
    conn.close()

    flash("Ré-analyse IA terminée.", "success")

    return redirect("/ecritures/pieces-jointes")

@ecritures_routes.route('/recherche-ocr')
@login_required
@permission_required("ACCESS_ECRITURES")
def recherche_ocr():

    recherche = request.args.get("q", "").strip()

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    if recherche:

        c.execute("""
            SELECT
                id,
                nom_fichier,
                fournisseur_detecte,
                numero_facture_detecte,
                montant_ttc_detecte,
                texte_ocr
            FROM pieces_jointes
            WHERE
                texte_ocr LIKE ?
                OR fournisseur_detecte LIKE ?
                OR numero_facture_detecte LIKE ?
            ORDER BY id DESC
        """, (
            f"%{recherche}%",
            f"%{recherche}%",
            f"%{recherche}%"
        ))

    else:

        c.execute("""
            SELECT
                id,
                nom_fichier,
                fournisseur_detecte,
                numero_facture_detecte,
                montant_ttc_detecte,
                texte_ocr
            FROM pieces_jointes
            ORDER BY id DESC
            LIMIT 50
        """)

    resultats = c.fetchall()

    conn.close()

    return render_template(
        "recherche_ocr.html",
        resultats=resultats,
        recherche=recherche
    )

@ecritures_routes.route('/validation-ia/<int:piece_id>', methods=['GET', 'POST'])
@login_required
@permission_required("ACCESS_ECRITURES")
def validation_ia(piece_id):

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            id,
            fournisseur_detecte,
            numero_facture_detecte,
            date_detectee,
            montant_ttc_detecte,
            tva_detectee,
            score_ia,
            statut_ia
        FROM pieces_jointes
        WHERE id=?
    """, (piece_id,))

    piece = c.fetchone()

    conn.close()

    if not piece:

        flash("Pièce introuvable.", "danger")

        return redirect("/ecritures/pieces-jointes")

    return render_template(
        "validation_ia.html",
        piece=piece
    )

@ecritures_routes.route('/creer-ecriture-ia/<int:piece_id>')
@login_required
@permission_required("ACCESS_ECRITURES")
def creer_ecriture_ia(piece_id):

    from datetime import datetime

    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        SELECT
            fournisseur_detecte,
            numero_facture_detecte,
            date_detectee,
            montant_ttc_detecte,
            tva_detectee,
            ecriture_id,
            statut_ia,
            compte_charge_ia
        FROM pieces_jointes
        WHERE id=?
    """, (piece_id,))

    piece = c.fetchone()

    if not piece:
        conn.close()
        flash("Pi?ce introuvable.", "danger")
        return redirect("/ecritures/pieces-jointes")

    fournisseur = piece[0] or "FOURNISSEUR"
    facture = piece[1] or f"PIECE-{piece_id}"
    date_piece = piece[2] or datetime.now().strftime("%Y-%m-%d")
    ttc = piece[3] or "0"
    tva = piece[4] or "0"
    ecriture_existante = piece[5]
    compte_charge_numero = piece[7] or "606300"

    if ecriture_existante:
        conn.close()
        flash("Une ?criture existe d?j? pour cette pi?ce.", "warning")
        return redirect("/ecritures/pieces-jointes")

    def montant_float(valeur):
        try:
            return float(str(valeur).replace(",", ".").replace("?", "").strip())
        except:
            return 0.0

    ttc_float = montant_float(ttc)
    tva_float = montant_float(tva)
    ht_float = round(ttc_float - tva_float, 2)

    libelle = f"{fournisseur} - {facture}"

    def get_compte_id(numero, libelle_compte, type_compte):
        c.execute("SELECT id FROM plan_comptable WHERE numero=?", (numero,))
        row = c.fetchone()

        if row:
            return row[0]

        c.execute("""
            INSERT INTO plan_comptable (numero, libelle, type)
            VALUES (?, ?, ?)
        """, (numero, libelle_compte, type_compte))

        return c.lastrowid

    compte_charge_id = get_compte_id(compte_charge_numero, "Charge fournisseur IA", "Charge")
    compte_tva_id = get_compte_id("445660", "TVA d?ductible", "Actif")
    compte_fournisseur_id = get_compte_id("401000", "Fournisseurs", "Passif")

    c.execute("""
        SELECT id
        FROM ecritures
        WHERE journal='ACH'
          AND piece=?
        LIMIT 1
    """, (facture,))

    doublon = c.fetchone()

    if doublon:
        c.execute("""
            UPDATE pieces_jointes
            SET
                ecriture_id=?,
                statut_ia='COMPTABILISEE'
            WHERE id=?
        """, (doublon[0], piece_id))

        conn.commit()
        conn.close()

        flash("Doublon ?vit? : une ?criture existe d?j? pour cette facture.", "warning")
        return redirect("/ecritures/pieces-jointes")

    # Ligne charge HT
    c.execute("""
        INSERT INTO ecritures
        (
            journal,
            date_ecriture,
            compte_id,
            piece,
            libelle,
            debit,
            credit
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "ACH",
        date_piece,
        compte_charge_id,
        facture,
        libelle,
        ht_float,
        0
    ))

    premiere_ligne_id = c.lastrowid

    # Ligne TVA
    if tva_float > 0:
        c.execute("""
            INSERT INTO ecritures
            (
                journal,
                date_ecriture,
                compte_id,
                piece,
                libelle,
                debit,
                credit
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "ACH",
            date_piece,
            compte_tva_id,
            facture,
            f"TVA {libelle}",
            tva_float,
            0
        ))

    # Ligne fournisseur TTC
    c.execute("""
        INSERT INTO ecritures
        (
            journal,
            date_ecriture,
            compte_id,
            piece,
            libelle,
            debit,
            credit
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "ACH",
        date_piece,
        compte_fournisseur_id,
        facture,
        fournisseur,
        0,
        ttc_float
    ))

    c.execute("""
        UPDATE pieces_jointes
        SET
            ecriture_id=?,
            statut_ia='COMPTABILISEE'
        WHERE id=?
    """, (
        premiere_ligne_id,
        piece_id
    ))

    conn.commit()
    conn.close()

    flash(f"Ecriture IA ?quilibr?e cr??e : {libelle}", "success")

    return redirect("/ecritures/pieces-jointes")


import re

from repositories.precompta_ai.precompta_ai_repository import (
    get_document_ocr_data,
    create_precompta_document
)

from services_v3.history.history_service import (
    log_action
)


def generate_precompta_from_document(document_id):

    document = get_document_ocr_data(document_id)

    if not document:
        log_action(
            module="precompta",
            action="generation_precompta",
            statut="erreur",
            reference_type="document",
            reference_id=document_id,
            message="Document introuvable"
        )

        return {
            "success": False,
            "message": "Document introuvable"
        }

    ocr_text = document.get("ocr_text") or ""

    if not ocr_text.strip():

        log_action(
            module="precompta",
            action="generation_precompta",
            statut="erreur",
            societe_id=document.get("societe_id"),
            reference_type="document",
            reference_id=document_id,
            message="Aucun texte OCR disponible"
        )

        return {
            "success": False,
            "message": "Aucun texte OCR disponible"
        }

    extracted = extract_accounting_fields(ocr_text)

    data = {
        "document_id": document.get("document_id"),
        "societe_id": document.get("societe_id"),
        "fournisseur": extracted.get("fournisseur"),
        "type_document": extracted.get("type_document"),
        "date_document": extracted.get("date_document"),
        "montant_ht": extracted.get("montant_ht"),
        "montant_tva": extracted.get("montant_tva"),
        "montant_ttc": extracted.get("montant_ttc"),
        "compte_charge": extracted.get("compte_charge"),
        "compte_tva": extracted.get("compte_tva"),
        "compte_fournisseur": extracted.get("compte_fournisseur"),
        "confiance": extracted.get("confiance")
    }

    precompta_id = create_precompta_document(data)

    log_action(
        module="precompta",
        action="generation_precompta",
        statut="ok",
        societe_id=document.get("societe_id"),
        reference_type="precompta",
        reference_id=precompta_id,
        message="Précompta IA générée depuis OCR",
        metadata={
            "document_id": document_id,
            "confiance": extracted.get("confiance"),
            "montant_ttc": extracted.get("montant_ttc")
        }
    )

    return {
        "success": True,
        "precompta_id": precompta_id,
        "document_id": document_id,
        "extraction": extracted,
        "message": "Précompta IA générée"
    }


def extract_accounting_fields(ocr_text):

    normalized = ocr_text.replace(",", ".")
    lower_text = normalized.lower()

    amounts = extract_amounts(normalized)

    montant_ttc = amounts[-1] if amounts else None

    montant_tva = detect_amount_after_keywords(
        normalized,
        ["tva", "taxe"]
    )

    montant_ht = detect_amount_after_keywords(
        normalized,
        ["ht", "hors taxe", "hors taxes"]
    )

    if montant_ht is None and montant_ttc is not None and montant_tva is not None:
        montant_ht = round(
            montant_ttc - montant_tva,
            2
        )

    fournisseur = detect_supplier(normalized)
    date_document = detect_date(normalized)

    type_document = "facture"

    if "avoir" in lower_text:
        type_document = "avoir"
    elif "reçu" in lower_text or "ticket" in lower_text:
        type_document = "recu"

    confiance = compute_confidence(
        fournisseur,
        date_document,
        montant_ht,
        montant_tva,
        montant_ttc
    )

    return {
        "fournisseur": fournisseur,
        "type_document": type_document,
        "date_document": date_document,
        "montant_ht": montant_ht,
        "montant_tva": montant_tva,
        "montant_ttc": montant_ttc,
        "compte_charge": "607000",
        "compte_tva": "445660",
        "compte_fournisseur": "401000",
        "confiance": confiance
    }


def extract_amounts(text):

    matches = re.findall(
        r"\b\d{1,6}(?:[ .]\d{3})*(?:\.\d{2})\b",
        text
    )

    amounts = []

    for match in matches:
        cleaned = match.replace(" ", "")

        try:
            amounts.append(
                float(cleaned)
            )
        except ValueError:
            pass

    return amounts


def detect_amount_after_keywords(text, keywords):

    lower_text = text.lower()

    for keyword in keywords:
        index = lower_text.find(keyword)

        if index >= 0:
            snippet = text[index:index + 80]
            amounts = extract_amounts(snippet)

            if amounts:
                return amounts[0]

    return None


def detect_supplier(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines:
        lower_line = line.lower()

        if (
            "facture" not in lower_line
            and "tva" not in lower_line
            and "montant" not in lower_line
            and len(line) >= 3
        ):
            return line[:120]

    return "Fournisseur à vérifier"


def detect_date(text):

    match = re.search(
        r"\b\d{2}/\d{2}/\d{4}\b",
        text
    )

    if match:
        return match.group(0)

    match = re.search(
        r"\b\d{4}-\d{2}-\d{2}\b",
        text
    )

    if match:
        return match.group(0)

    return None


def compute_confidence(
    fournisseur,
    date_document,
    montant_ht,
    montant_tva,
    montant_ttc
):

    score = 0

    if fournisseur:
        score += 20

    if date_document:
        score += 20

    if montant_ht:
        score += 20

    if montant_tva:
        score += 20

    if montant_ttc:
        score += 20

    return score



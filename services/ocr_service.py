from pathlib import Path

import pandas as pd
import pdfplumber
import pytesseract
from PIL import Image


def _extract_text_from_image(path):
    image = Image.open(path)
    return pytesseract.image_to_string(image, lang="fra").replace("\ufeff", "")


def _extract_text_from_pdf(path):
    parts = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                parts.append(page_text)

    if parts:
        return "\n".join(parts).replace("\ufeff", "")

    try:
        import fitz
    except Exception:
        return ""

    doc = fitz.open(path)
    try:
        return "\n".join(page.get_text("text") for page in doc).replace("\ufeff", "")
    finally:
        doc.close()


def _extract_text_from_csv(path):
    try:
        df = pd.read_csv(path, sep=None, engine="python")
    except Exception:
        df = pd.read_csv(path, sep=";")
    return df.fillna("").to_csv(index=False).replace("\ufeff", "")


def _extract_text_from_excel(path):
    df = pd.read_excel(path)
    return df.fillna("").to_csv(index=False).replace("\ufeff", "")


def extract_text(path):
    file_path = Path(path)
    extension = file_path.suffix.lower().lstrip(".")

    try:
        if extension == "pdf":
            return _extract_text_from_pdf(file_path)

        if extension == "csv":
            return _extract_text_from_csv(file_path)

        if extension in {"xlsx", "xls"}:
            return _extract_text_from_excel(file_path)

        try:
            return _extract_text_from_image(file_path)
        except Exception:
            return file_path.read_text(encoding="utf-8", errors="ignore").replace("\ufeff", "")

    except Exception as e:
        return str(e).replace("\ufeff", "")


def analyser_facture(path):
    text = extract_text(path)

    return {
        "texte": text.replace("\ufeff", ""),
        "fournisseur": "Detecte automatiquement",
        "montant": "A analyser",
        "tva": "20%"
    }

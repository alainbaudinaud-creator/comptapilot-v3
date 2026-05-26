import pytesseract

from PIL import Image


def extract_text(path):

    try:

        image = Image.open(path)

        text = pytesseract.image_to_string(
            image,
            lang="fra"
        )

        return text

    except Exception as e:

        return str(e)


def analyser_facture(path):

    text = extract_text(path)

    return {
        "texte": text,
        "fournisseur": "Detecte automatiquement",
        "montant": "A analyser",
        "tva": "20%"
    }


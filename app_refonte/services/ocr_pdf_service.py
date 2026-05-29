from pathlib import Path
import pdfplumber
import fitz
import pytesseract
from PIL import Image
import io


def extraire_texte_pdf(path):
    path = Path(path)
    texte = ""

    try:
        with pdfplumber.open(str(path)) as pdf:
            for page in pdf.pages:
                texte += (page.extract_text() or "") + "\n"
    except Exception:
        pass

    if texte.strip():
        return texte.strip()

    doc = fitz.open(str(path))
    textes = []

    for page in doc:
        pix = page.get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        textes.append(pytesseract.image_to_string(img, lang="fra"))

    doc.close()

    return "\n".join(textes).strip()

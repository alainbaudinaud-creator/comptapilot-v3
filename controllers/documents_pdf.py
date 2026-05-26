
from pathlib import Path
from flask import Blueprint, render_template, send_file, request, redirect, url_for

bp_documents_pdf = Blueprint("documents_pdf", __name__)

ROOT = Path(r"C:\Users\alain\mon-projet-agent")

PDFS = {
    "balance": {
        "title": "Balance générale",
        "file": ROOT / "balance.pdf",
    },
    "grand_livre": {
        "title": "Grand livre",
        "file": ROOT / "grand_livre.pdf",
    },
    "bilan": {
        "title": "Bilan comptable",
        "file": ROOT / "bilan.pdf",
    },
    "resultat": {
        "title": "Compte de résultat",
        "file": ROOT / "compte_resultat.pdf",
    },
    "liasse": {
        "title": "Liasse fiscale",
        "file": ROOT / "liasse_complete.pdf",
    },
}

@bp_documents_pdf.route("/documents")
def documents():
    return render_template("documents/index.html", pdfs=PDFS)

@bp_documents_pdf.route("/documents/view/<name>")
def view_pdf(name):
    item = PDFS.get(name)
    if not item:
        return "Document introuvable", 404
    return send_file(item["file"], mimetype="application/pdf", as_attachment=False)

@bp_documents_pdf.route("/documents/download/<name>")
def download_pdf(name):
    item = PDFS.get(name)
    if not item:
        return "Document introuvable", 404
    return send_file(item["file"], mimetype="application/pdf", as_attachment=True)

@bp_documents_pdf.route("/documents/print/<name>")
def print_pdf(name):
    item = PDFS.get(name)
    if not item:
        return "Document introuvable", 404
    return render_template("documents/print.html", name=name, title=item["title"])

@bp_documents_pdf.route("/documents/email/<name>", methods=["GET", "POST"])
def email_pdf(name):
    item = PDFS.get(name)
    if not item:
        return "Document introuvable", 404

    if request.method == "POST":
        email = request.form.get("email")
        message = request.form.get("message")

        # Version actuelle : préparation de l'envoi.
        # Le branchement SMTP réel sera ajouté avec identifiants email sécurisés.
        return render_template(
            "documents/email_sent.html",
            title=item["title"],
            email=email,
            message=message,
            file=item["file"].name
        )

    return render_template("documents/email.html", name=name, title=item["title"])



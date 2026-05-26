
from pathlib import Path
from flask import Blueprint, render_template, send_file

bp_fiscal_documents = Blueprint("fiscal_documents", __name__)

ROOT = Path(r"C:\Users\alain\mon-projet-agent")
BASE = ROOT / "documents_officiels" / "liasse_fiscale_2026"

@bp_fiscal_documents.route("/fiscal/documents")
def fiscal_documents():
    docs = []
    if BASE.exists():
        for f in sorted(BASE.glob("*.pdf")):
            docs.append({
                "name": f.name,
                "size": f.stat().st_size,
            })
    return render_template("fiscal/documents.html", docs=docs)

@bp_fiscal_documents.route("/fiscal/documents/view/<filename>")
def fiscal_view(filename):
    return send_file(BASE / filename, mimetype="application/pdf", as_attachment=False)

@bp_fiscal_documents.route("/fiscal/documents/download/<filename>")
def fiscal_download(filename):
    return send_file(BASE / filename, mimetype="application/pdf", as_attachment=True)



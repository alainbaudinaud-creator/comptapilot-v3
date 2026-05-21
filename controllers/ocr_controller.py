from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
from pathlib import Path
from sqlalchemy import text

from database import engine
from services.ocr_service import extract_text
from services.ai_service import generate_accounting_entry

bp_ocr = Blueprint("ocr", __name__)

UPLOAD_DIR = Path("/app/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@bp_ocr.route("/ocr", methods=["GET", "POST"])
def ocr():
    result = None

    with engine.connect() as conn:
        clients = conn.execute(text("SELECT id, name FROM clients ORDER BY name")).fetchall()

    if request.method == "POST":
        file = request.files.get("file")
        client_id = request.form.get("client_id")

        if file and file.filename and client_id:
            filename = secure_filename(file.filename)
            path = UPLOAD_DIR / filename
            file.save(str(path))

            ocr_text = extract_text(str(path))
            accounting = generate_accounting_entry(ocr_text)

            with engine.begin() as conn:
                doc_id = conn.execute(text("""
                    INSERT INTO documents(filename, ocr_text, client_id)
                    VALUES(:filename, :ocr_text, :client_id)
                    RETURNING id
                """), {
                    "filename": filename,
                    "ocr_text": ocr_text,
                    "client_id": int(client_id)
                }).scalar()

                conn.execute(text("""
                    INSERT INTO accounting_entries(
                        client_id, document_id, journal, account, label, vat, status
                    )
                    VALUES(
                        :client_id, :document_id, :journal, :account, :label, :vat, 'draft'
                    )
                """), {
                    "client_id": int(client_id),
                    "document_id": doc_id,
                    "journal": accounting["journal"],
                    "account": accounting["account"],
                    "label": accounting["label"],
                    "vat": accounting["vat"]
                })

            result = {
                "filename": filename,
                "text": ocr_text,
                "accounting": accounting,
                "document_id": doc_id
            }

    return render_template("cabinet/ocr.html", result=result, clients=clients)

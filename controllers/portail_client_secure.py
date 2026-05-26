
from flask import Blueprint, render_template, request
from services.documents_auto_service import envoyer_document_client

bp_portail_client_secure = Blueprint("portail_client_secure", __name__)

@bp_portail_client_secure.route("/client")
def client_home():
    return render_template("client/index.html")

@bp_portail_client_secure.route("/client/envoyer-document", methods=["POST"])
def client_envoyer_document():
    email = request.form.get("email")
    document = request.form.get("document")
    resultat = envoyer_document_client(email, document)
    return render_template("client/resultat.html", resultat=resultat)




from pathlib import Path
from services.smtp_service import envoyer_email

ROOT = Path(r"C:\Users\alain\mon-projet-agent")

DOCUMENTS = {
    "balance": ROOT / "balance.pdf",
    "grand_livre": ROOT / "grand_livre.pdf",
    "bilan": ROOT / "bilan.pdf",
    "resultat": ROOT / "compte_resultat.pdf",
    "liasse": ROOT / "liasse_complete.pdf",
}

def envoyer_document_client(email, document):
    fichier = DOCUMENTS.get(document)

    if not fichier or not fichier.exists():
        return "DOCUMENT INTROUVABLE"

    return envoyer_email(
        destinataire=email,
        sujet=f"Document Comptapilot - {document}",
        contenu=f"""
Bonjour,

Veuillez trouver ci-joint votre document Comptapilot : {document}.

Cordialement,
IFG SOLUTION
""",
        piece_jointe=str(fichier)
    )

def envoyer_liasse_client(email):
    return envoyer_document_client(email, "liasse")


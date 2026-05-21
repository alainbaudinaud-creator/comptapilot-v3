
from flask import Blueprint, render_template, request
from controllers.auth import login_required

from services.signatures_service import signer_document

signatures_routes = Blueprint('signatures', __name__)


@signatures_routes.route(
    '/signature-electronique-renforcee',
    methods=['GET', 'POST']
)
@login_required
def signature_electronique_renforcee():

    if request.method == 'GET':

        return render_template(
            'signature_electronique_renforcee.html'
        )

    document = (
        request.form.get('document')
        or "Document ComptaPilot"
    )

    signataire = (
    request.form.get('signataire')
    or "Utilisateur ComptaPilot"
)

    resultat = signer_document(
        document,
        signataire
    )

    return render_template(
        'signature_resultat.html',
        document=resultat['document'],
        signataire=resultat['signataire'],
        date_signature=resultat['date_signature'],
        empreinte=resultat['empreinte']
    )

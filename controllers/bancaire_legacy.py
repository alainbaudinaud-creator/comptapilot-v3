from flask import Blueprint, render_template
from controllers.auth import login_required

from services.bancaire_service import lister_ecritures_bancaires

bancaire_routes = Blueprint('bancaire', __name__)


@bancaire_routes.route('/rapprochement-bancaire')
@login_required
def rapprochement_bancaire():

    ecritures = lister_ecritures_bancaires()

    return render_template(
        'rapprochement.html',
        ecritures=ecritures
    )


from flask import Blueprint, render_template
from controllers.auth import login_required

from services.transmission_service import (
    enregistrer_acces_transmission,
    lister_factures_transmission
)

transmission_routes = Blueprint('transmission', __name__)


@transmission_routes.route('/transmission-factures')
@login_required
def transmission_factures():

    enregistrer_acces_transmission()

    factures = lister_factures_transmission()

    return render_template(
        'transmission_factures.html',
        factures=factures
    )

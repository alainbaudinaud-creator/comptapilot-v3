
from flask import Blueprint, render_template
from controllers.auth import login_required
import os

sauvegardes_routes = Blueprint('sauvegardes', __name__)

@sauvegardes_routes.route('/liste-sauvegardes')
@login_required
def liste_sauvegardes():

    dossier = 'C:/Users/alain/mon-projet-agent/sauvegardes'
    fichiers = []

    if os.path.exists(dossier):

        for nom in os.listdir(dossier):

            chemin = os.path.join(dossier, nom)

            if os.path.isfile(chemin):

                fichiers.append({
                    'nom': nom,
                    'chemin': chemin,
                    'taille': round(os.path.getsize(chemin) / 1024, 2)
                })

    return render_template(
        'liste_sauvegardes.html',
        fichiers=fichiers
    )



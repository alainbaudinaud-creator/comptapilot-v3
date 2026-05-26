
from flask import Blueprint, request, jsonify, render_template
from controllers.auth import login_required
from models.societe import Societe

societes_routes = Blueprint('societes', __name__)


@societes_routes.route('/ui')
@login_required
def ui():
    return render_template("societes.html")


@societes_routes.route('/', methods=['GET'])
@login_required
def get_societes():
    return jsonify([s.serialize() for s in Societe.all()])


@societes_routes.route('/add', methods=['POST'])
@login_required
def add_societe():
    data = request.get_json()

    new_societe = Societe(
        name=data.get('name'),
        address=data.get('address')
    )

    new_societe.save()
    return jsonify(new_societe.serialize()), 201



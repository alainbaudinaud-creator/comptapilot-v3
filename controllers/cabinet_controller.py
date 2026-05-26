
from flask import Blueprint, render_template

bp_cabinet = Blueprint("cabinet", __name__)

@bp_cabinet.route("/cabinet")
def cabinet():

    return render_template("dashboard/cabinet.html")



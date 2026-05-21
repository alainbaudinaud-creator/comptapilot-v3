
from flask import Blueprint, render_template

bp_dashboard_auto = Blueprint("dashboard_auto", __name__)

@bp_dashboard_auto.route("/")
def home():
    return render_template("dashboard/index.html")

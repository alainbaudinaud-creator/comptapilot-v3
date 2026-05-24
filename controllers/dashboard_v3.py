from flask import Blueprint, render_template

from controllers.auth import login_required
from services.permission_service import permission_required


bp_dashboard_v3 = Blueprint("dashboard_v3", __name__)


@bp_dashboard_v3.route("/")
@login_required
@permission_required("ACCESS_ECRITURES")
def dashboard_v3_home():

    return render_template("dashboard_v3.html")


@bp_dashboard_v3.route("/dashboard-v3")
@login_required
@permission_required("ACCESS_ECRITURES")
def dashboard_v3():

    return render_template("dashboard_v3.html")

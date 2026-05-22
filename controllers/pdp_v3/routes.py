from flask import Blueprint, render_template

bp_pdp_v3 = Blueprint("pdp_v3", __name__)

@bp_pdp_v3.route("/pdp-v3")
def pdp_v3():
    return render_template("pdp_v3/index.html")

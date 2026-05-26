from flask import Blueprint, render_template, session, redirect

bp_dashboard_v3 = Blueprint("dashboard_v3", __name__)

@bp_dashboard_v3.route("/dashboard-v3")
def dashboard_v3():
    if not session.get("user"):
        return redirect("/login")
    return render_template("dashboard_v3.html")

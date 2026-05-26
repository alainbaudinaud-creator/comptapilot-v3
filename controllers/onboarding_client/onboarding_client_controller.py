from flask import Blueprint, redirect, render_template, session

bp_onboarding_client = Blueprint("onboarding_client", __name__)


@bp_onboarding_client.route("/onboarding-client")
def onboarding_client_index():

    if not session.get("user_id"):
        return redirect("/login")

    return render_template("onboarding_client_v3.html")


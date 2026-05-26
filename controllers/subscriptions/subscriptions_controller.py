from flask import Blueprint, redirect, render_template, session

bp_subscriptions = Blueprint("subscriptions", __name__)


@bp_subscriptions.route("/subscriptions")
def subscriptions_index():

    if not session.get("user_id"):
        return redirect("/login")

    return render_template("subscriptions_v3.html")




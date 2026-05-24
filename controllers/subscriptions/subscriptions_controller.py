from flask import Blueprint, redirect, render_template_string, session, url_for

bp_subscriptions = Blueprint("subscriptions", __name__)


@bp_subscriptions.route("/subscriptions")
def subscriptions_index():
    if not session.get("user_id"):
        return redirect("/auth/login")

    return render_template_string("""
    <!doctype html>
    <html lang="fr">
    <head>
        <meta charset="utf-8">
        <title>Abonnements - ComptaPilot V3</title>
    </head>
    <body>
        <h1>Abonnements ComptaPilot V3</h1>
        <p>Module abonnements opérationnel.</p>
    </body>
    </html>
    """)

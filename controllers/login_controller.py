from flask import Blueprint
from flask import request
from flask import session
from flask import redirect

bp_login = Blueprint("login", __name__)


@bp_login.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            "admin@comptapilot.local"
        )

        session["user"] = email
        session["role"] = "admin"

        return redirect("/dashboard-v3")

    return """
    <!DOCTYPE html>
    <html lang='fr'>

    <head>

        <meta charset='UTF-8'>

        <title>ComptaPilot V3</title>

        <meta
            name='viewport'
            content='width=device-width, initial-scale=1'
        >

        <link
            rel='stylesheet'
            href='/static/v3/css/login-v3.css'
        >

    </head>

    <body>

        <div class='login-bg'></div>

        <div class='login-card'>

            <div class='login-logo'>
                Compta<span>Pilot</span>
            </div>

            <div class='login-subtitle'>
                Plateforme comptable intelligente nouvelle génération.
                Pilotage cabinet, automatisation et IA métier.
            </div>

            <form method='post'>

                <input
                    class='login-input'
                    type='email'
                    name='email'
                    value='admin@comptapilot.local'
                    placeholder='Adresse email'
                >

                <button
                    class='login-button'
                    type='submit'
                >
                    Accéder au cockpit V3
                </button>

            </form>

            <div class='login-footer'>
                ComptaPilot V3 • Cabinet augmenté IA
            </div>

        </div>

    </body>

    </html>
    """


@bp_login.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


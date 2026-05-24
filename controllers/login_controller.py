from flask import Blueprint
from flask import request
from flask import session
from flask import redirect
from flask import render_template

bp_login = Blueprint("login", __name__)


@bp_login.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "admin@comptapilot.local")

        session["user"] = email
        session["role"] = "admin"

        return redirect("/dashboard-v3")

    return """
    <html>
    <body style='font-family:Arial;padding:40px'>
        <h2>ComptaPilot Login</h2>

        <form method='post'>
            <input type='email' name='email' value='admin@comptapilot.local'/>
            <br><br>
            <button type='submit'>Connexion</button>
        </form>
    </body>
    </html>
    """
    

@bp_login.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


from flask import Flask
import sqlite3

app = Flask(__name__)
app.secret_key = "comptapilot_secret_key"


def init_db():
    conn = sqlite3.connect("db.sqlite")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS societes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS plan_comptable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT,
            libelle TEXT,
            type TEXT,
            societe_id INTEGER
        )
    """)

    c.execute("PRAGMA table_info(plan_comptable)")
    colonnes = [col[1] for col in c.fetchall()]
    if "societe_id" not in colonnes:
        c.execute("ALTER TABLE plan_comptable ADD COLUMN societe_id INTEGER")

        c.execute("""
        CREATE TABLE IF NOT EXISTS ecritures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_ecriture TEXT,
            piece TEXT,
            libelle TEXT,
            debit REAL DEFAULT 0,
            credit REAL DEFAULT 0,
            societe_id INTEGER,
            compte_id INTEGER,
            FOREIGN KEY (societe_id) REFERENCES societes(id),
            FOREIGN KEY (compte_id) REFERENCES plan_comptable(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS clotures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            societe_id INTEGER UNIQUE,
            date_cloture TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    
    conn.commit()
    conn.close()


init_db()

from controllers.auth import auth_routes
from controllers.gestion_societes import societes_routes
from controllers.gestion_plan_comptable import plan_comptable_routes
from controllers.gestion_ecritures import ecritures_routes
from controllers.exportation import exportation_routes
from controllers.balance import balance_routes
from controllers.grand_livre import grand_livre_routes

app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(societes_routes, url_prefix='/societes')
app.register_blueprint(plan_comptable_routes, url_prefix='/plan-comptable')
app.register_blueprint(ecritures_routes, url_prefix='/ecritures')
app.register_blueprint(exportation_routes, url_prefix='/export')
app.register_blueprint(balance_routes, url_prefix='/balance')
app.register_blueprint(grand_livre_routes, url_prefix='/grand-livre')


@app.route("/")
def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>ComptaPilot SaaS</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container py-5">
            <h1 class="mb-4">ComptaPilot SaaS</h1>
            <p class="lead">Mini logiciel comptable : sociétés, plan comptable, écritures, journal, export et balance.</p>

            <div class="mb-4">
                <a class="btn btn-outline-primary" href="/auth/login">Connexion</a>
                <a class="btn btn-outline-secondary" href="/auth/register">Créer un compte</a>
                <a class="btn btn-outline-danger" href="/auth/logout">Déconnexion</a>
            </div>

            <div class="row mt-4">
                <div class="col-md-3">
                    <a class="btn btn-primary w-100 mb-3" href="/societes/ui">Sociétés</a>
                </div>

                <div class="col-md-3">
                    <a class="btn btn-success w-100 mb-3" href="/plan-comptable/ui">Plan comptable</a>
                </div>

                <div class="col-md-3">
                    <a class="btn btn-warning w-100 mb-3" href="/ecritures/ui">Écritures</a>
                </div>

                <div class="col-md-3">
                    <a class="btn btn-dark w-100 mb-3" href="/ecritures/journal">Journal</a>
                </div>

                <div class="col-md-3">
                    <a class="btn btn-info w-100 mb-3" href="/export/">Export</a>
                </div>

                <div class="col-md-3">
                    <a class="btn btn-secondary w-100 mb-3" href="/balance/">Balance</a>
                </div>

                <div class="col-md-3">
                    <a class="btn btn-outline-dark w-100 mb-3" href="/grand-livre/">Grand livre</a>
                </div>

                <div class="col-md-3">
                    <a class="btn btn-primary w-100 mb-3" href="/ecritures/facture/ui">Facture client</a>
                </div>

                <div class="col-md-3">
                    <a class="btn btn-info w-100 mb-3" href="/ecritures/dashboard">Dashboard financier</a>
                </div>
                <div class="col-md-3">
                    <a class="btn btn-danger w-100 mb-3" href="/ecritures/tva/ui">TVA simplifiée</a>
            </div>
            </div>
        </div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)

from controllers.premium_saas_routes import premium_saas
from flask import Flask, redirect, render_template, request, jsonify
from flask_mail import Mail
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_limiter.errors import RateLimitExceeded
from datetime import timedelta
from dotenv import load_dotenv
import os
import config

from extensions import db, limiter, csrf

from controllers.auth import auth_routes
from controllers.gestion_societes import societes_routes
from controllers.gestion_plan_comptable import plan_comptable_routes
from controllers.gestion_ecritures import ecritures_routes
from controllers.exportation import exportation_routes
from controllers.audit import audit_routes
from controllers.signatures import signatures_routes
from controllers.sauvegardes import sauvegardes_routes
from controllers.transmission import transmission_routes
from controllers.bancaire_legacy import bancaire_routes
from controllers.dashboard import dashboard_routes
from controllers.ia_v7 import ia_v7_routes
from controllers.api_v1 import api_v1_routes
from controllers.api_dashboard import api_dashboard_routes
from controllers.api_auth import api_auth_routes
from controllers.rgpd_controller import rgpd_routes

from services.log_service import log_info, log_erreur
from services.scheduler_service import demarrer_scheduler
from services.http_logger_service import log_http_request
from controllers.registre_rgpd_controller import registre_rgpd_routes
from controllers.admin_users import admin_users_routes
from controllers.comptabilite.routes import comptabilite_routes
from controllers.facturation.routes import facturation_routes
from controllers.ged.routes import ged_routes
from controllers.ia.routes import ia_routes
from controllers.fiscal.routes import fiscal_routes
from controllers.bancaire.routes import bancaire_routes_v2
from controllers.supervision.routes import supervision_routes_v2
from controllers.production.routes import production_routes
from controllers.pdp.routes import pdp_routes
from controllers.pdp_v3.routes import bp_pdp_v3
from services.permission_service import has_permission

load_dotenv()

app = Flask(__name__)
@app.context_processor
def inject_permissions():

    def can(permission):
        return has_permission(permission)

    return dict(can=can)

MAINTENANCE_MODE = False

app.secret_key = config.SECRET_KEY
app.config["SESSION_COOKIE_HTTPONLY"] = True

app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=2)

app.config["SESSION_COOKIE_SECURE"] = False
app.config["WTF_CSRF_CHECK_DEFAULT"] = False

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://comptapilot:comptapilot@postgres:5432/comptapilot_v3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)

app.config["MAIL_SERVER"] = config.MAIL_SERVER
app.config["MAIL_PORT"] = config.MAIL_PORT
app.config["MAIL_USE_TLS"] = config.MAIL_USE_TLS
app.config["MAIL_USERNAME"] = config.MAIL_USERNAME
app.config["MAIL_PASSWORD"] = config.MAIL_PASSWORD
app.config["MAIL_DEFAULT_SENDER"] = config.MAIL_DEFAULT_SENDER

db.init_app(app)
# limiter.init_app(app)
# # csrf.init_app(app)  # TEMP DESACTIVE LOGIN  # TEMP désactivé pour login OVH

@app.before_request
def enforce_csrf_except_login():
    public_csrf_paths = (
        "/login",
        "/static",
        "/favicon.ico",
        "/api/v3/",
        "/public-api",
        "/public-dynamic"
    )

    if request.method in ("POST", "PUT", "PATCH", "DELETE"):
        if not request.path.startswith(public_csrf_paths):
            pass  # TEMP csrf.protect désactivé

mail = Mail(app)
jwt = JWTManager(app)
swagger = Swagger(app)
app.register_blueprint(premium_saas)

@app.errorhandler(RateLimitExceeded)
def handle_rate_limit(e):
    return jsonify({
        "error": "Trop de tentatives",
        "detail": str(e.description)
    }), 429


@app.before_request
def csrf_exempt_public_dynamic():
    if request.path.startswith("/public-dynamic"):
        setattr(request, "_csrf_exempt", True)
        return

@app.before_request
def maintenance_mode():
    # PUBLIC API V3 - cockpit KPI
    if request.path.startswith("/api/v3/kpi"):
        return
    if request.path.startswith("/api/v3/supervision"):
        return

    allowed_routes = [
        "auth.login",
        "static"
    ]

    if MAINTENANCE_MODE:

        if request.endpoint not in allowed_routes:

            return render_template(
                "maintenance.html"
            ), 503

@app.after_request
def after_request(response):

    log_http_request(request, response.status_code)

    response.headers["X-Frame-Options"] = "DENY"

    response.headers["X-Content-Type-Options"] = "nosniff"

    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    response.headers["X-XSS-Protection"] = "1; mode=block"

    response.headers["Content-Security-Policy"] = (
    "default-src 'self'; "
    "style-src 'self' 'unsafe-inline'; "
    "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
    "connect-src 'self' https://cdn.jsdelivr.net"
)

    return response

app.register_blueprint(auth_routes, url_prefix="/auth")
app.register_blueprint(societes_routes, url_prefix="/societe")
app.register_blueprint(plan_comptable_routes, url_prefix="/plan-comptable")
app.register_blueprint(ecritures_routes, url_prefix="/ecritures")
app.register_blueprint(exportation_routes, url_prefix="/exportations")
app.register_blueprint(audit_routes, url_prefix="/ecritures")
app.register_blueprint(signatures_routes, url_prefix="/ecritures")
app.register_blueprint(sauvegardes_routes, url_prefix="/ecritures")
app.register_blueprint(transmission_routes, url_prefix="/ecritures")
app.register_blueprint(bancaire_routes, url_prefix="/ecritures")
app.register_blueprint(dashboard_routes, url_prefix="/ecritures")
app.register_blueprint(ia_v7_routes, url_prefix="/ecritures")
app.register_blueprint(api_v1_routes, url_prefix="/api/v1")
app.register_blueprint(api_dashboard_routes)
app.register_blueprint(api_auth_routes, url_prefix="/api/v1")
app.register_blueprint(rgpd_routes)
app.register_blueprint(registre_rgpd_routes)
app.register_blueprint(admin_users_routes)
app.register_blueprint(comptabilite_routes, url_prefix='/comptabilite')
app.register_blueprint(facturation_routes, url_prefix='/facturation')
app.register_blueprint(ged_routes, url_prefix='/ged-v3')
app.register_blueprint(ia_routes, url_prefix='/ia-v3')
app.register_blueprint(fiscal_routes, url_prefix='/fiscal-v3')
app.register_blueprint(bancaire_routes_v2, url_prefix='/bancaire-v3')
app.register_blueprint(supervision_routes_v2, url_prefix='/supervision-v3')
app.register_blueprint(production_routes, url_prefix='/production-v3')
app.register_blueprint(pdp_routes, url_prefix='/pdp-v3')
app.register_blueprint(bp_pdp_v3)

@app.route("/favicon.ico")
def favicon():
    return "", 204

@app.route("/bootstrap-admin")
def bootstrap_admin_direct():

    from werkzeug.security import generate_password_hash
    from sqlalchemy import text
    from services.db_postgres import get_engine

    with get_engine().begin() as conn:

        existing = conn.execute(text("""
            SELECT id
            FROM users
            WHERE username = :username
        """), {
            "username": "admin"
        }).fetchone()

        if not existing:

            conn.execute(text("""
                INSERT INTO users (username, password)
                VALUES (:username, :password)
            """), {
                "username": "admin",
                "password": generate_password_hash("AdminComptaPilot2026!")
            })

            return "SUPER ADMIN cree"

    return "SUPER ADMIN deja existant"

@app.route("/")
def home():
    return render_template("accueil.html")

@app.route("/mentions-legales")
def mentions_legales():
    return render_template("mentions_legales.html")

@app.route("/politique-confidentialite")
def politique_confidentialite():
    return render_template("politique_confidentialite.html")

# @app.errorhandler(Exception)
# def gerer_erreur_globale(erreur):
#     log_erreur(str(erreur))
#
#     return render_template(
#         "erreur.html",
#         erreur=str(erreur)
#     ), 500

@app.errorhandler(500)
def erreur_500(e):
    return render_template("errors/500.html"), 500




@app.route("/v3/ecritures")
def v3_ecritures_direct():
    from sqlalchemy import text
    from database import engine

    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS ecritures (
                id SERIAL PRIMARY KEY,
                journal VARCHAR(20),
                compte VARCHAR(20),
                libelle TEXT,
                debit NUMERIC(14,2) DEFAULT 0,
                credit NUMERIC(14,2) DEFAULT 0,
                date_ecriture DATE DEFAULT CURRENT_DATE
            )
        """))

        rows = conn.execute(text("""
            SELECT id, journal, compte, libelle, debit, credit, date_ecriture
            FROM ecritures
            ORDER BY id DESC
        """)).fetchall()

    html = """
    <html><head><title>Écritures V3</title>
    <style>
    body{background:#050816;color:white;font-family:Arial;padding:40px}
    h1{font-size:42px}
    table{width:100%;border-collapse:collapse;background:#11182d;border-radius:18px;overflow:hidden}
    td,th{padding:14px;border-bottom:1px solid #24304f}
    th{background:#17203b;text-align:left;color:#8fa3c7}
    a{color:#22d3ee}
    </style></head><body>
    <h1>Écritures Comptables V3</h1>
    <p><a href='/dashboard-v3'>← Retour cockpit</a></p>
    <table>
    <tr><th>ID</th><th>Journal</th><th>Compte</th><th>Libellé</th><th>Débit</th><th>Crédit</th><th>Date</th></tr>
    """

    for r in rows:
        html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td><td>{r[6]}</td></tr>"

    html += "</table></body></html>"
    return html








# === ComptaPilot V3 - API CRUD mutualisée propre ===
@app.route("/api/module/ecritures", methods=["GET", "POST"])
def api_module_ecritures_clean():
    from flask import request, jsonify
    from sqlalchemy import text
    from database import engine

    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS ecritures (
                id SERIAL PRIMARY KEY,
                journal VARCHAR(20),
                compte VARCHAR(20),
                libelle TEXT,
                debit NUMERIC(14,2) DEFAULT 0,
                credit NUMERIC(14,2) DEFAULT 0,
                date_ecriture DATE DEFAULT CURRENT_DATE
            )
        """))

        if request.method == "POST":
            data = request.get_json(silent=True) or {}
            result = conn.execute(text("""
                INSERT INTO ecritures (journal, compte, libelle, debit, credit)
                VALUES (:journal, :compte, :libelle, :debit, :credit)
                RETURNING id
            """), {
                "journal": data.get("journal", ""),
                "compte": data.get("compte", ""),
                "libelle": data.get("libelle", ""),
                "debit": data.get("debit") or 0,
                "credit": data.get("credit") or 0,
            }).scalar()

            return jsonify({"success": True, "id": result})

        rows = conn.execute(text("""
            SELECT id, journal, compte, libelle, debit, credit, date_ecriture
            FROM ecritures
            ORDER BY id DESC
            LIMIT 500
        """)).mappings().all()

        return jsonify({"rows": [dict(r) for r in rows]})


@app.route("/api/module/ecritures/<int:item_id>", methods=["DELETE"])
def api_module_ecritures_delete_clean(item_id):
    from flask import jsonify
    from sqlalchemy import text
    from database import engine

    with engine.begin() as conn:
        conn.execute(text("DELETE FROM ecritures WHERE id = :id"), {"id": item_id})

    return jsonify({"success": True})
# === Fin API CRUD mutualisée propre ===




# === ComptaPilot V3 - API publique CRUD ===
@app.route("/public-api/ecritures", methods=["GET", "POST"])
def public_api_ecritures():
    from flask import request, jsonify
    from sqlalchemy import text
    from database import engine

    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS ecritures (
                id SERIAL PRIMARY KEY,
                journal VARCHAR(20),
                compte VARCHAR(20),
                libelle TEXT,
                debit NUMERIC(14,2) DEFAULT 0,
                credit NUMERIC(14,2) DEFAULT 0,
                date_ecriture DATE DEFAULT CURRENT_DATE
            )
        """))

        if request.method == "POST":
            data = request.get_json(silent=True) or {}
            new_id = conn.execute(text("""
                INSERT INTO ecritures (journal, compte, libelle, debit, credit)
                VALUES (:journal, :compte, :libelle, :debit, :credit)
                RETURNING id
            """), {
                "journal": data.get("journal", ""),
                "compte": data.get("compte", ""),
                "libelle": data.get("libelle", ""),
                "debit": data.get("debit") or 0,
                "credit": data.get("credit") or 0
            }).scalar()

            return jsonify({"success": True, "id": new_id})

        rows = conn.execute(text("""
            SELECT id, journal, compte, libelle, debit, credit, date_ecriture
            FROM ecritures
            ORDER BY id DESC
            LIMIT 500
        """)).mappings().all()

        return jsonify({"rows": [dict(r) for r in rows]})


@app.route("/public-api/ecritures/<int:item_id>", methods=["DELETE"])
def public_api_ecritures_delete(item_id):
    from flask import jsonify
    from sqlalchemy import text
    from database import engine

    with engine.begin() as conn:
        conn.execute(text("DELETE FROM ecritures WHERE id = :id"), {"id": item_id})

    return jsonify({"success": True})
# === Fin API publique CRUD ===



from controllers.dynamic_api import bp_dynamic_api
try:
    csrf.exempt(bp_dynamic_api)
except Exception as e:
    print("CSRF exempt dynamic_api:", e)
app.register_blueprint(bp_dynamic_api)



# === RESTAURATION ROUTES METIER COMPTAPILOT V3 ===

@app.route("/ecritures/saisie-rapide", methods=["GET"])
def restauration_saisie_rapide_v3():
    return """
    <h1>ComptaPilot V3 - Saisie rapide</h1>
    <p>Route restaurée.</p>
    <p><a href="/">Retour Dashboard</a></p>
    <p><a href="/societe/ui">Sociétés clientes</a></p>
    """

@app.route("/societe/ui", methods=["GET"])
def restauration_societes_clientes_v3():
    return """
    <h1>ComptaPilot V3 - Sociétés clientes</h1>
    <p>Route restaurée.</p>
    <p><a href="/">Retour Dashboard</a></p>
    <p><a href="/societe/add">Créer une société</a></p>
    <p><a href="/ecritures/saisie-rapide">Saisie rapide</a></p>
    """

@app.route("/v3/ecritures", methods=["GET"])
@app.route("/v3/ecritures/", methods=["GET"])
@app.route("/public/v3/ecritures", methods=["GET"])
def restauration_ecritures_v3():
    return restauration_saisie_rapide_v3()



# === REDIRECTION DASHBOARD RACINE ===
@app.route("/dashboard")
def dashboard_redirect_root():
    from flask import redirect
    return redirect("/ecritures/dashboard")

if __name__ == "__main__":
    log_info("DÃ©marrage application ComptaPilot")
    demarrer_scheduler()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
)

# DIRECT LOGIN ROUTES

from flask import request
from flask import session
from flask import redirect
from flask import render_template_string


# === CABINET WORKFLOW SAAS ===
@app.route("/cabinet/workflow")
def cabinet_workflow_saas():
    collaborateurs = []
    permissions = []
    taches = []

    try:
        from database import engine
        from sqlalchemy import text

        with engine.connect() as conn:
            collaborateurs = conn.execute(text("""
                SELECT nom, email, role, actif
                FROM cabinet_collaborateurs
                ORDER BY nom
            """)).mappings().all()

            permissions = conn.execute(text("""
                SELECT role, module, peut_lire, peut_ecrire, peut_valider
                FROM cabinet_permissions
                ORDER BY role, module
            """)).mappings().all()

            taches = conn.execute(text("""
                SELECT
                    t.titre,
                    t.module,
                    t.statut,
                    t.priorite,
                    c.nom AS assigne_a,
                    t.echeance
                FROM cabinet_workflow_taches t
                LEFT JOIN cabinet_collaborateurs c ON c.id = t.assigne_a
                ORDER BY t.echeance NULLS LAST, t.priorite DESC, t.created_at DESC
            """)).mappings().all()
    except Exception as e:
        print("Erreur cabinet_workflow_saas:", e)

    return render_template(
        "cabinet_workflow.html",
        collaborateurs=collaborateurs,
        permissions=permissions,
        taches=taches
    )



# === CENTRE FISCAL PREMIUM ===
@app.route("/centre-fiscal")
def centre_fiscal():

    notifications = []
    immobilisations = []
    rapprochements = []

    try:
        from database import engine
        from sqlalchemy import text

        with engine.connect() as conn:

            notifications = conn.execute(text("""
                SELECT *
                FROM notifications_workflow
                ORDER BY created_at DESC
                LIMIT 20
            """)).mappings().all()

            immobilisations = conn.execute(text("""
                SELECT *
                FROM immobilisations
                ORDER BY created_at DESC
                LIMIT 20
            """)).mappings().all()

            rapprochements = conn.execute(text("""
                SELECT *
                FROM rapprochements_bancaires
                ORDER BY created_at DESC
                LIMIT 20
            """)).mappings().all()

    except Exception as e:
        print(e)

    return render_template(
        "centre_fiscal.html",
        notifications=notifications,
        immobilisations=immobilisations,
        rapprochements=rapprochements
    )


@app.route("/login", methods=["GET", "POST"])
@csrf.exempt
def direct_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "AdminComptaPilot2026!":

            session["user"] = "admin"

            return redirect("/")

        return "Identifiants invalides"

    return render_template_string("""

    <html>
    <head>
        <title>ComptaPilot V3 Login</title>

        <style>

            body{
                background:#0b1120;
                color:white;
                font-family:Arial;
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
            }

            .box{
                background:#111827;
                padding:40px;
                border-radius:20px;
                width:360px;
                box-shadow:0 20px 60px rgba(0,0,0,.4);
            }

            input{
                width:100%;
                padding:14px;
                margin-top:14px;
                border-radius:12px;
                border:none;
                background:#1f2937;
                color:white;
            }

            button{
                width:100%;
                padding:14px;
                margin-top:20px;
                border:none;
                border-radius:12px;
                background:#6366f1;
                color:white;
                font-weight:bold;
                cursor:pointer;
            }

        </style>

    </head>

    <body>

        <div class="box">

            <h1>ComptaPilot V3</h1>

            <form method="POST">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">

                <input name="username" placeholder="Utilisateur">

                <input type="password" name="password" placeholder="Mot de passe">

                <button type="submit">
                    Connexion
                </button>

            </form>

        </div>

    </body>

    </html>

    """)

from controllers.kpi_v3 import bp_kpi_v3

app.register_blueprint(bp_kpi_v3)

@app.before_request
def protect_app():
    public_paths = [
        "/login",
        "/register",
        "/static",
        "/favicon.ico",
        "/api/v3/kpi",
        "/api/v3/supervision",
        "/public-api",
        "/public-dynamic"
    ]

    for path in public_paths:
        if request.path.startswith(path):
            return

    if request.path.startswith("/api/v3/"):
        return

    if "user" not in session and "user_id" not in session:
        return redirect("/login")

from controllers.public_kpi import bp_public_kpi

app.register_blueprint(bp_public_kpi)

from controllers.ecritures_v3 import bp_ecritures_v3

app.register_blueprint(bp_ecritures_v3)



@app.route("/v3/ecritures/")
def v3_ecritures_direct_slash():
    return v3_ecritures_direct()

@app.route("/public/v3/ecritures")
def public_v3_ecritures_direct():
    return v3_ecritures_direct()






@app.route("/")
def dashboard():
    return render_template("dashboard.html")

# === ROUTES DE SECOURS ERP V3 - RESTAURATION POST MIGRATION ===

@app.route("/ecritures/saisie-rapide", methods=["GET"])
def route_saisie_rapide_secours():
    return render_template("saisie_rapide.html")

@app.route("/v3/ecritures", methods=["GET"])
@app.route("/v3/ecritures/", methods=["GET"])
@app.route("/public/v3/ecritures", methods=["GET"])
def route_v3_ecritures_secours():
    return render_template("saisie_rapide.html")

@app.route("/societe/ui", methods=["GET"])
def route_societes_clientes_secours():
    return render_template("societes_clientes.html")

# === COCKPIT CABINET DYNAMIQUE V3 ===
@app.route("/cockpit-cabinet", methods=["GET"])
def cockpit_cabinet_dynamique_v3():
    from flask import render_template
    from sqlalchemy import text

    def scalar_safe(sql):
        try:
            with engine.connect() as conn:
                return conn.execute(text(sql)).scalar() or 0
        except Exception:
            return 0

    def rows_safe(sql):
        try:
            with engine.connect() as conn:
                return conn.execute(text(sql)).mappings().all()
        except Exception:
            return []

    kpis = {
        "nb_societes": scalar_safe("SELECT COUNT(*) FROM societes_clientes_premium"),
        "nb_ecritures": scalar_safe("SELECT COUNT(*) FROM ecritures_premium"),
        "nb_immobilisations": scalar_safe("SELECT COUNT(*) FROM immobilisations"),
        "nb_factures": scalar_safe("SELECT COUNT(*) FROM factures"),
        "nb_emprunts": scalar_safe("SELECT COUNT(*) FROM emprunts_bancaires"),
    }

    societes = rows_safe("""
        SELECT id, nom, ville, statut
        FROM societes_clientes_premium
        ORDER BY id DESC
        LIMIT 10
    """)

    ecritures = rows_safe("""
        SELECT id, date_ecriture, journal, compte_debit, compte_credit, libelle, montant_ttc
        FROM ecritures_premium
        ORDER BY id DESC
        LIMIT 10
    """)

    immobilisations = rows_safe("""
        SELECT id, designation, date_acquisition, valeur_origine, duree_amortissement, amortissement_annuel
        FROM immobilisations
        ORDER BY id DESC
        LIMIT 10
    """)

    alertes = []

    if kpis["nb_societes"] == 0:
        alertes.append({"message": "Aucune société cliente chargée", "niveau": "danger", "label": "Critique"})

    if kpis["nb_ecritures"] == 0:
        alertes.append({"message": "Aucune écriture comptable disponible", "niveau": "warn", "label": "À traiter"})

    if kpis["nb_immobilisations"] == 0:
        alertes.append({"message": "Aucune immobilisation enregistrée", "niveau": "warn", "label": "À enrichir"})

    if kpis["nb_factures"] == 0:
        alertes.append({"message": "Aucune facture dans le workflow", "niveau": "warn", "label": "À alimenter"})

    if not alertes:
        alertes.append({"message": "Socle métier alimenté et exploitable", "niveau": "ok", "label": "OK"})

    return render_template(
        "cockpit_cabinet_dynamique.html",
        kpis=kpis,
        societes=societes,
        ecritures=ecritures,
        immobilisations=immobilisations,
        alertes=alertes,
    )

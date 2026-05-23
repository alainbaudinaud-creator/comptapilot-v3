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
csrf.init_app(app)
mail = Mail(app)
jwt = JWTManager(app)
swagger = Swagger(app)


@app.errorhandler(RateLimitExceeded)
def handle_rate_limit(e):
    return jsonify({
        "error": "Trop de tentatives",
        "detail": str(e.description)
    }), 429

@app.before_request
def maintenance_mode():

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

if __name__ == "__main__":
    log_info("DÃ©marrage application ComptaPilot")
    demarrer_scheduler()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
)

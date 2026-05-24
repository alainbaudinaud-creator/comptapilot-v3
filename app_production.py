
from flask import Flask

from controllers.dashboard_auto import bp_dashboard_auto
from controllers.balance_generale import bp_balance
from controllers.grand_livre_auto import bp_gl
from controllers.bilan_auto import bp_bilan
from controllers.resultat_auto import bp_resultat
from controllers.documents_pdf import bp_documents_pdf
from controllers.fiscal_documents import bp_fiscal_documents
from controllers.veille_reglementaire import bp_veille_reglementaire
from controllers.teledec_controller import bp_teledec
from controllers.supervision_controller import bp_supervision
from controllers.production_controller import bp_production
from controllers.pdp_v3.routes import bp_pdp_v3
from controllers.ia_controller import bp_ia_controller
from controllers.erp_premium_controller import bp_erp_premium
from controllers.erp_advanced_controller import bp_erp_advanced
from controllers.enterprise_controller import bp_enterprise
from controllers.ocr_controller import bp_ocr
from controllers.login_controller import bp_login
from controllers.fiscal_controller import bp_fiscal
from controllers.ged_controller import bp_ged
from controllers.upload_controller import bp_upload
from api.rest_api import bp_rest_api
from controllers.cabinet_dashboard_controller import bp_cabinet_dashboard
from controllers.portail_client_secure import bp_portail_client_secure
from controllers.connecteurs_controller import bp_connecteurs
from controllers.api_saas import bp_api_saas
from controllers.cabinet_controller import bp_cabinet
from controllers.api_v3.routes import api_v3_routes
from controllers.dashboard_v3 import bp_dashboard_v3
from controllers.onboarding.onboarding_controller import bp_onboarding
from controllers.client_portal.client_portal_controller import bp_client_portal
from controllers.validation.validation_controller import bp_validation
from controllers.journal_v3.journal_controller import bp_journal_v3
from controllers.exports_v3.export_controller import bp_exports_v3
from controllers.production.production_controller import bp_production
from controllers.alerts.alerts_controller import bp_alerts
from controllers.notifications.notifications_controller import bp_notifications
from controllers.relances.relances_controller import bp_relances
from controllers.history.history_controller import bp_history
from controllers.audit_v3.audit_controller import bp_audit_v3
from controllers.security.security_controller import bp_security
from controllers.isolation.isolation_controller import bp_isolation
from controllers.client_space.client_space_controller import bp_client_space
from controllers.admin_users import admin_users_routes
from logs_v3.http_logger import install_http_logging

app = Flask(__name__)
app.config["SECRET_KEY"] = "COMPTAPILOT_SECRET_2026"

app.register_blueprint(bp_dashboard_auto)
app.register_blueprint(bp_balance)
app.register_blueprint(bp_gl)
app.register_blueprint(bp_bilan)
app.register_blueprint(bp_resultat)
app.register_blueprint(bp_documents_pdf)
app.register_blueprint(bp_fiscal_documents)
app.register_blueprint(bp_veille_reglementaire)
app.register_blueprint(bp_teledec)
app.register_blueprint(bp_supervision)
app.register_blueprint(bp_production)
app.register_blueprint(bp_alerts)
app.register_blueprint(bp_notifications)
app.register_blueprint(bp_relances)
app.register_blueprint(bp_history)
app.register_blueprint(bp_audit_v3)
app.register_blueprint(bp_security)
app.register_blueprint(bp_isolation)
app.register_blueprint(bp_client_space)
app.register_blueprint(bp_pdp_v3)
app.register_blueprint(bp_ia_controller)
app.register_blueprint(bp_erp_premium)
app.register_blueprint(bp_erp_advanced)
app.register_blueprint(bp_enterprise)
app.register_blueprint(bp_login)
app.register_blueprint(bp_fiscal)
app.register_blueprint(bp_ged)
app.register_blueprint(bp_upload)
app.register_blueprint(bp_rest_api)
app.register_blueprint(bp_cabinet_dashboard)
app.register_blueprint(bp_portail_client_secure)
app.register_blueprint(bp_connecteurs)
app.register_blueprint(bp_api_saas)
app.register_blueprint(bp_cabinet)
app.register_blueprint(api_v3_routes)
app.register_blueprint(bp_dashboard_v3)
app.register_blueprint(bp_onboarding)
app.register_blueprint(bp_client_portal)
app.register_blueprint(bp_validation)
app.register_blueprint(bp_journal_v3)
app.register_blueprint(bp_exports_v3)
app.register_blueprint(admin_users_routes)

install_http_logging(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


app.register_blueprint(bp_ocr)




















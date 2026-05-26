import importlib
from datetime import datetime


MODULES = [
    "app_production",
    "controllers.onboarding.onboarding_controller",
    "controllers.client_portal.client_portal_controller",
    "controllers.validation.validation_controller",
    "controllers.journal_v3.journal_controller",
    "controllers.exports_v3.export_controller",
    "controllers.production.production_controller",
    "controllers.alerts.alerts_controller",
    "controllers.notifications.notifications_controller",
    "controllers.relances.relances_controller",
    "controllers.history.history_controller",
    "controllers.audit_v3.audit_controller",
    "services_v3.ocr.ocr_service",
    "services_v3.precompta_ai.precompta_ai_service",
    "services_v3.validation.validation_service",
    "services_v3.ecritures.ecriture_service",
    "services_v3.exports.export_service",
    "services_v3.production.production_service",
    "services_v3.alerts.alerts_service",
    "services_v3.notifications.notifications_service",
    "services_v3.relances.relances_service",
    "services_v3.history.history_service",
    "services_v3.audit.audit_service",
]


def run_quality_check():

    errors = []

    print("=== COMPTAPILOT V3 QUALITY CHECK ===")
    print("Date:", datetime.utcnow().isoformat())
    print()

    for module_name in MODULES:
        try:
            importlib.import_module(module_name)
            print("[OK]", module_name)
        except Exception as exc:
            print("[ERROR]", module_name, "=>", exc)
            errors.append(
                {
                    "module": module_name,
                    "error": str(exc)
                }
            )

    print()
    print("Modules testes:", len(MODULES))
    print("Erreurs:", len(errors))

    if errors:
        print()
        print("QUALITY CHECK FAILED")
        raise SystemExit(1)

    print()
    print("QUALITY CHECK OK")


if __name__ == "__main__":
    run_quality_check()


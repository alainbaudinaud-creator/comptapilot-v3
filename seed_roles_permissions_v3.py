from database import engine
from sqlalchemy import text


roles = [
    ("ADMIN_CABINET", "Administrateur cabinet", "Accès complet cabinet"),
    ("COLLABORATEUR", "Collaborateur", "Production et validation comptable"),
    ("CLIENT", "Client", "Accès portail client uniquement"),
]

permissions = [
    ("ACCESS_ONBOARDING", "Accès onboarding", "onboarding"),
    ("ACCESS_CLIENT_PORTAL", "Accès portail client", "client_portal"),
    ("ACCESS_DOCUMENTS", "Accès documents", "documents"),
    ("ACCESS_OCR", "Accès OCR", "ocr"),
    ("ACCESS_PRECOMPTA", "Accès précompta", "precompta"),
    ("ACCESS_VALIDATION", "Accès validation", "validation"),
    ("ACCESS_ECRITURES", "Accès écritures", "ecritures"),
    ("ACCESS_JOURNAL", "Accès journal", "journal"),
    ("ACCESS_EXPORTS", "Accès exports", "exports"),
    ("ACCESS_PRODUCTION", "Accès production", "production"),
    ("ACCESS_ALERTS", "Accès alertes", "alerts"),
    ("ACCESS_NOTIFICATIONS", "Accès notifications", "notifications"),
    ("ACCESS_RELANCES", "Accès relances", "relances"),
    ("ACCESS_HISTORY", "Accès historique", "history"),
    ("ACCESS_AUDIT", "Accès audit", "audit"),
    ("ADMIN_USERS", "Administration utilisateurs", "users"),
]

role_permissions = {
    "ADMIN_CABINET": [p[0] for p in permissions],
    "COLLABORATEUR": [
        "ACCESS_DOCUMENTS",
        "ACCESS_OCR",
        "ACCESS_PRECOMPTA",
        "ACCESS_VALIDATION",
        "ACCESS_ECRITURES",
        "ACCESS_JOURNAL",
        "ACCESS_EXPORTS",
        "ACCESS_PRODUCTION",
        "ACCESS_ALERTS",
        "ACCESS_NOTIFICATIONS",
        "ACCESS_RELANCES",
        "ACCESS_HISTORY",
        "ACCESS_AUDIT",
    ],
    "CLIENT": [
        "ACCESS_CLIENT_PORTAL",
        "ACCESS_DOCUMENTS",
    ],
}


with engine.begin() as conn:

    for code, label, description in roles:
        conn.execute(
            text(
                """
                INSERT INTO roles_v3 (code, label, description)
                VALUES (:code, :label, :description)
                ON CONFLICT (code) DO UPDATE
                SET label = EXCLUDED.label,
                    description = EXCLUDED.description
                """
            ),
            {
                "code": code,
                "label": label,
                "description": description
            }
        )

    for code, label, module in permissions:
        conn.execute(
            text(
                """
                INSERT INTO permissions_v3 (code, label, module)
                VALUES (:code, :label, :module)
                ON CONFLICT (code) DO UPDATE
                SET label = EXCLUDED.label,
                    module = EXCLUDED.module
                """
            ),
            {
                "code": code,
                "label": label,
                "module": module
            }
        )

    for role_code, permission_codes in role_permissions.items():
        for permission_code in permission_codes:
            conn.execute(
                text(
                    """
                    INSERT INTO role_permissions_v3 (
                        role_code,
                        permission_code
                    )
                    SELECT :role_code, :permission_code
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM role_permissions_v3
                        WHERE role_code = :role_code
                        AND permission_code = :permission_code
                    )
                    """
                ),
                {
                    "role_code": role_code,
                    "permission_code": permission_code
                }
            )

print("Seed roles permissions V3 OK")


from database import engine
from sqlalchemy import text


plans = [
    ("STARTER", "Starter", 49, 5, 2, 500),
    ("PRO", "Pro Cabinet", 149, 30, 10, 5000),
    ("ENTERPRISE", "Enterprise", 399, 999, 100, 100000),
]


with engine.begin() as conn:

    for plan in plans:

        conn.execute(
            text(
                """
                INSERT INTO subscription_plans_v3 (
                    code,
                    label,
                    monthly_price,
                    max_societes,
                    max_users,
                    max_documents
                )
                VALUES (
                    :code,
                    :label,
                    :price,
                    :societes,
                    :users,
                    :docs
                )
                ON CONFLICT (code)
                DO UPDATE SET
                    label = EXCLUDED.label,
                    monthly_price = EXCLUDED.monthly_price,
                    max_societes = EXCLUDED.max_societes,
                    max_users = EXCLUDED.max_users,
                    max_documents = EXCLUDED.max_documents
                """
            ),
            {
                "code": plan[0],
                "label": plan[1],
                "price": plan[2],
                "societes": plan[3],
                "users": plan[4],
                "docs": plan[5]
            }
        )

    conn.execute(
        text(
            """
            INSERT INTO subscriptions_v3 (
                cabinet_name,
                plan_code,
                status
            )
            SELECT
                'Cabinet Demo',
                'PRO',
                'trial'
            WHERE NOT EXISTS (
                SELECT 1
                FROM subscriptions_v3
            )
            """
        )
    )

print("Plans abonnements V3 OK")

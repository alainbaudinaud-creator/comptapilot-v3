from app import app

try:
    from controllers.premium_saas_routes import premium_saas

    already_registered = "premium_saas" in app.blueprints

    if not already_registered:
        app.register_blueprint(premium_saas)

    print("WSGI OK - premium_saas registered:", "premium_saas" in app.blueprints)

except Exception as e:
    print("WSGI premium_saas registration error:", e)

application = app

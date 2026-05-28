from flask import Flask
from app_refonte.routes.api_metier_demo import api_metier_demo

def create_test_app():
    app = Flask(__name__)
    app.register_blueprint(api_metier_demo)
    return app

if __name__ == "__main__":
    app = create_test_app()
    app.run(host="127.0.0.1", port=5099, debug=True)

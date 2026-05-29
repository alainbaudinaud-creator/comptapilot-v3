from flask import Flask, render_template, jsonify

from app_refonte.services.cockpit_reel_service import charger_cockpit_reel
from app_refonte.routes.api_metier_demo import api_metier_demo


def create_app_refonte():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        static_url_path="/refonte-static",
    )

    app.register_blueprint(api_metier_demo)

    @app.get("/")
    def cockpit():
        kpis, priorites = charger_cockpit_reel()
        return render_template(
            "cockpit_premium_dynamic.html",
            kpis=kpis,
            priorites=priorites,
        )

    @app.get("/pcg")
    def pcg():
        return render_template("pcg.html")

    @app.get("/immobilisations")
    def immobilisations():
        return render_template("immobilisations.html")

    @app.get("/emprunts")
    def emprunts():
        return render_template("emprunts.html")

    @app.get("/tva")
    def tva():
        return render_template("tva.html")

    @app.get("/fec")
    def fec():
        return render_template("fec.html")

    @app.get("/balance")
    def balance():
        return render_template("balance.html")

    @app.get("/grand-livre")
    def grand_livre():
        return render_template("grand_livre.html")

    @app.get("/journal")
    def journal():
        return render_template("journal.html")

    @app.get("/fec-export")
    def fec_export():
        return render_template("fec_export.html")

    @app.get("/compte-resultat")
    def compte_resultat():
        return render_template("compte_resultat.html")

    @app.get("/bilan")
    def bilan():
        return render_template("bilan.html")

    @app.get("/ocr")
    def ocr():
        return render_template("ocr.html")

    @app.get("/ocr-pdf")
    def ocr_pdf():
        return render_template("ocr_pdf.html")

    @app.get("/validation-ocr")
    def validation_ocr():
        return render_template("validation_ocr.html")

    @app.get("/health")
    def health():
        return jsonify({"success": True, "app": "ComptaPilot V3 Refonte", "status": "OK"})

    return app


if __name__ == "__main__":
    app = create_app_refonte()
    app.run(host="127.0.0.1", port=5099, debug=True)

# Instance WSGI pour Gunicorn
app = create_app_refonte()

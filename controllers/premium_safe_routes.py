import json
import urllib.parse
import urllib.request

from flask import Blueprint, render_template, request, redirect, jsonify, session
from sqlalchemy import text

from database import engine

bp_premium_safe = Blueprint("premium_safe", __name__)


@bp_premium_safe.route("/societe/ui")
def societe_ui_safe():
    return redirect("/cabinet/societes")


@bp_premium_safe.route("/cabinet/societes")
def societes_crud_premium():
    ensure_societes_clientes_table()

    search = request.args.get("search", "").strip()
    search_results = []

    if search:
        try:
            url = "https://recherche-entreprises.api.gouv.fr/search?" + urllib.parse.urlencode({
                "q": search,
                "per_page": 10,
            })
            req = urllib.request.Request(url, headers={"User-Agent": "ComptaPilot-V3"})
            with urllib.request.urlopen(req, timeout=12) as response:
                data = json.loads(response.read().decode("utf-8"))

            for item in data.get("results", []):
                siege = item.get("siege") or {}
                siren = item.get("siren") or ""
                tva = ""
                if siren.isdigit() and len(siren) == 9:
                    key = (12 + 3 * (int(siren) % 97)) % 97
                    tva = "FR" + str(key).zfill(2) + siren

                search_results.append({
                    "nom": item.get("nom_complet") or item.get("nom_raison_sociale") or "",
                    "siren": siren,
                    "siret": siege.get("siret") or "",
                    "tva_intracom": tva,
                    "adresse": siege.get("adresse") or "",
                    "code_postal": siege.get("code_postal") or "",
                    "ville": siege.get("libelle_commune") or siege.get("commune") or "",
                    "forme_juridique": item.get("nature_juridique") or item.get("forme_juridique") or "",
                    "activite_ape": item.get("activite_principale") or "",
                    "etat_administratif": item.get("etat_administratif") or "",
                })
        except Exception as e:
            search_results = []

    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT id, nom, siren, siret, tva_intracom, adresse, code_postal, ville,
                   forme_juridique, activite_ape, etat_administratif, email, statut, created_at
            FROM societes_clientes_premium
            ORDER BY id DESC
        """)).mappings().all()

    return render_template(
        "cabinet/societes_crud_premium.html",
        societes=rows,
        search=search,
        search_results=search_results
    )


def ensure_societes_clientes_table():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS societes_clientes_premium (
                id SERIAL PRIMARY KEY,
                nom TEXT NOT NULL,
                siren TEXT,
                siret TEXT,
                tva_intracom TEXT,
                adresse TEXT,
                code_postal TEXT,
                ville TEXT,
                forme_juridique TEXT,
                activite_ape TEXT,
                etat_administratif TEXT,
                email TEXT,
                statut TEXT DEFAULT 'ACTIF',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        for col in [
            "siret TEXT",
            "tva_intracom TEXT",
            "adresse TEXT",
            "code_postal TEXT",
            "forme_juridique TEXT",
            "activite_ape TEXT",
            "etat_administratif TEXT"
        ]:
            conn.execute(text(f"ALTER TABLE societes_clientes_premium ADD COLUMN IF NOT EXISTS {col}"))


@bp_premium_safe.route("/cabinet/societes/creer", methods=["POST"])
def societes_crud_creer():
    ensure_societes_clientes_table()

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO societes_clientes_premium
            (nom, siren, siret, tva_intracom, adresse, code_postal, ville, forme_juridique, activite_ape, etat_administratif, email, statut)
            VALUES
            (:nom, :siren, :siret, :tva_intracom, :adresse, :code_postal, :ville, :forme_juridique, :activite_ape, :etat_administratif, :email, 'ACTIF')
        """), {
            "nom": request.form.get("nom", "").strip(),
            "siren": request.form.get("siren", "").strip(),
            "siret": request.form.get("siret", "").strip(),
            "tva_intracom": request.form.get("tva_intracom", "").strip(),
            "adresse": request.form.get("adresse", "").strip(),
            "code_postal": request.form.get("code_postal", "").strip(),
            "ville": request.form.get("ville", "").strip(),
            "forme_juridique": request.form.get("forme_juridique", "").strip(),
            "activite_ape": request.form.get("activite_ape", "").strip(),
            "etat_administratif": request.form.get("etat_administratif", "").strip(),
            "email": request.form.get("email", "").strip(),
        })

    return redirect("/cabinet/societes")


@bp_premium_safe.route("/cabinet/societes/<int:societe_id>/archiver", methods=["POST"])
def societes_crud_archiver(societe_id):
    ensure_societes_clientes_table()
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE societes_clientes_premium
            SET statut = 'ARCHIVE'
            WHERE id = :id
        """), {"id": societe_id})
    return redirect("/cabinet/societes")


@bp_premium_safe.route("/cabinet/societes/<int:societe_id>/supprimer", methods=["POST"])
def societes_crud_supprimer(societe_id):
    ensure_societes_clientes_table()
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM societes_clientes_premium WHERE id = :id"), {"id": societe_id})
    return redirect("/cabinet/societes")


@bp_premium_safe.route("/cabinet/api/recherche-entreprise")
def api_recherche_entreprise_premium():
    q = request.args.get("q", "").strip()

    if not q:
        return jsonify({"success": False, "results": [], "error": "Recherche vide"})

    url = "https://recherche-entreprises.api.gouv.fr/search?" + urllib.parse.urlencode({
        "q": q,
        "per_page": 10,
    })

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ComptaPilot-V3"})
        with urllib.request.urlopen(req, timeout=12) as response:
            data = json.loads(response.read().decode("utf-8"))

        results = []
        for item in data.get("results", []):
            siege = item.get("siege") or {}
            results.append({
                "nom": item.get("nom_complet") or item.get("nom_raison_sociale") or "",
                "siren": item.get("siren") or "",
                "siret": siege.get("siret") or "",
                "ville": siege.get("libelle_commune") or siege.get("commune") or "",
                "code_postal": siege.get("code_postal") or "",
                "adresse": siege.get("adresse") or "",
                "activite": item.get("activite_principale") or "",
                "etat": item.get("etat_administratif") or "",
            })

        return jsonify({"success": True, "results": results})

    except Exception as e:
        return jsonify({"success": False, "results": [], "error": str(e)}), 500


@bp_premium_safe.route("/ecritures/saisie-rapide")
def saisie_rapide_safe():
    return render_template("cabinet/saisie_rapide_premium.html")


@bp_premium_safe.route("/v3/ecritures")
@bp_premium_safe.route("/v3/ecritures/")
@bp_premium_safe.route("/public/v3/ecritures")
def ecritures_v3_safe():
    return render_template("cabinet/saisie_rapide_premium.html")


@bp_premium_safe.route("/cabinet/ged")
def ged_premium_safe():
    return render_template("cabinet/ged_premium.html")


@bp_premium_safe.route("/cabinet/tva")
def tva_premium_safe():
    return render_template("cabinet/tva_premium.html")


@bp_premium_safe.route("/cabinet/fiscal")
def fiscal_premium_safe():
    return render_template("cabinet/fiscal_premium.html")


@bp_premium_safe.route("/cabinet/banques")
def banques_premium_safe():
    return render_template("cabinet/banques_premium.html")


@bp_premium_safe.route("/cabinet/immobilisations")
def immobilisations_premium_safe():
    return render_template("cabinet/immobilisations_premium.html")


@bp_premium_safe.route("/cabinet/utilisateurs")
def utilisateurs_premium_safe():
    return render_template("cabinet/utilisateurs_premium.html")


@bp_premium_safe.route("/cabinet/parametres")
def parametres_premium_safe():
    return render_template("cabinet/parametres_premium.html")


@bp_premium_safe.route("/cabinet/journal")
def journal_premium_safe():
    return render_template("cabinet/journal_premium.html")


@bp_premium_safe.route("/cabinet/grand-livre")
def grand_livre_premium_safe():
    return render_template("cabinet/grand_livre_premium.html")


@bp_premium_safe.route("/cabinet/balance")
def balance_premium_safe():
    return render_template("cabinet/balance_premium.html")


@bp_premium_safe.route("/cabinet/portail-client")
def portail_client_premium_safe():
    return render_template("cabinet/portail_client_premium.html")


@bp_premium_safe.route("/cabinet/societes/<int:societe_id>")
def societes_crud_fiche(societe_id):
    ensure_societes_clientes_table()
    with engine.begin() as conn:
        societe = conn.execute(text("""
            SELECT id, nom, siren, siret, tva_intracom, adresse, code_postal, ville,
                   forme_juridique, activite_ape, etat_administratif, email, statut, created_at
            FROM societes_clientes_premium
            WHERE id = :id
        """), {"id": societe_id}).mappings().first()

    if not societe:
        return redirect("/cabinet/societes")

    return render_template("cabinet/societe_fiche_premium.html", societe=societe)


@bp_premium_safe.route("/cabinet/societes/<int:societe_id>/modifier", methods=["POST"])
def societes_crud_modifier(societe_id):
    ensure_societes_clientes_table()
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE societes_clientes_premium
            SET nom = :nom,
                siren = :siren,
                siret = :siret,
                tva_intracom = :tva_intracom,
                adresse = :adresse,
                code_postal = :code_postal,
                ville = :ville,
                forme_juridique = :forme_juridique,
                activite_ape = :activite_ape,
                etat_administratif = :etat_administratif,
                email = :email,
                statut = :statut
            WHERE id = :id
        """), {
            "id": societe_id,
            "nom": request.form.get("nom", "").strip(),
            "siren": request.form.get("siren", "").strip(),
            "siret": request.form.get("siret", "").strip(),
            "tva_intracom": request.form.get("tva_intracom", "").strip(),
            "adresse": request.form.get("adresse", "").strip(),
            "code_postal": request.form.get("code_postal", "").strip(),
            "ville": request.form.get("ville", "").strip(),
            "forme_juridique": request.form.get("forme_juridique", "").strip(),
            "activite_ape": request.form.get("activite_ape", "").strip(),
            "etat_administratif": request.form.get("etat_administratif", "").strip(),
            "email": request.form.get("email", "").strip(),
            "statut": request.form.get("statut", "ACTIF").strip(),
        })

    return redirect(f"/cabinet/societes/{societe_id}")


@bp_premium_safe.route("/cabinet/societes/<int:societe_id>/selectionner", methods=["POST"])
def selectionner_societe_active(societe_id):
    ensure_societes_clientes_table()
    with engine.begin() as conn:
        societe = conn.execute(text("""
            SELECT id, nom, siren
            FROM societes_clientes_premium
            WHERE id = :id
        """), {"id": societe_id}).mappings().first()

    if societe:
        session["societe_active_id"] = societe["id"]
        session["societe_active_nom"] = societe["nom"]
        session["societe_active_siren"] = societe["siren"]

    return redirect("/erp-premium")

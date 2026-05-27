import json
import re
import requests
from flask import Flask, jsonify, request
from sqlalchemy import text
from database import engine

app = Flask(__name__)

def sanitize(name):
    name = re.sub(r"[^a-zA-Z0-9_]", "_", str(name).lower())
    name = re.sub(r"_+", "_", name).strip("_")
    return name or "module"

def table_name(module):
    return "dyn_" + sanitize(module)

def current_societe():
    return request.headers.get("X-Societe-ID") or request.args.get("societe") or "demo"

def ensure_societes(conn):
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dyn_societes (
            id SERIAL PRIMARY KEY,
            code VARCHAR(80) UNIQUE NOT NULL,
            nom VARCHAR(255) NOT NULL,
            data JSONB NOT NULL DEFAULT '{}'::jsonb,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
    conn.execute(text("""
        INSERT INTO dyn_societes (code, nom, data)
        VALUES
        ('demo', 'Société Démonstration', '{}'::jsonb),
        ('ifg', 'IFG Solution', '{}'::jsonb)
        ON CONFLICT (code) DO NOTHING
    """))

def ensure_users(conn):
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dyn_users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            nom VARCHAR(255),
            role VARCHAR(80) DEFAULT 'LECTURE',
            societe_code VARCHAR(80),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))

@app.route("/public-dynamic-health")
def health():
    return jsonify({"ok": True, "service": "dynamic_api", "users": True, "societes": True})

@app.route("/public-users", methods=["GET", "POST"])
def users():
    with engine.begin() as conn:
        ensure_users(conn)

        if request.method == "POST":
            payload = request.get_json(silent=True) or {}
            email = (payload.get("email") or "").strip().lower()
            if not email:
                return jsonify({"success": False, "error": "Email obligatoire"}), 400

            conn.execute(text("""
                INSERT INTO dyn_users (email, nom, role, societe_code)
                VALUES (:email, :nom, :role, :societe_code)
                ON CONFLICT (email)
                DO UPDATE SET nom = EXCLUDED.nom,
                              role = EXCLUDED.role,
                              societe_code = EXCLUDED.societe_code
            """), {
                "email": email,
                "nom": payload.get("nom"),
                "role": payload.get("role") or "LECTURE",
                "societe_code": payload.get("societe_code")
            })

            return jsonify({"success": True, "email": email})

        rows = conn.execute(text("""
            SELECT id, email, nom, role, societe_code, created_at
            FROM dyn_users
            ORDER BY id DESC
        """)).mappings().all()

        return jsonify({"rows": [
            {
                "id": r["id"],
                "email": r["email"],
                "nom": r["nom"],
                "role": r["role"],
                "societe_code": r["societe_code"],
                "created_at": r["created_at"].isoformat() if r["created_at"] else None
            }
            for r in rows
        ]})

@app.route("/public-dynamic-societes", methods=["GET", "POST"])
def societes():
    with engine.begin() as conn:
        ensure_societes(conn)

        if request.method == "POST":
            payload = request.get_json(silent=True) or {}
            code = sanitize(payload.get("code") or payload.get("siren") or payload.get("nom") or "")
            nom = payload.get("nom") or payload.get("raison_sociale") or code

            conn.execute(text("""
                INSERT INTO dyn_societes (code, nom, data)
                VALUES (:code, :nom, CAST(:data AS jsonb))
                ON CONFLICT (code)
                DO UPDATE SET nom = EXCLUDED.nom, data = EXCLUDED.data
            """), {
                "code": code,
                "nom": nom,
                "data": json.dumps(payload, ensure_ascii=False)
            })

            return jsonify({"success": True, "code": code, "nom": nom})

        rows = conn.execute(text("""
            SELECT code, nom, data, created_at
            FROM dyn_societes
            ORDER BY code
        """)).mappings().all()

        return jsonify({"rows": [
            {
                "code": r["code"],
                "nom": r["nom"],
                "data": r["data"] or {},
                "created_at": r["created_at"].isoformat() if r["created_at"] else None
            }
            for r in rows
        ]})

@app.route("/public-sirene/<query>")
def sirene_lookup(query):
    raw_query = str(query).strip()
    try:
        r = requests.get(f"https://recherche-entreprises.api.gouv.fr/search?q={raw_query}", timeout=15)
        data = r.json()
        results = data.get("results", [])
        if not results:
            return jsonify({"success": False, "error": "Entreprise introuvable"}), 404

        e = results[0]
        siege = e.get("siege") or {}
        siren = e.get("siren") or re.sub(r"[^0-9]", "", raw_query)

        tva = ""
        if siren and len(siren) == 9 and siren.isdigit():
            cle = (12 + 3 * (int(siren) % 97)) % 97
            tva = "FR" + str(cle).zfill(2) + siren

        dirigeants = e.get("dirigeants") or []
        dirigeant = dirigeants[0].get("nom_complet") if dirigeants else ""

        return jsonify({
            "success": True,
            "siren": siren,
            "siret": siege.get("siret"),
            "nom": e.get("nom_complet") or e.get("nom_raison_sociale"),
            "forme_juridique": e.get("nature_juridique") or e.get("forme_juridique"),
            "ape": e.get("activite_principale") or siege.get("activite_principale"),
            "tva": tva,
            "adresse": siege.get("adresse"),
            "code_postal": siege.get("code_postal"),
            "ville": siege.get("libelle_commune") or siege.get("commune"),
            "pays": "France",
            "dirigeant": dirigeant,
            "source": "recherche-entreprises.api.gouv.fr"
        })
    except Exception as ex:
        return jsonify({"success": False, "error": str(ex)}), 500

@app.route("/public-dynamic/<module>", methods=["GET", "POST"])
def collection(module):
    table = table_name(module)
    societe_id = current_societe()

    with engine.begin() as conn:
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id SERIAL PRIMARY KEY,
                societe_id VARCHAR(80) NOT NULL DEFAULT 'demo',
                data JSONB NOT NULL DEFAULT '{{}}'::jsonb,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        if request.method == "POST":
            payload = request.get_json(silent=True) or {}
            new_id = conn.execute(text(f"""
                INSERT INTO {table} (societe_id, data)
                VALUES (:societe_id, CAST(:data AS jsonb))
                RETURNING id
            """), {
                "societe_id": societe_id,
                "data": json.dumps(payload, ensure_ascii=False)
            }).scalar()
            return jsonify({"success": True, "id": new_id, "societe_id": societe_id})

        rows = conn.execute(text(f"""
            SELECT id, societe_id, data, created_at
            FROM {table}
            WHERE societe_id = :societe_id
            ORDER BY id DESC
            LIMIT 500
        """), {"societe_id": societe_id}).mappings().all()

        return jsonify({"rows": [
            {
                **dict(r["data"] or {}),
                "id": r["id"],
                "societe_id": r["societe_id"],
                "created_at": r["created_at"].isoformat() if r["created_at"] else None
            }
            for r in rows
        ], "societe_id": societe_id})

@app.route("/public-dynamic/<module>/<int:item_id>", methods=["DELETE"])
def delete(module, item_id):
    table = table_name(module)
    societe_id = current_societe()

    with engine.begin() as conn:
        conn.execute(text(f"DELETE FROM {table} WHERE id = :id AND societe_id = :societe_id"), {
            "id": item_id,
            "societe_id": societe_id
        })

    return jsonify({"success": True, "societe_id": societe_id})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)

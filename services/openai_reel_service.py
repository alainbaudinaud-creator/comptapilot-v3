import os
import json
from datetime import datetime
from sqlalchemy import text
from database import engine


def initialiser_openai_reel():

    with engine.begin() as conn:

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS openai_reel_v3 (
                id SERIAL PRIMARY KEY,
                type_analyse VARCHAR(100),
                modele VARCHAR(100),
                prompt TEXT,
                resultat TEXT,
                statut VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))


def analyser_facture_openai(texte_facture):

    initialiser_openai_reel()

    api_key = os.getenv("OPENAI_API_KEY", "")
    modele = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    prompt = f"""
Analyse cette facture et retourne une structure comptable JSON :
{texte_facture}
"""

    if not api_key:
        resultat = {
            "mode": "FALLBACK_SANS_CLE",
            "fournisseur": "FOURNISSEUR DEMO OPENAI",
            "numero_facture": "OPENAI-" + datetime.utcnow().strftime("%Y%m%d%H%M%S"),
            "date_facture": datetime.utcnow().date().isoformat(),
            "montant_ht": 1000.00,
            "montant_tva": 200.00,
            "montant_ttc": 1200.00,
            "compte_charge": "606100",
            "compte_tva": "445660",
            "compte_tiers": "401000",
            "score_ia": 94,
            "statut": "ANALYSE_SIMULEE_SECURISÉE"
        }

        statut = "FALLBACK"

    else:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model=modele,
                messages=[
                    {
                        "role": "system",
                        "content": "Tu es un assistant expert-comptable français. Retourne uniquement un JSON comptable exploitable."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1
            )

            content = response.choices[0].message.content

            try:
                resultat = json.loads(content)
            except Exception:
                resultat = {
                    "raw": content,
                    "warning": "Réponse non JSON parsée"
                }

            statut = "SUCCESS"

        except Exception as e:
            resultat = {
                "mode": "ERREUR_OPENAI",
                "error": str(e),
                "fallback": {
                    "fournisseur": "FOURNISSEUR FALLBACK",
                    "montant_ht": 1000.00,
                    "montant_tva": 200.00,
                    "montant_ttc": 1200.00
                }
            }

            statut = "ERROR_FALLBACK"

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO openai_reel_v3
            (type_analyse, modele, prompt, resultat, statut)
            VALUES
            (:type_analyse, :modele, :prompt, :resultat, :statut)
        """), {
            "type_analyse": "ANALYSE_FACTURE",
            "modele": modele,
            "prompt": prompt,
            "resultat": json.dumps(resultat, ensure_ascii=False),
            "statut": statut,
        })

    return resultat


def dashboard_openai_reel():

    initialiser_openai_reel()

    with engine.connect() as conn:
        total = conn.execute(text("""
            SELECT COUNT(*) FROM openai_reel_v3
        """)).scalar() or 0

        rows = conn.execute(text("""
            SELECT id, type_analyse, modele, statut, created_at
            FROM openai_reel_v3
            ORDER BY id DESC
            LIMIT 10
        """)).mappings().all()

    return {
        "total": total,
        "enabled": bool(os.getenv("OPENAI_API_KEY", "")),
        "model": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        "history": [dict(row) for row in rows],
    }


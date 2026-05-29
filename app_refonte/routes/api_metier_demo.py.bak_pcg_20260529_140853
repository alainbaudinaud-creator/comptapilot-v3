from flask import Blueprint, jsonify, request

from app_refonte.services.immobilisations_service import amortissement_lineaire
from app_refonte.services.emprunts_service import tableau_amortissement_emprunt
from app_refonte.services.tva_service import calcul_tva
from app_refonte.services.fec_service import controle_colonnes_fec, REQUIRED_FEC_COLUMNS

api_metier_demo = Blueprint("api_metier_demo", __name__)

@api_metier_demo.get("/api/refonte/health")
def health():
    return jsonify({
        "success": True,
        "module": "ComptaPilot V3 Refonte",
        "status": "OK"
    })

@api_metier_demo.post("/api/refonte/immobilisation/amortissement")
def api_amortissement():
    data = request.get_json(silent=True) or {}
    lignes = amortissement_lineaire(
        data.get("valeur_origine", 0),
        data.get("duree_mois", 0)
    )
    return jsonify({"success": True, "lignes": lignes})

@api_metier_demo.post("/api/refonte/emprunt/tableau")
def api_emprunt():
    data = request.get_json(silent=True) or {}
    lignes = tableau_amortissement_emprunt(
        data.get("montant", 0),
        data.get("taux_annuel", 0),
        data.get("duree_mois", 0)
    )
    return jsonify({"success": True, "lignes": lignes})

@api_metier_demo.post("/api/refonte/tva/calcul")
def api_tva():
    data = request.get_json(silent=True) or {}
    resultat = calcul_tva(
        data.get("tva_collectee", 0),
        data.get("tva_deductible", 0)
    )
    return jsonify({"success": True, "resultat": resultat})

@api_metier_demo.get("/api/refonte/fec/controle-demo")
def api_fec_demo():
    resultat = controle_colonnes_fec(REQUIRED_FEC_COLUMNS)
    return jsonify({"success": True, "resultat": resultat})

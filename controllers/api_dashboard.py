from flask import Blueprint, render_template

api_dashboard_routes = Blueprint('api_dashboard', __name__)


@api_dashboard_routes.route('/api-dashboard')
def api_dashboard():
    routes_api = [
        {
            "nom": "Health check",
            "methode": "GET",
            "url": "/api/v1/health",
            "securisee": "Non",
            "description": "Vérifie que l'API fonctionne."
        },
        {
            "nom": "Logs audit",
            "methode": "GET",
            "url": "/api/v1/audit/logs",
            "securisee": "Oui",
            "description": "Retourne les 50 derniers logs d'audit."
        },
        {
            "nom": "Écritures bancaires",
            "methode": "GET",
            "url": "/api/v1/bancaire/ecritures",
            "securisee": "Oui",
            "description": "Retourne les écritures bancaires."
        },
        {
            "nom": "Tâches actives V7",
            "methode": "GET",
            "url": "/api/v1/v7/taches-actives",
            "securisee": "Oui",
            "description": "Retourne les tâches actives du scheduler V7."
        },
        {
            "nom": "Récupérer une tâche V7",
            "methode": "GET",
            "url": "/api/v1/v7/taches/<id>",
            "securisee": "Oui",
            "description": "Retourne une tâche V7 précise depuis SQLite."
        },
        {
            "nom": "Créer une tâche V7",
            "methode": "POST",
            "url": "/api/v1/v7/taches",
            "securisee": "Oui",
            "description": "Crée une nouvelle tâche V7."
        },
        {
            "nom": "Modifier une tâche V7",
            "methode": "PUT",
            "url": "/api/v1/v7/taches/<id>",
            "securisee": "Oui",
            "description": "Modifie une tâche V7 existante."
        },
        {
            "nom": "Supprimer une tâche V7",
            "methode": "DELETE",
            "url": "/api/v1/v7/taches/<id>",
            "securisee": "Oui",
            "description": "Supprime une tâche V7."
        },
                {
            "nom": "Login JWT",
            "methode": "POST",
            "url": "/api/v1/auth/login",
            "securisee": "Non",
            "description": "Authentifie un utilisateur et retourne un token JWT."
        },
        {
            "nom": "Créer utilisateur",
            "methode": "POST",
            "url": "/api/v1/auth/users",
            "securisee": "Oui ADMIN",
            "description": "Crée un utilisateur avec rôle."
        },
        {
            "nom": "Lister utilisateurs",
            "methode": "GET",
            "url": "/api/v1/auth/users",
            "securisee": "Oui ADMIN",
            "description": "Liste les utilisateurs."
        },
        {
            "nom": "Désactiver utilisateur",
            "methode": "PUT",
            "url": "/api/v1/auth/users/<id>/disable",
            "securisee": "Oui ADMIN",
            "description": "Désactive un utilisateur."
        },
        {
            "nom": "Modifier rôle utilisateur",
            "methode": "PUT",
            "url": "/api/v1/auth/users/<id>/role",
            "securisee": "Oui ADMIN",
            "description": "Modifie le rôle d'un utilisateur."
        },
        {
            "nom": "Modifier mot de passe",
            "methode": "PUT",
            "url": "/api/v1/auth/users/<id>/password",
            "securisee": "Oui ADMIN",
            "description": "Réinitialise le mot de passe d'un utilisateur."
        },
        {
            "nom": "Supprimer utilisateur",
            "methode": "DELETE",
            "url": "/api/v1/auth/users/<id>",
            "securisee": "Oui ADMIN",
            "description": "Supprime un utilisateur."
        }
    ]

    return render_template(
        'api_dashboard.html',
        routes_api=routes_api
    )


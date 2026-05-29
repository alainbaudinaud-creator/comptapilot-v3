# Session de reprise ComptaPilot V3

Date : Fri May 29 01:09:29 UTC 2026

## Serveur actif
IP : 57.130.60.80
URL : http://57.130.60.80

## Etat validé
- Nginx fonctionne
- Docker fonctionne
- Gunicorn répond
- Le 502 est supprimé
- docker-compose.yml est revenu sur : gunicorn app:app
- / répond par 302 vers /login
- app_refonte existe sur le serveur mais pas dans l'image Docker actuelle

## Dernier point fonctionnel
Commande active :
gunicorn -w 2 -b 0.0.0.0:5000 app:app

Test validé :
curl -I http://127.0.0.1:5001/
Retour :
HTTP/1.1 302 FOUND
Location: /login

## Problème ouvert
La vraie interface V3 moderne semble être dans :
/home/ubuntu/apps/comptapilot-v3/app_refonte

Mais elle n'est pas présente dans le conteneur Docker actuel :
/app/app_refonte absent

## Prochaine étape recommandée
Avant toute nouvelle bascule :
1. Inspecter Dockerfile
2. Comprendre pourquoi app_refonte n'est pas copiée dans l'image
3. Créer une sauvegarde avant modification
4. Rebuild contrôlé uniquement après validation

## Règle de travail
Ne plus modifier docker-compose.yml, app.py ou Dockerfile sans :
1. Sauvegarde complète
2. Note dans ce fichier
3. Test de retour arrière connu

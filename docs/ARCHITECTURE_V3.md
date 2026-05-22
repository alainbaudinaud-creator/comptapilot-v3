# Architecture officielle ComptaPilot V3

## Statut
ComptaPilot V3 est désormais stabilisé autour d’un noyau Flask + PostgreSQL + Docker.

## Point d’entrée actif
- app.py

## Environnement actif
- Docker
- Gunicorn
- PostgreSQL
- Port applicatif local : 5001
- Port PostgreSQL local : 5433

## Modules actifs principaux
- controllers
- services
- templates
- static
- models
- utils

## Modules archivés
Tous les prototypes, anciennes bases SQLite, dumps SQL, anciennes versions et scripts de réparation sont déplacés dans :
- archive/

## Règle de travail
Ne plus créer de fichiers *_OK, *_STABLE, *_BACKUP à la racine ou dans controllers/services.
Toute sauvegarde doit aller dans archive/ ou être gérée par Git.

## Objectif V3
Passer du mode prototype au mode produit industrialisé.

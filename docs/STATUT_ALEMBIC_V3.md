# Statut Alembic ComptaPilot V3

## Statut actuel

Alembic est préparé mais non activé en production.

## Fichiers présents

- alembic.ini
- alembic/env.py
- alembic/README.md
- alembic/versions/

## Quality check

Le quality check V3 vérifie la présence de la configuration Alembic.

Pour le moment, la validation Alembic est non bloquante car la dépendance alembic n'est pas encore installée dans l'image Docker.

## Règle

Ne pas appliquer de migration automatiquement.

Toute migration devra être :
1. générée,
2. relue,
3. testée localement,
4. validée par quality_check_v3.ps1,
5. commitée séparément.

## Prochaine étape

Installer Alembic dans requirements.txt uniquement quand la migration PostgreSQL réelle sera prête.

# Alembic / migrations ComptaPilot V3

Préparation future des migrations PostgreSQL.

## Objectif

Versionner proprement les évolutions de base de données :

- tables PDP V3
- tables SaaS
- multi-tenant
- audit
- supervision
- production

## Règle

Ne pas activer Alembic brutalement.
Ne pas modifier la base actuelle sans migration contrôlée.

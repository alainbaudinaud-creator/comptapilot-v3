# Migration PostgreSQL PDP V3

## Objectif

Préparer la migration progressive du module PDP V3 vers PostgreSQL / SQLAlchemy.

## État actuel

Le module PDP V3 utilise actuellement :

- routes Flask
- services métier
- repositories
- models dataclasses
- db_core SQLite legacy

## Cible

À terme :

routes
-> services
-> repositories
-> models SQLAlchemy
-> PostgreSQL

## Règles

- Ne pas casser le legacy SQLite.
- Ne pas supprimer les anciennes tables.
- Ne pas migrer en big bang.
- Introduire PostgreSQL progressivement.
- Garder les tests automatiques verts.

## Étapes prévues

1. Créer les modèles SQLAlchemy PDP V3.
2. Créer les tables PostgreSQL PDP V3.
3. Ajouter un repository PostgreSQL expérimental.
4. Comparer SQLite legacy et PostgreSQL.
5. Basculer lecture seule.
6. Basculer écriture.
7. Déprécier progressivement SQLite PDP.

## Tables cibles

- pdp_v3_workflows
- pdp_v3_archives
- pdp_v3_journal_technique

# Models PDP V3

Ce dossier prépare la future couche de modèles métier PDP V3.

## Objectif

Préparer la transition progressive depuis SQLite brut vers une architecture propre :

- modèles métier,
- SQLAlchemy,
- PostgreSQL,
- migrations futures,
- API SaaS stable.

## Modèles prévus

- WorkflowPDP
- ArchiveProbatoire
- JournalTechniquePDP

## Règle

Ne pas migrer brutalement les données.
Le socle actuel reste compatible legacy pendant la transition.

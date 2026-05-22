# PDP V3

Architecture cible du module PDP / e-invoicing / archivage probatoire.

## Sous-modules prévus

- workflow
- depot
- reception
- supervision
- api
- archivage
- journal_technique

## Objectif

Extraire progressivement les fonctionnalités PDP du monolithe gestion_ecritures.py sans casser le socle historique.

## Stratégie

- migration progressive,
- compatibilité legacy,
- commits courts,
- tests systématiques,
- fallback anti-crash.

## Tables identifiées

- workflow_factures_pdp
- workflow_factures_pdp_v2
- archives_probatoires
- archives_probatoires_v2
- journal_technique_pdp_v2

## APIs identifiées

- /api/e-invoicing/*
- /api-v2/e-invoicing/*

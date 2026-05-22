# Plan de refactorisation ComptaPilot V3

## Diagnostic
Le fichier controllers/gestion_ecritures.py contient 327 routes.
Il est devenu un méga-controller regroupant trop de domaines métier.

## Objectif
Découper progressivement ce fichier sans casser l’application.

## Découpage cible

### controllers/comptabilite
- écritures
- journaux
- balance
- grand livre
- bilan
- compte de résultat
- TVA

### controllers/ged
- documents
- pièces jointes
- coffre-fort
- archivage probatoire

### controllers/ocr
- OCR facture
- analyse document
- extraction automatique

### controllers/ia
- assistant IA
- analyse financière IA
- anomalies
- prévisions
- robots

### controllers/bancaire
- import bancaire
- rapprochement
- banque IA

### controllers/fiscalite
- FEC
- liasse fiscale
- CA3
- télétransmission

### controllers/workflow
- validation
- kanban
- correction
- multi-niveaux

### controllers/saas
- abonnements
- tenants
- limites usage
- sécurité SaaS

### controllers/monitoring
- supervision
- santé système
- logs
- scheduler

## Règle
Ne pas déplacer toutes les routes d’un coup.
Découper par petits blocs testés après chaque extraction.

# Architecture technique ComptaPilot V3

## État actuel

ComptaPilot V3 dispose maintenant d'un socle premium stable et d'une architecture métier progressivement industrialisée.

## Socle validé

Les routes suivantes sont validées automatiquement :

- /
- /ged
- /ocr
- /supervision
- /production
- /pdp-v3
- /pdp-v3/workflow
- /pdp-v3/supervision
- /api/pdp-v3/workflows
- /balance
- /grand-livre
- /bilan
- /compte-resultat

## Architecture cible appliquée à PDP V3

Le module PDP V3 suit désormais la chaîne :

routes
-> services
-> repositories
-> models
-> db_core

## Rôles des couches

### controllers/pdp_v3
Expose les routes web et API.

### services/pdp_v3
Contient la logique métier.

### repositories/pdp_v3
Contient l'accès aux données.

### models/pdp_v3
Décrit les objets métier.

### db_core
Centralise les connexions techniques sans entrer en conflit avec database.py.

## Règle importante

Le fichier database.py historique reste préservé car plusieurs modules existants l'utilisent encore.

La nouvelle couche technique s'appelle db_core pour éviter tout conflit d'import Python.

## Stratégie

- Migration progressive
- Aucun big bang
- Compatibilité legacy maintenue
- Tests automatiques après chaque étape
- Commits courts
- Design premium homogène

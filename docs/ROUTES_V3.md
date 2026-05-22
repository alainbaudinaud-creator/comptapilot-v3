# Routes officielles ComptaPilot V3

## Routes principales

- / : accueil
- /auth : authentification
- /societe : sociétés
- /plan-comptable : plan comptable
- /ecritures : écritures comptables et modules associés
- /exportations : exports
- /api/v1 : API principale
- /mentions-legales : mentions légales
- /politique-confidentialite : politique de confidentialité

## Attention architecture

Le préfixe /ecritures regroupe actuellement trop de modules :
- écritures
- audit
- signatures
- sauvegardes
- transmission
- bancaire
- dashboard
- IA

Objectif futur :
séparer progressivement ces domaines en routes dédiées.

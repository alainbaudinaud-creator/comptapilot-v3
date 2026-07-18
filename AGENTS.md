# AGENTS.md — ComptaPilot V3

## Mission

Tu travailles sur ComptaPilot V3, un ERP destiné aux cabinets d’expertise comptable.

La priorité absolue est de faire évoluer le projet sans casser les fonctionnalités déjà validées.

## Langue et réponses

- Répondre en français.
- Aller directement au diagnostic, au code ou au script demandé.
- Fournir des commandes directement copiables.
- Éviter les longues introductions.
- Ne jamais annoncer qu’une étape est validée si les tests ont échoué.

## Environnement

Répertoire principal :

`/home/ubuntu/apps/comptapilot-v3`

Branche Git habituelle :

`refonte-propre-saas-v3`

## Règles absolues

Ne jamais :

- casser une route existante ;
- supprimer une fonctionnalité validée ;
- inventer une table, une colonne, une route ou une fonction ;
- utiliser `git reset --hard` ;
- utiliser `git push --force` ;
- supprimer un volume Docker ;
- supprimer une base PostgreSQL ;
- exposer un mot de passe, un jeton ou une clé API ;
- annoncer un succès sans test ;
- écraser des modifications utilisateur sans rapport avec la tâche.

## Méthode obligatoire

Avant toute modification :

1. Lire les fichiers concernés.
2. Rechercher les dépendances.
3. Vérifier les structures SQL.
4. Vérifier les routes et services existants.
5. Limiter le patch au strict nécessaire.

Après toute modification :

1. Vérifier la syntaxe.
2. Vérifier les imports.
3. Exécuter les tests ciblés.
4. Tester les routes concernées.
5. Contrôler les logs.
6. Exécuter `git diff --check`.
7. Exécuter `git status --short`.

## Git

Interdictions :

- `git reset --hard`
- `git push --force`

Avant modification :

- `git status --short`
- `git branch --show-current`

Après modification :

- `git diff --check`
- `git diff --stat`
- `git status --short`

## PostgreSQL

Ne jamais supposer qu’une colonne existe.

Toujours vérifier le schéma réel avant d’écrire une nouvelle requête.

Distinguer soigneusement :

- `client_id`
- `societe_id`
- `exercice_id`

## Docker

Privilégier :

- `docker ps`
- `docker logs`
- `docker inspect`
- `docker exec`
- les redémarrages ciblés

Ne jamais supprimer une base, un volume ou un conteneur de production sans autorisation explicite.

## Comptabilité

Toujours préserver :

- l’équilibre débit/crédit ;
- la traçabilité ;
- le journal ;
- la date ;
- la pièce ;
- le libellé ;
- le statut ;
- l’exercice ;
- le client.

## Révision et fiscalité

Un dossier comportant un bloquant réel ne peut pas être déclaré signable.

Avant toute télétransmission, vérifier :

- le client ;
- l’exercice ;
- le régime fiscal ;
- le statut signable ;
- le visa ;
- le verrouillage réel ;
- l’absence de bloquant.

## Dossier annuel

BM IMMOBILIER est un dossier pilote, pas une exception permanente.

Toute fonctionnalité validée sur BM doit être industrialisable pour les autres clients.

## Source de vérité

Ordre de priorité :

1. Schéma PostgreSQL réel.
2. Code réellement exécuté.
3. Tests.
4. Configuration Docker.
5. Documentation.
6. Hypothèses historiques.


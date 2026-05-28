# Manifeste de reprise rapide

## Commandes de reprise
```bash
cd ~/apps/comptapilot-v3
git checkout refonte-propre-saas-v3
git status
docker compose up -d
docker compose ps
curl -k -I https://127.0.0.1/login

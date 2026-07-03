#!/usr/bin/env bash
set -e

echo "=== GIT ==="
git status --short

echo "=== DOCKER ==="
docker compose ps

echo "=== LOGIN ==="
curl -k -I https://127.0.0.1/login | head -20

echo "=== ROOT ==="
curl -k -I https://127.0.0.1/ | head -20

#!/bin/bash
cd ~/apps/comptapilot-v3 || exit 1

DATE=$(date +%Y%m%d_%H%M%S)
DEST="backups/comptapilot_backup_$DATE"

mkdir -p "$DEST"

cp -a app.py "$DEST/" 2>/dev/null || true
cp -a app_production.py "$DEST/" 2>/dev/null || true
cp -a templates "$DEST/" 2>/dev/null || true
cp -a static "$DEST/" 2>/dev/null || true
cp -a docker-compose.yml "$DEST/" 2>/dev/null || true
cp -a Dockerfile "$DEST/" 2>/dev/null || true

tar -czf "$DEST.tar.gz" "$DEST"
rm -rf "$DEST"

echo "Sauvegarde créée : $DEST.tar.gz"

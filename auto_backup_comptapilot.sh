#!/bin/bash

cd ~/apps/comptapilot-v3 || exit 1

DATE=$(date +%Y%m%d_%H%M%S)

DEST="backups/full_backup_$DATE"

mkdir -p "$DEST"

echo "=== BACKUP APPLICATION ==="

cp -a templates "$DEST/" 2>/dev/null || true
cp -a static "$DEST/" 2>/dev/null || true
cp -a controllers "$DEST/" 2>/dev/null || true
cp -a app.py "$DEST/" 2>/dev/null || true
cp -a app_production.py "$DEST/" 2>/dev/null || true
cp -a database.py "$DEST/" 2>/dev/null || true
cp -a docker-compose.yml "$DEST/" 2>/dev/null || true
cp -a Dockerfile "$DEST/" 2>/dev/null || true

echo "=== BACKUP POSTGRESQL ==="

docker compose exec -T postgres pg_dump -U comptapilot comptapilot > "$DEST/postgres_dump.sql"

echo "=== COMPRESSION ==="

tar -czf "$DEST.tar.gz" "$DEST"

rm -rf "$DEST"

echo "=== ROTATION BACKUPS > 15 JOURS ==="

find backups -name "*.tar.gz" -type f -mtime +15 -delete

echo "=== BACKUP TERMINE ==="
echo "$DEST.tar.gz"


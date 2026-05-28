#!/bin/bash

cd ~/apps/comptapilot-v3 || exit 1

DATE=$(date "+%Y-%m-%d %H:%M:%S")

echo "=== GIT AUTO SAVE ==="

git add .

git commit -m "Auto backup ComptaPilot $DATE" || true

git push origin main || true

echo "=== PUSH TERMINE ==="


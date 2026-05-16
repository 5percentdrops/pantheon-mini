#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ORG="SoftwareHouse"

INSTALL_ROOT="${SOFTWAREHOUSE_INSTALL_ROOT:-$HOME/softwarehouse}"
PAPERCLIP_IMPORT_DIR="${PAPERCLIP_IMPORT_DIR:-$HOME/paperclip/imports/$ORG}"
HERMES_SEED_DIR="${HERMES_SEED_DIR:-$HOME/hermes/seed_skills/$ORG}"
OPENCLAW_SEED_DIR="${OPENCLAW_SEED_DIR:-$HOME/openclaw/seed_skills/$ORG}"

echo "== $ORG installer =="
python3 "$ROOT/scripts/validate.py"

mkdir -p "$INSTALL_ROOT" "$PAPERCLIP_IMPORT_DIR" "$HERMES_SEED_DIR" "$OPENCLAW_SEED_DIR"

cp "$ROOT/$ORG/paperclip/organization.import.json" "$PAPERCLIP_IMPORT_DIR/"
cp "$ROOT/$ORG/paperclip/agents.json" "$PAPERCLIP_IMPORT_DIR/"
cp "$ROOT/$ORG/paperclip/agents.csv" "$PAPERCLIP_IMPORT_DIR/"
cp "$ROOT/$ORG/routes/routes.json" "$PAPERCLIP_IMPORT_DIR/"

cp -R "$ROOT/$ORG/skills/hermes_seed/"* "$HERMES_SEED_DIR/" 2>/dev/null || true
cp -R "$ROOT/$ORG/skills/openclaw_seed/"* "$OPENCLAW_SEED_DIR/" 2>/dev/null || true

cp -R "$ROOT/$ORG" "$INSTALL_ROOT/"
cp -R "$ROOT/shared" "$INSTALL_ROOT/shared" 2>/dev/null || true

echo "$ORG STAGED SUCCESSFULLY."

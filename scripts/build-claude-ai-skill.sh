#!/usr/bin/env bash
# Zip the seeder skill for upload to claude.ai (Settings > Capabilities > Skills).
# Output: dist/cxone-onboarding-seeder.zip
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_DIR="$ROOT/plugins/cx-se-onboarding-checklist/skills"
mkdir -p "$ROOT/dist"
rm -f "$ROOT/dist/cxone-onboarding-seeder.zip"
( cd "$SKILL_DIR" && zip -qr "$ROOT/dist/cxone-onboarding-seeder.zip" cxone-onboarding-seeder -x '*.DS_Store' )
echo "wrote dist/cxone-onboarding-seeder.zip"
unzip -l "$ROOT/dist/cxone-onboarding-seeder.zip"

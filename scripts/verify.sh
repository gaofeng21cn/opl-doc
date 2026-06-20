#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

python3 -m pytest -q
python3 scripts/opl_doc_doctor.py doctor . --format json >/tmp/opl-doc-doctor.json
python3 scripts/opl_doc_doctor.py family-plan --format markdown >/tmp/opl-doc-family-plan.md
python3 scripts/opl_doc_doctor.py native-check . >/tmp/opl-doc-native-check.json
git diff --check

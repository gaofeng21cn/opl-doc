#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

python3 -m pytest -q
python3 scripts/opl_doc_doctor.py doctor . --format json >/tmp/opl-doc-governance-doctor.json
python3 scripts/opl_doc_doctor.py family-plan --format markdown >/tmp/opl-doc-governance-family-plan.md
python3 scripts/opl_doc_doctor.py init-repo /tmp/opl-doc-governance-init-smoke --dry-run --format json >/tmp/opl-doc-governance-init-repo.json
git diff --check

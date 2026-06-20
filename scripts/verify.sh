#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

temp_root="${OPL_DOC_REPO_TEMP_ROOT:-${TMPDIR:-/tmp}/opl-doc-repo-temp-${USER:-user}}"
mkdir -p "$temp_root/python-pycache" "$temp_root/pytest-cache"

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="$temp_root/python-pycache"
export PYTEST_ADDOPTS="${PYTEST_ADDOPTS:-} -o cache_dir=$temp_root/pytest-cache"

python3 -m pytest -q
python3 scripts/opl_doc_doctor.py doctor . --format json >/tmp/opl-doc-doctor.json
python3 scripts/opl_doc_doctor.py family-plan --format markdown >/tmp/opl-doc-family-plan.md
python3 scripts/opl_doc_doctor.py native-check . >/tmp/opl-doc-native-check.json
git diff --check

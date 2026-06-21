#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

temp_root="${OPL_DOC_REPO_TEMP_ROOT:-${TMPDIR:-/tmp}/opl-doc-repo-temp-${USER:-user}}"
mkdir -p "$temp_root/python-pycache" "$temp_root/pytest-cache"

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="$temp_root/python-pycache"
export PYTEST_ADDOPTS="${PYTEST_ADDOPTS:-} -o cache_dir=$temp_root/pytest-cache"

lane="${1:-all}"

run_support_profile_strict() {
  python3 scripts/opl_doc_doctor.py support-profile-check . --format json >/tmp/opl-doc-support-profile-check.json
}

case "$lane" in
  all|default)
    python3 -m pytest -q
    python3 scripts/opl_doc_doctor.py doctor . --format json >/tmp/opl-doc-doctor.json
    python3 scripts/opl_doc_doctor.py family-plan --format markdown >/tmp/opl-doc-family-plan.md
    run_support_profile_strict
    python3 scripts/opl_doc_doctor.py native-check . >/tmp/opl-doc-native-check.json
    git diff --check
    ;;
  support-profile|support-profile-strict|support-profile:strict)
    run_support_profile_strict
    git diff --check
    ;;
  *)
    echo "Unknown lane: $lane" >&2
    echo "Usage: scripts/verify.sh [all|default|support-profile|support-profile-strict|support-profile:strict]" >&2
    exit 1
    ;;
esac

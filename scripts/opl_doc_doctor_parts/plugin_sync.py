"""Plugin-native profile drift checks and sync rendering."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .common import read_text
from .constants import NATIVE_PROFILE_REL_PATH, OPL_DOC_AUTHORITY_BOUNDARY
from .invariant_checks import doctor
from .profile_discovery import repo_identity


def _profile_doc_role(path: str) -> str:
    roles = {
        "README.md": "root_entry",
        "AGENTS.md": "repo_agent_working_rules",
        "TASTE.md": "maintenance_preferences",
        "docs/README.md": "docs_entry",
        "docs/project.md": "project_positioning",
        "docs/status.md": "current_status",
        "docs/architecture.md": "architecture_boundary",
        "docs/invariants.md": "hard_constraints",
        "docs/decisions.md": "active_decision_record",
    }
    return roles.get(path, "canonical_doc")


def _owned_by_repo(active_truth_owner: str | None) -> list[str]:
    owned = ["contracts/**", "src/**", "tests/**", "docs/status.md"]
    if active_truth_owner:
        owned.append(active_truth_owner)
    return owned


def expected_native_profile(root: Path, current: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = doctor(root)
    surfaces = payload["repo_native_surfaces"]
    active_truth_owner = next(iter(payload["active_truth_health"]["owner_docs"]), None)
    canonical_docs = [
        {"path": path, "role": _profile_doc_role(path)}
        for path in surfaces["canonical_docs"]["present"]
    ]
    taxonomy_dirs = [
        path
        for path, exists in payload["canonical_dirs"].items()
        if exists
    ]
    repo_profile = payload["repo_profile"]
    managed_by_plugins = dict((current or {}).get("managed_by_plugins") or {})
    managed_by_plugins["opl-doc"] = {
        "management": "profile_check_and_sync",
        "managed_surfaces": [NATIVE_PROFILE_REL_PATH],
        "authority_boundary": OPL_DOC_AUTHORITY_BOUNDARY,
        "does_not_own": [
            "repo_truth",
            "domain_truth",
            "runtime_truth",
            "artifact_authority",
            "owner_receipts",
            "quality_verdicts",
            "production_readiness",
        ],
    }
    return {
        "schema": "opl_native_profile.v1",
        "repo_id": repo_identity(root),
        "repo_profile": repo_profile,
        "flow_profile": repo_profile,
        "doc_profile": repo_profile,
        "active_truth_owner": active_truth_owner,
        "canonical_docs": canonical_docs,
        "taxonomy_dirs": taxonomy_dirs,
        "machine_truth_surfaces": surfaces["machine_truth"],
        "verification_commands": surfaces["verification"],
        "owned_by_repo": _owned_by_repo(active_truth_owner),
        "managed_by_plugins": managed_by_plugins,
        "plugin_native_status": "profile_declared",
    }


def _native_profile_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _load_native_profile(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.exists():
        return None, None
    try:
        payload = json.loads(read_text(path))
    except json.JSONDecodeError as exc:
        return None, f"{NATIVE_PROFILE_REL_PATH} is not valid JSON: {exc}"
    if not isinstance(payload, dict):
        return None, f"{NATIVE_PROFILE_REL_PATH} must contain a JSON object"
    return payload, None


def native_check(root: Path) -> dict[str, Any]:
    root = root.resolve()
    profile_path = root / NATIVE_PROFILE_REL_PATH
    current, load_error = _load_native_profile(profile_path)
    expected = expected_native_profile(root, current)
    missing = [] if profile_path.exists() else [NATIVE_PROFILE_REL_PATH]
    errors = [load_error] if load_error else []
    drift: list[str] = []
    if current is not None:
        for key, expected_value in expected.items():
            if current.get(key) != expected_value:
                drift.append(key)
    ok = not missing and not errors and not drift
    return {
        "ok": ok,
        "mode": "native-check",
        "apply": False,
        "repo_root": str(root),
        "profile_path": str(profile_path),
        "missing": missing,
        "errors": errors,
        "drift": drift,
        "expected_profile": expected,
    }


def native_sync(root: Path, apply: bool = False) -> dict[str, Any]:
    root = root.resolve()
    profile_path = root / NATIVE_PROFILE_REL_PATH
    current, _load_error = _load_native_profile(profile_path)
    expected = expected_native_profile(root, current)
    expected_text = _native_profile_text(expected)
    current_text = read_text(profile_path) if profile_path.exists() else None
    planned_changes = []
    if current_text != expected_text:
        planned_changes.append(
            {
                "path": NATIVE_PROFILE_REL_PATH,
                "action": "create" if current_text is None else "update",
            }
        )
    if apply and planned_changes:
        profile_path.parent.mkdir(parents=True, exist_ok=True)
        profile_path.write_text(expected_text, encoding="utf-8")
    check = native_check(root)
    return {
        **check,
        "mode": "native-sync",
        "apply": apply,
        "applied": bool(apply and planned_changes),
        "planned_changes": planned_changes,
    }

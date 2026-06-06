"""Repository identity and native surface discovery."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import package_json_name, package_json_scripts, pyproject_name, rel_exists
from .constants import (
    AGENT_GUIDANCE_DOCS,
    MACHINE_TRUTH_SURFACES,
    PACKAGE_SCRIPT_VERIFICATION_ORDER,
)


def repo_identity(root: Path) -> str:
    package_name = package_json_name(root)
    if package_name == "opl-framework-shared":
        return "one-person-lab"
    if package_name == "redcube-ai-mono":
        return "redcube-ai"
    return package_name or pyproject_name(root) or root.name


def detect_profile(root: Path) -> str:
    name = repo_identity(root)
    if name == "one-person-lab":
        return "opl_framework"
    if name == "one-person-lab-app":
        return "opl_app"
    if name in {"med-autoscience", "med-autogrant", "redcube-ai"}:
        return "foundry_agent"
    if name == "opl-meta-agent":
        return "opl_meta_agent"
    if rel_exists(root, ".codex-plugin/plugin.json") or rel_exists(root, "skills"):
        return "codex_plugin"
    if rel_exists(root, "pyproject.toml") or rel_exists(root, "package.json"):
        return "tooling_repo"
    return "generic_repo"


def inspect_repo_native_surfaces(root: Path, core_status: dict[str, bool]) -> dict[str, Any]:
    package_scripts = package_json_scripts(root)
    verification = []
    if rel_exists(root, "scripts/verify.sh"):
        verification.append("scripts/verify.sh")
    for script_name in PACKAGE_SCRIPT_VERIFICATION_ORDER:
        if script_name in package_scripts:
            verification.append(f"package.json:scripts.{script_name}")
    if rel_exists(root, "pyproject.toml") and rel_exists(root, "tests"):
        verification.append("python -m pytest")

    return {
        "agent_guidance": [
            path for path in AGENT_GUIDANCE_DOCS if rel_exists(root, path)
        ],
        "canonical_docs": {
            "present": [path for path, exists in core_status.items() if exists],
            "missing": [path for path, exists in core_status.items() if not exists],
        },
        "machine_truth": [
            path for path in MACHINE_TRUTH_SURFACES if rel_exists(root, path)
        ],
        "verification": verification,
    }

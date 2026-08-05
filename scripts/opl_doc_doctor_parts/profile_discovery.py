"""Repository identity and native surface discovery."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from .common import package_json_name, package_json_scripts, pyproject_name, rel_exists
from .constants import (
    AGENT_GUIDANCE_DOCS,
    MACHINE_TRUTH_SURFACES,
    PACKAGE_SCRIPT_VERIFICATION_ORDER,
)


def _git_common_repo_root(root: Path) -> Path | None:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "--git-common-dir"],
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        return None
    common_dir = Path(result.stdout.strip())
    if not common_dir.is_absolute():
        common_dir = (root / common_dir).resolve()
    if common_dir.name != ".git":
        return None
    return common_dir.parent


def _machine_truth_surface_exists(root: Path, rel_path: str, *, git_repo: bool) -> bool:
    path = root / rel_path
    if path.is_file():
        return True
    if not path.is_dir() or not git_repo:
        return path.is_dir()
    return any(candidate.is_file() or candidate.is_symlink() for candidate in path.rglob("*"))


def repo_identity(root: Path) -> str:
    package_name = package_json_name(root)
    if package_name in {"opl-framework", "opl-framework-shared"}:
        return "one-person-lab"
    if package_name == "redcube-ai-mono":
        return "redcube-ai"
    canonical_root = _git_common_repo_root(root)
    return package_name or pyproject_name(root) or (canonical_root or root).name


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
    git_repo = _git_common_repo_root(root) is not None
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
            path
            for path in MACHINE_TRUTH_SURFACES
            if _machine_truth_surface_exists(root, path, git_repo=git_repo)
        ],
        "verification": verification,
    }

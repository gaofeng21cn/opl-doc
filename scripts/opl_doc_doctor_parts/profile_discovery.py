"""Repository identity and native surface discovery."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from .common import package_json_name, package_json_scripts, pyproject_name
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


def _tracked_paths(root: Path, rel_path: str) -> list[Path] | None:
    if _git_common_repo_root(root) is None:
        return None
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--", rel_path],
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    if result.returncode != 0:
        return []
    return [root / path for path in result.stdout.splitlines() if path]


def repo_surface_exists(root: Path, rel_path: str) -> bool:
    tracked = _tracked_paths(root, rel_path)
    if tracked is None:
        return (root / rel_path).exists()
    return any(path.exists() or path.is_symlink() for path in tracked)


def tracked_markdown_docs(root: Path) -> list[Path]:
    tracked = _tracked_paths(root, "docs")
    if tracked is None:
        docs_root = root / "docs"
        if not docs_root.exists():
            return []
        return sorted(path for path in docs_root.rglob("*.md") if path.is_file())
    return sorted(
        path for path in tracked if path.suffix == ".md" and path.is_file()
    )


def repo_identity(root: Path) -> str:
    package_name = (
        package_json_name(root) if repo_surface_exists(root, "package.json") else None
    )
    if package_name in {"opl-framework", "opl-framework-shared"}:
        return "one-person-lab"
    if package_name == "redcube-ai-mono":
        return "redcube-ai"
    canonical_root = _git_common_repo_root(root)
    project_name = (
        pyproject_name(root) if repo_surface_exists(root, "pyproject.toml") else None
    )
    return package_name or project_name or (canonical_root or root).name


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
    if repo_surface_exists(root, ".codex-plugin/plugin.json") or repo_surface_exists(
        root, "skills"
    ):
        return "codex_plugin"
    if repo_surface_exists(root, "pyproject.toml") or repo_surface_exists(
        root, "package.json"
    ):
        return "tooling_repo"
    return "generic_repo"


def inspect_repo_native_surfaces(root: Path, core_status: dict[str, bool]) -> dict[str, Any]:
    package_scripts = (
        package_json_scripts(root) if repo_surface_exists(root, "package.json") else {}
    )
    verification = []
    if repo_surface_exists(root, "scripts/verify.sh"):
        verification.append("scripts/verify.sh")
    for script_name in PACKAGE_SCRIPT_VERIFICATION_ORDER:
        if script_name in package_scripts:
            verification.append(f"package.json:scripts.{script_name}")
    if repo_surface_exists(root, "pyproject.toml") and repo_surface_exists(
        root, "tests"
    ):
        verification.append("python -m pytest")

    return {
        "agent_guidance": [
            path for path in AGENT_GUIDANCE_DOCS if repo_surface_exists(root, path)
        ],
        "canonical_docs": {
            "present": [path for path, exists in core_status.items() if exists],
            "missing": [path for path, exists in core_status.items() if not exists],
        },
        "machine_truth": [
            path
            for path in MACHINE_TRUTH_SURFACES
            if repo_surface_exists(root, path)
        ],
        "verification": verification,
    }

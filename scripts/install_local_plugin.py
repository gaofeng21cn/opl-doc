#!/usr/bin/env python3
"""Install this repository as a local Codex plugin by copying it to ~/plugins."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


PLUGIN_NAME = "opl-doc-governance"
COMMAND_NAME = "opl-doc-doctor"
REQUIRED_PLUGIN_FILES = (
    ".codex-plugin/plugin.json",
    "skills/opl-doc-governance/SKILL.md",
    "skills/opl-doc-governance/agents/openai.yaml",
    "skills/opl-doc/SKILL.md",
    "skills/opl-doc/agents/openai.yaml",
    "scripts/opl_doc_doctor.py",
)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def install(
    repo_root: Path,
    plugins_dir: Path,
    marketplace_path: Path,
    bin_dir: Path,
) -> dict[str, str]:
    target = plugins_dir / PLUGIN_NAME
    if target.exists():
        shutil.rmtree(target)
    ignore = shutil.ignore_patterns(".git", ".worktrees", ".pytest_cache", "__pycache__")
    shutil.copytree(repo_root, target, ignore=ignore)

    marketplace = load_json(marketplace_path)
    marketplace.setdefault("name", "personal")
    marketplace.setdefault("interface", {"displayName": "Personal"})
    plugins = marketplace.setdefault("plugins", [])
    if not isinstance(plugins, list):
        raise ValueError("marketplace plugins must be a list")

    entry = {
        "name": PLUGIN_NAME,
        "source": {"source": "local", "path": f"./plugins/{PLUGIN_NAME}"},
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": "Developer Tools",
    }
    plugins[:] = [item for item in plugins if not (isinstance(item, dict) and item.get("name") == PLUGIN_NAME)]
    plugins.append(entry)
    write_json(marketplace_path, marketplace)

    bin_dir.mkdir(parents=True, exist_ok=True)
    command_path = bin_dir / COMMAND_NAME
    if command_path.exists() or command_path.is_symlink():
        command_path.unlink()
    command_path.symlink_to(target / "scripts" / "opl_doc_doctor.py")

    return {
        "plugin_path": str(target),
        "marketplace_path": str(marketplace_path),
        "command_path": str(command_path),
    }


def verify(
    plugins_dir: Path,
    marketplace_path: Path,
    bin_dir: Path,
) -> dict[str, Any]:
    plugin_path = plugins_dir / PLUGIN_NAME
    missing = [
        str(plugin_path / rel)
        for rel in REQUIRED_PLUGIN_FILES
        if not (plugin_path / rel).exists()
    ]
    marketplace = load_json(marketplace_path)
    plugins = marketplace.get("plugins", [])
    marketplace_ok = any(
        isinstance(item, dict)
        and item.get("name") == PLUGIN_NAME
        and item.get("source", {}).get("path") == f"./plugins/{PLUGIN_NAME}"
        for item in plugins
    )
    command_path = bin_dir / COMMAND_NAME
    command_ok = command_path.is_symlink() and command_path.resolve() == plugin_path / "scripts" / "opl_doc_doctor.py"
    ok = not missing and marketplace_ok and command_ok
    return {
        "ok": ok,
        "plugin_path": str(plugin_path),
        "marketplace_ok": marketplace_ok,
        "command_path": str(command_path),
        "command_ok": command_ok,
        "missing": missing,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install OPL Doc Governance as a local Codex plugin")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--plugins-dir", default=str(Path.home() / "plugins"))
    parser.add_argument(
        "--marketplace-path",
        default=str(Path.home() / ".agents" / "plugins" / "marketplace.json"),
    )
    parser.add_argument(
        "--bin-dir",
        default=str(Path.home() / ".local" / "bin"),
        help="User-level directory for the opl-doc-doctor command symlink.",
    )
    parser.add_argument("--verify-only", action="store_true", help="Only verify an existing local install.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plugins_dir = Path(args.plugins_dir).expanduser().resolve()
    marketplace_path = Path(args.marketplace_path).expanduser().resolve()
    bin_dir = Path(args.bin_dir).expanduser().resolve()
    if args.verify_only:
        result = verify(plugins_dir, marketplace_path, bin_dir)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["ok"] else 1

    result = install(
        Path(args.repo_root).resolve(),
        plugins_dir,
        marketplace_path,
        bin_dir,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

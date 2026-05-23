#!/usr/bin/env python3
"""Install this repository as a local Codex plugin by copying it to ~/plugins."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


PLUGIN_NAME = "opl-doc-governance"


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


def install(repo_root: Path, plugins_dir: Path, marketplace_path: Path) -> dict[str, str]:
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

    return {
        "plugin_path": str(target),
        "marketplace_path": str(marketplace_path),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install OPL Doc Governance as a local Codex plugin")
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--plugins-dir", default=str(Path.home() / "plugins"))
    parser.add_argument(
        "--marketplace-path",
        default=str(Path.home() / ".agents" / "plugins" / "marketplace.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = install(
        Path(args.repo_root).resolve(),
        Path(args.plugins_dir).expanduser().resolve(),
        Path(args.marketplace_path).expanduser().resolve(),
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


"""Small shared helpers for doctor modules."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    message: str
    action: str

    def to_json(self) -> dict[str, str]:
        return {
            "severity": self.severity,
            "code": self.code,
            "path": self.path,
            "message": self.message,
            "action": self.action,
        }


def rel_exists(root: Path, rel_path: str) -> bool:
    return (root / rel_path).exists()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="ignore")


def package_json_scripts(root: Path) -> dict[str, str]:
    package_json = root / "package.json"
    if not package_json.exists():
        return {}
    try:
        payload = json.loads(read_text(package_json))
    except json.JSONDecodeError:
        return {}
    scripts = payload.get("scripts")
    return scripts if isinstance(scripts, dict) else {}


def package_json_name(root: Path) -> str | None:
    package_json = root / "package.json"
    if not package_json.exists():
        return None
    try:
        payload = json.loads(read_text(package_json))
    except json.JSONDecodeError:
        return None
    name = payload.get("name")
    return name if isinstance(name, str) and name else None


def pyproject_name(root: Path) -> str | None:
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return None
    for line in read_text(pyproject).splitlines():
        match = re.match(r'\s*name\s*=\s*["\']([^"\']+)["\']', line)
        if match:
            return match.group(1)
    return None

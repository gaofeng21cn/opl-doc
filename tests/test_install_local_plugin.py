from __future__ import annotations

from pathlib import Path

import yaml

from scripts.install_local_plugin import install, verify

RETIRED_SKILL_NAME = "opl-doc-governance"
RETIRED_NAME_ALLOWED_PATHS = {
    Path("docs/history/opl-doc-governance-tombstone.md"),
    Path("docs/history/opl-doc-governance-installer-cleanup-tail-retirement.md"),
    Path("tests/test_install_local_plugin.py"),
}


def _tracked_text_files() -> list[Path]:
    roots = [
        Path(".codex-plugin"),
        Path("skills"),
        Path("scripts"),
        Path("templates"),
        Path("docs"),
        Path("tests"),
        Path("README.md"),
        Path("README.zh-CN.md"),
    ]
    files: list[Path] = []
    for root in roots:
        if root.is_file():
            files.append(root)
        elif root.exists():
            files.extend(
                path
                for path in root.rglob("*")
                if path.is_file()
                and "__pycache__" not in path.parts
                and ".pytest_cache" not in path.parts
                and path.suffix != ".pyc"
            )
    return sorted(files)


def test_install_copies_plugin_and_updates_marketplace(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".codex-plugin").mkdir()
    (repo / ".codex-plugin" / "plugin.json").write_text('{"name":"opl-doc"}\n')
    (repo / "skills").mkdir()
    (repo / "skills" / "dummy.txt").write_text("ok\n")
    (repo / ".git").mkdir()
    (repo / ".git" / "ignored").write_text("ignored\n")

    result = install(
        repo,
        tmp_path / "plugins",
        tmp_path / "marketplace.json",
        tmp_path / "bin",
    )

    plugin_path = Path(result["plugin_path"])
    command_path = Path(result["command_path"])
    assert (plugin_path / ".codex-plugin" / "plugin.json").exists()
    assert not (plugin_path / ".git").exists()
    assert command_path.name == "opl-doc-doctor"
    assert command_path.is_symlink()
    assert command_path.resolve() == plugin_path / "scripts" / "opl_doc_doctor.py"
    marketplace = (tmp_path / "marketplace.json").read_text()
    assert "opl-doc" in marketplace
    assert "Developer Tools" in marketplace


def test_short_opl_doc_skill_metadata_exists() -> None:
    skill = Path("skills/opl-doc/SKILL.md").read_text(encoding="utf-8")
    metadata = Path("skills/opl-doc/agents/openai.yaml").read_text(encoding="utf-8")
    prompt = yaml.safe_load(metadata)["interface"]["default_prompt"]

    assert 'name: "opl-doc"' in skill
    assert "# OPL Doc" in skill
    assert 'display_name: "OPL Doc"' in metadata
    assert "$opl-doc" in prompt
    assert "skills/opl-doc/SKILL.md" in prompt
    assert "/Users/gaofeng" not in prompt
    assert "allow_implicit_invocation: true" in metadata


def test_retired_governance_skill_is_not_an_active_surface() -> None:
    assert not Path("skills/opl-doc-governance/SKILL.md").exists()
    assert not Path("skills/opl-doc-governance/agents/openai.yaml").exists()
    assert Path("docs/history/opl-doc-governance-tombstone.md").exists()


def test_retired_governance_name_only_appears_in_tombstone_or_negative_guards() -> None:
    active_hits = [
        path
        for path in _tracked_text_files()
        if path not in RETIRED_NAME_ALLOWED_PATHS
        and RETIRED_SKILL_NAME in path.read_text(encoding="utf-8", errors="ignore")
    ]

    assert active_hits == []


def test_verify_only_checks_installed_short_skill_and_command(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    plugins_dir = tmp_path / "plugins"
    marketplace_path = tmp_path / "marketplace.json"
    bin_dir = tmp_path / "bin"

    install(repo_root, plugins_dir, marketplace_path, bin_dir)
    result = verify(plugins_dir, marketplace_path, bin_dir)

    assert result["ok"] is True
    assert result["marketplace_ok"] is True
    assert result["command_ok"] is True
    assert result["missing"] == []

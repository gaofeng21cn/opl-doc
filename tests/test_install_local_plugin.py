from __future__ import annotations

from pathlib import Path

import yaml

from scripts.install_local_plugin import install, verify


def test_install_copies_plugin_and_updates_marketplace(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".codex-plugin").mkdir()
    (repo / ".codex-plugin" / "plugin.json").write_text('{"name":"opl-doc-governance"}\n')
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
    assert "opl-doc-governance" in marketplace
    assert "Developer Tools" in marketplace


def test_skill_ui_metadata_supports_direct_invocation() -> None:
    metadata = Path("skills/opl-doc-governance/agents/openai.yaml").read_text(encoding="utf-8")
    prompt = yaml.safe_load(metadata)["interface"]["default_prompt"]

    assert 'display_name: "OPL Doc Governance"' in metadata
    assert "$opl-doc-governance" in metadata
    assert "/Users/gaofeng/workspace/opl-doc-governance/skills/opl-doc-governance/SKILL.md" in prompt
    assert "six-repo default" in prompt
    assert "12 primary reference documents" in prompt
    assert "do not mark the global goal complete" in prompt
    assert "do not treat that as the skill being unavailable" in prompt
    assert "/goal" in metadata
    assert "allow_implicit_invocation: true" in metadata


def test_short_opl_doc_skill_metadata_exists() -> None:
    skill = Path("skills/opl-doc/SKILL.md").read_text(encoding="utf-8")
    metadata = Path("skills/opl-doc/agents/openai.yaml").read_text(encoding="utf-8")
    prompt = yaml.safe_load(metadata)["interface"]["default_prompt"]

    assert 'name: "opl-doc"' in skill
    assert "short skill name for OPL Doc Governance" in skill
    assert 'display_name: "OPL Doc"' in metadata
    assert "$opl-doc" in prompt
    assert "opl-doc-governance" in prompt
    assert "allow_implicit_invocation: true" in metadata


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

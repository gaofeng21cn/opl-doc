from __future__ import annotations

from pathlib import Path

from scripts.install_local_plugin import install


def test_install_copies_plugin_and_updates_marketplace(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / ".codex-plugin").mkdir()
    (repo / ".codex-plugin" / "plugin.json").write_text('{"name":"opl-doc-governance"}\n')
    (repo / "skills").mkdir()
    (repo / "skills" / "dummy.txt").write_text("ok\n")
    (repo / ".git").mkdir()
    (repo / ".git" / "ignored").write_text("ignored\n")

    result = install(repo, tmp_path / "plugins", tmp_path / "marketplace.json")

    plugin_path = Path(result["plugin_path"])
    assert (plugin_path / ".codex-plugin" / "plugin.json").exists()
    assert not (plugin_path / ".git").exists()
    marketplace = (tmp_path / "marketplace.json").read_text()
    assert "opl-doc-governance" in marketplace
    assert "Developer Tools" in marketplace


def test_skill_ui_metadata_supports_direct_invocation() -> None:
    metadata = Path("skills/opl-doc-governance/agents/openai.yaml").read_text(encoding="utf-8")

    assert 'display_name: "OPL Doc Governance"' in metadata
    assert "$opl-doc-governance" in metadata
    assert "/goal" in metadata
    assert "allow_implicit_invocation: true" in metadata

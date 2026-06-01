from pathlib import Path

import pytest

from scripts.scanner import scan_repo


@pytest.fixture
def fake_repo(tmp_path: Path) -> Path:
    """Build a fake repo layout."""
    (tmp_path / "README.md").write_text("# My Project\n")
    (tmp_path / "package.json").write_text('{"name": "my-proj"}')
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "index.md").write_text("# Docs")
    (tmp_path / ".well-known").mkdir()
    return tmp_path


def test_scan_finds_readme(fake_repo):
    assets = scan_repo(fake_repo)
    assert assets.readme == fake_repo / "README.md"


def test_scan_detects_node_project(fake_repo):
    assets = scan_repo(fake_repo)
    assert assets.project_type == "node"


def test_scan_finds_docs_dir(fake_repo):
    assets = scan_repo(fake_repo)
    assert any(p.name == "index.md" for p in assets.docs_files)


def test_scan_detects_well_known_dir(fake_repo):
    assets = scan_repo(fake_repo)
    assert assets.has_well_known_dir is True


def test_scan_detects_missing_llms_txt(fake_repo):
    assets = scan_repo(fake_repo)
    assert assets.has_llms_txt is False


def test_scan_handles_empty_repo(tmp_path):
    assets = scan_repo(tmp_path)
    assert assets.readme is None
    assert assets.project_type == "unknown"
    assert assets.docs_files == []

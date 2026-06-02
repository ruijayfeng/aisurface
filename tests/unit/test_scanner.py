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


def test_scan_detects_nextjs_not_node(tmp_path):
    """A project with both package.json and next.config.js should be 'nextjs', not 'node'."""
    (tmp_path / "package.json").write_text("{}")
    (tmp_path / "next.config.js").write_text("module.exports = {}")
    assets = scan_repo(tmp_path)
    assert assets.project_type == "nextjs"


def test_scan_detects_vite_not_node(tmp_path):
    """A project with both package.json and vite.config.ts should be 'vite', not 'node'."""
    (tmp_path / "package.json").write_text("{}")
    (tmp_path / "vite.config.ts").write_text("export default {}")
    assets = scan_repo(tmp_path)
    assert assets.project_type == "vite"


def test_scan_ignores_schema_files_in_node_modules(tmp_path):
    """Schema files inside node_modules should not trigger has_schema_org=True."""
    (tmp_path / "package.json").write_text("{}")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "vendor.schema.json").write_text("{}")
    assets = scan_repo(tmp_path)
    assert assets.has_schema_org is False
    assert assets.schema_files == []


def test_iter_relevant_files_prunes_ignored_dirs(tmp_path):
    """Verify os.walk receives pruned dirs list, not just post-filter."""
    import os

    from scripts.scanner import _iter_relevant_files

    # Create a deep node_modules tree
    (tmp_path / "node_modules" / "vendor" / "deeply" / "nested").mkdir(parents=True)
    (tmp_path / "node_modules" / "vendor" / "deeply" / "nested" / "schema.json").write_text("{}")
    (tmp_path / "real.json").write_text("{}")

    # Collect visited dirpaths by monkey-patching os.walk
    visited = []
    original_walk = os.walk
    def tracking_walk(top, **kwargs):
        for dirpath, dirs, files in original_walk(top, **kwargs):
            visited.append(dirpath)
            yield dirpath, dirs, files
    os.walk = tracking_walk
    try:
        results = list(_iter_relevant_files(tmp_path, "*.json"))
    finally:
        os.walk = original_walk

    # Result correctness
    assert len(results) == 1
    assert results[0].name == "real.json"

    # Pruning correctness: os.walk should never have been called with
    # a dirpath inside node_modules
    for dirpath in visited:
        assert "node_modules" not in Path(dirpath).parts, f"Walked into ignored dir: {dirpath}"


def test_structural_finding_imports():
    """StructuralFinding should be importable from scripts.findings."""
    from scripts.findings import StructuralFinding
    from scripts.report import CheckResult

    assert issubclass(StructuralFinding, CheckResult)


def test_structural_checks_return_structural_finding():
    """Checks #5 and #6 (file-based structural) should return StructuralFinding with file_path."""
    from scripts.cli import run_audit
    from scripts.findings import StructuralFinding

    fixture_root = Path(__file__).resolve().parents[2] / "evals" / "fixtures" / "good-schema-nextjs-docs"
    report = run_audit(fixture_root)

    structural_with_paths = [r for r in report.results if isinstance(r, StructuralFinding)]
    assert len(structural_with_paths) == 2, f"Expected 2 StructuralFinding results, got {len(structural_with_paths)}"

    for r in structural_with_paths:
        assert r.file_path is not None
        assert r.file_path.endswith((".json", ".txt"))


def test_semantic_checks_do_not_return_structural_finding():
    """Non-file-based checks should NOT return StructuralFinding."""
    from scripts.cli import run_audit
    from scripts.findings import StructuralFinding

    fixture_root = Path(__file__).resolve().parents[2] / "evals" / "fixtures" / "good-schema-nextjs-docs"
    report = run_audit(fixture_root)

    non_structural = [r for r in report.results if not isinstance(r, StructuralFinding)]
    assert len(non_structural) == 10, f"Expected 10 non-StructuralFinding results, got {len(non_structural)}"

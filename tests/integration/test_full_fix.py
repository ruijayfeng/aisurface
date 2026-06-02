"""End-to-end: audit a bad fixture, run fix --dry-run, verify all 4 patches generated."""
import subprocess
import sys
from pathlib import Path

import pytest

EVAL_FIXTURES = Path(__file__).resolve().parents[2] / "evals" / "fixtures"


@pytest.mark.eval
def test_dry_run_generates_4_patches_for_bad_fixture(tmp_path: Path):
    """Copy bad fixture to tmp_path (so dry-run touches nothing real), then fix --dry-run."""
    import shutil
    src = EVAL_FIXTURES / "bad-readme-python-lib"
    fixture = tmp_path / "project"
    shutil.copytree(src, fixture)

    result = subprocess.run(
        [sys.executable, "-m", "scripts.cli", "fix", str(fixture), "--dry-run"],
        capture_output=True, text=True, encoding="utf-8",
    )
    assert result.returncode == 0, result.stderr
    out = result.stdout
    assert "faq" in out.lower()
    assert "when_to_use" in out.lower() or "when to use" in out.lower()
    assert "llms.txt" in out.lower()
    assert "schema" in out.lower()


@pytest.mark.eval
def test_apply_with_yes_writes_files_and_lifts_score(tmp_path: Path):
    """Apply patches non-interactively, then re-audit. Score must increase."""
    import json
    import shutil
    src = EVAL_FIXTURES / "bad-readme-python-lib"
    fixture = tmp_path / "project"
    shutil.copytree(src, fixture)

    # Baseline audit score
    baseline = subprocess.run(
        [sys.executable, "-m", "scripts.cli", "audit", str(fixture), "--json"],
        capture_output=True, text=True, encoding="utf-8",
    )
    baseline_score = json.loads(baseline.stdout).get("health_score", 0)

    # Apply fix
    fix_result = subprocess.run(
        [sys.executable, "-m", "scripts.cli", "fix", str(fixture), "--yes"],
        capture_output=True, text=True, encoding="utf-8",
    )
    assert fix_result.returncode == 0, fix_result.stderr

    # Verify files exist
    assert (fixture / ".well-known" / "llms.txt").exists()
    assert (fixture / "index.schema.json").exists()
    readme = (fixture / "README.md").read_text(encoding="utf-8")
    assert "## FAQ" in readme
    assert "## When to use" in readme

    # Re-audit, expect higher score
    after = subprocess.run(
        [sys.executable, "-m", "scripts.cli", "audit", str(fixture), "--json"],
        capture_output=True, text=True, encoding="utf-8",
    )
    after_score = json.loads(after.stdout).get("health_score", 0)
    assert after_score > baseline_score, f"Score did not improve: {baseline_score} → {after_score}"


@pytest.mark.eval
def test_only_filter_limits_patches(tmp_path: Path):
    import shutil
    src = EVAL_FIXTURES / "bad-readme-python-lib"
    fixture = tmp_path / "project"
    shutil.copytree(src, fixture)

    result = subprocess.run(
        [sys.executable, "-m", "scripts.cli", "fix", str(fixture), "--dry-run", "--only", "faq"],
        capture_output=True, text=True, encoding="utf-8",
    )
    assert result.returncode == 0
    out = result.stdout.lower()
    assert "faq" in out
    assert "llms.txt" not in out
    assert "schema" not in out


EXPECTED_PATCHES = Path(__file__).resolve().parents[2] / "evals" / "expected_patches"


@pytest.mark.eval
def test_patches_match_snapshot(tmp_path: Path):
    """Snapshot test: each patch generator's output must match recorded fixtures."""
    import shutil
    src = EVAL_FIXTURES / "bad-readme-python-lib"
    fixture = tmp_path / "project"
    shutil.copytree(src, fixture)

    from scripts.fix.llms_txt import generate_llms_txt_patch
    from scripts.fix.schema_org import generate_schema_org_patch

    expected_dir = EXPECTED_PATCHES / "bad-readme-python-lib"

    llms_patch = generate_llms_txt_patch(fixture)
    assert llms_patch.new_content == (expected_dir / "llms_txt.txt").read_text(encoding="utf-8")

    schema_patch = generate_schema_org_patch(fixture)
    assert schema_patch.new_content == (expected_dir / "schema_org.json").read_text(encoding="utf-8")

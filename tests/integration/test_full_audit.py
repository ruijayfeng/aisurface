"""End-to-end test: run audit on every eval fixture and verify the report is sensible."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

EVAL_FIXTURES = Path(__file__).resolve().parents[2] / "evals" / "fixtures"
EXPECTED_DIR = Path(__file__).resolve().parents[2] / "evals" / "expected"


@pytest.mark.eval
@pytest.mark.parametrize("fixture_name", [
    "bad-readme-python-lib",
    "good-schema-nextjs-docs",
    "minimal-cli-tool",
])
def test_audit_runs_on_fixture(fixture_name, tmp_path):
    """Run aisurface CLI on a fixture and verify it produces a valid JSON report."""
    fixture_path = EVAL_FIXTURES / fixture_name
    result = subprocess.run(
        [sys.executable, "-m", "scripts.cli", str(fixture_path), "--json"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    report = json.loads(result.stdout)
    assert report["project_name"] == fixture_name
    assert len(report["results"]) == 12  # 12-check audit


@pytest.mark.eval
def test_audit_fails_gracefully_on_minimal():
    """The minimal-cli-tool fixture should not crash on missing files."""
    fixture_path = EVAL_FIXTURES / "minimal-cli-tool"
    result = subprocess.run(
        [sys.executable, "-m", "scripts.cli", str(fixture_path)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert "Health score" in result.stdout


@pytest.mark.eval
def test_bad_readme_scores_lower_than_good():
    """The bad fixture should score strictly lower than the good one."""
    def _score(fixture_name: str) -> int:
        result = subprocess.run(
            [sys.executable, "-m", "scripts.cli",
             str(EVAL_FIXTURES / fixture_name), "--json"],
            capture_output=True, text=True,
        )
        report = json.loads(result.stdout)
        total = sum(r["score"] for r in report["results"])
        return total

    bad = _score("bad-readme-python-lib")
    good = _score("good-schema-nextjs-docs")
    assert good > bad, f"Good ({good}) should score higher than bad ({bad})"

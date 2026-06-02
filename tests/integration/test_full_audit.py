"""End-to-end test: run audit on every eval fixture and verify the report is sensible."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

EVAL_FIXTURES = Path(__file__).resolve().parents[2] / "evals" / "fixtures"
EXPECTED_DIR = Path(__file__).resolve().parents[2] / "evals" / "expected"


def _run_audit_json(fixture_path: Path) -> dict:
    """Run the CLI on `fixture_path` with --json and return the parsed report."""
    result = subprocess.run(
        [sys.executable, "-m", "scripts.cli", str(fixture_path), "--json"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    return json.loads(result.stdout)


@pytest.mark.eval
@pytest.mark.parametrize("fixture_name", [
    "bad-readme-python-lib",
    "good-schema-nextjs-docs",
    "minimal-cli-tool",
    "perfect-readme-and-docs",
])
def test_audit_matches_expected(fixture_name):
    """Run aisurface CLI on a fixture and compare to its expected JSON.

    The audit is fully deterministic on a fixed fixture (no random sources, no
    network calls), so we can deep-compare the full report. If this ever
    stops being the case, the test should be reduced to comparing the
    deterministic keys only: project_name, id, name, category, passed,
    impact, max_score.
    """
    fixture_path = EVAL_FIXTURES / fixture_name
    expected_path = EXPECTED_DIR / f"{fixture_name}.json"
    assert expected_path.exists(), f"Missing expected JSON: {expected_path}"

    actual = _run_audit_json(fixture_path)
    expected = json.loads(expected_path.read_text(encoding="utf-8"))

    # Top-level shape: project_name, results, skipped, errors.
    assert actual["project_name"] == expected["project_name"]
    assert len(actual["results"]) == len(expected["results"]) == 12

    # Compare every result row by id (the order can drift if results are
    # re-shuffled; ids are stable).
    actual_by_id = {r["id"]: r for r in actual["results"]}
    expected_by_id = {r["id"]: r for r in expected["results"]}
    assert set(actual_by_id) == set(expected_by_id)
    for cid, exp in expected_by_id.items():
        act = actual_by_id[cid]
        # Deterministic keys must match exactly. score is also deterministic
        # in v0.1 (offline_critique + content heuristics, no random/network).
        for key in ("id", "name", "score", "max_score", "passed", "impact"):
            assert act[key] == exp[key], (
                f"check #{cid} key '{key}' differs: "
                f"actual={act[key]!r} expected={exp[key]!r}"
            )


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
        report = _run_audit_json(EVAL_FIXTURES / fixture_name)
        return sum(r["score"] for r in report["results"])

    bad = _score("bad-readme-python-lib")
    good = _score("good-schema-nextjs-docs")
    assert good > bad, f"Good ({good}) should score higher than bad ({bad})"

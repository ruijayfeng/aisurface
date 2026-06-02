"""Baseline store unit tests (tmpdir-scoped)."""
from pathlib import Path

from scripts.verify import ProbeResult
from scripts.verify.baseline import BaselineStore


def test_round_trip_save_and_load(tmp_path: Path):
    store = BaselineStore(cache_root=tmp_path)
    results = [
        ProbeResult(query="q1", cited=True, citation_url="https://x/y", raw_response="..."),
        ProbeResult(query="q2", cited=False, citation_url=None, raw_response=""),
    ]
    store.save(project_root=tmp_path / "proj", platform="perplexity", results=results)
    loaded = store.load(project_root=tmp_path / "proj", platform="perplexity")
    assert loaded is not None
    assert len(loaded) == 2
    assert loaded[0].cited is True


def test_load_missing_returns_none(tmp_path: Path):
    store = BaselineStore(cache_root=tmp_path)
    assert store.load(project_root=tmp_path / "proj", platform="perplexity") is None


def test_different_projects_different_baselines(tmp_path: Path):
    store = BaselineStore(cache_root=tmp_path)
    r1 = [ProbeResult(query="a", cited=True, citation_url="x", raw_response="")]
    r2 = [ProbeResult(query="a", cited=False, citation_url=None, raw_response="")]
    store.save(project_root=tmp_path / "p1", platform="perplexity", results=r1)
    store.save(project_root=tmp_path / "p2", platform="perplexity", results=r2)
    assert store.load(project_root=tmp_path / "p1", platform="perplexity")[0].cited is True
    assert store.load(project_root=tmp_path / "p2", platform="perplexity")[0].cited is False


def test_diff_summary(tmp_path: Path):
    from scripts.verify.baseline import diff_summary
    baseline = [
        ProbeResult(query="q1", cited=False, citation_url=None, raw_response=""),
        ProbeResult(query="q2", cited=False, citation_url=None, raw_response=""),
    ]
    current = [
        ProbeResult(query="q1", cited=True, citation_url="https://x", raw_response=""),
        ProbeResult(query="q2", cited=False, citation_url=None, raw_response=""),
    ]
    summary = diff_summary(baseline, current)
    assert summary["baseline_cited"] == 0
    assert summary["current_cited"] == 1
    assert summary["delta"] == 1

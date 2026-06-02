"""Verify command integration tests (mocked Perplexity API)."""
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

EVAL_FIXTURES = Path(__file__).resolve().parents[2] / "evals" / "fixtures"


@pytest.mark.eval
def test_baseline_run_writes_cache_file(tmp_path, monkeypatch):
    """First verify run stores a baseline."""
    monkeypatch.setenv("PERPLEXITY_API_KEY", "fake-test-key")
    monkeypatch.setenv("AISURFACE_CACHE_DIR", str(tmp_path))

    # Mock httpx.Client.post to return a fake-no-citation response for all queries
    with patch("httpx.Client.post") as mock_post:
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "choices": [{"message": {"content": "..."}}],
            "citations": [],
        }
        response.raise_for_status = MagicMock()
        mock_post.return_value = response

        from scripts.verify import cmd_verify
        args = MagicMock(
            path=str(EVAL_FIXTURES / "minimal-cli-tool"),
            platforms="perplexity",
            baseline=False,
            queries_file=None,
        )
        rc = cmd_verify(args)

    assert rc == 0
    # Some baseline file got written
    baselines = list(tmp_path.glob("baselines/**/*.json"))
    assert len(baselines) >= 1


@pytest.mark.eval
def test_missing_api_key_actionable_error(monkeypatch, capsys):
    monkeypatch.delenv("PERPLEXITY_API_KEY", raising=False)
    monkeypatch.setenv("AISURFACE_CACHE_DIR", "/tmp/dummy")
    from scripts.verify import cmd_verify
    args = MagicMock(
        path=str(EVAL_FIXTURES / "minimal-cli-tool"),
        platforms="perplexity", baseline=False, queries_file=None,
    )
    rc = cmd_verify(args)
    captured = capsys.readouterr()
    assert rc != 0
    assert "PERPLEXITY_API_KEY" in captured.out + captured.err

"""PerplexityAdapter unit tests (mocked httpx)."""
from unittest.mock import MagicMock, patch

import pytest

from scripts.verify import ProbeResult
from scripts.verify.perplexity import PerplexityAdapter, PerplexityAPIError


def _fake_response(content: str, citations: list[str]) -> MagicMock:
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        "choices": [{"message": {"content": content}}],
        "citations": citations,
    }
    response.raise_for_status = MagicMock()
    return response


def test_probe_detects_citation(monkeypatch):
    adapter = PerplexityAdapter(api_key="fake", project_url="https://github.com/owner/proj")
    with patch("httpx.Client.post") as mock_post:
        mock_post.return_value = _fake_response(
            content="The best is github.com/owner/proj which does X.",
            citations=["https://github.com/owner/proj"],
        )
        result = adapter.probe("best library for X")
    assert isinstance(result, ProbeResult)
    assert result.cited is True
    assert result.citation_url == "https://github.com/owner/proj"


def test_probe_detects_no_citation(monkeypatch):
    adapter = PerplexityAdapter(api_key="fake", project_url="https://github.com/owner/proj")
    with patch("httpx.Client.post") as mock_post:
        mock_post.return_value = _fake_response(
            content="Use Foo or Bar.",
            citations=["https://example.com/foo"],
        )
        result = adapter.probe("best library for X")
    assert result.cited is False
    assert result.citation_url is None


def test_missing_api_key_raises():
    with pytest.raises(ValueError, match="api_key"):
        PerplexityAdapter(api_key="", project_url="https://x/y")


def test_api_error_raises_perplexity_api_error(monkeypatch):
    import httpx
    adapter = PerplexityAdapter(api_key="fake", project_url="https://x/y")
    with patch("httpx.Client.post") as mock_post:
        mock_post.side_effect = httpx.HTTPStatusError(
            "401", request=MagicMock(), response=MagicMock(status_code=401)
        )
        with pytest.raises(PerplexityAPIError):
            adapter.probe("x")

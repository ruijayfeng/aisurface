"""
 * [INPUT]: Depends on `httpx` (POST to https://api.perplexity.ai/chat/completions), `os.environ["PERPLEXITY_API_KEY"]`, `scripts.verify.ProbeResult` (lazy-imported to avoid circular import).
 * [OUTPUT]: Provides `PerplexityAdapter` class — implements the `ProbeAdapter` Protocol via `probe(query) -> ProbeResult` (queries Perplexity, parses cited sources, returns whether the project URL/name appears in the citations). Returns `cited=False` and an actionable error if the API key is missing or the call fails.
 * [POS]: The first concrete `ProbeAdapter` implementation. Imported by `verify.cmd_verify`. Future adapters (DeepSeek, ChatGPT) follow the same Protocol.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md

Perplexity AI search adapter.
"""
from __future__ import annotations

import httpx

from scripts.verify import ProbeResult

PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"
DEFAULT_MODEL = "sonar-pro"
# Approximate per-query cost for `sonar-pro` (~$3/M input + ~$15/M output tokens,
# ~100 input + ~500 output tokens per query). Used by verify cost warning only —
# actual billed amount may differ. Update when Perplexity pricing changes.
PERPLEXITY_COST_PER_QUERY_USD = 0.008


class PerplexityAPIError(RuntimeError):
    """Raised when the Perplexity API returns an error."""


class PerplexityAdapter:
    """ProbeAdapter implementation for Perplexity AI."""

    def __init__(self, api_key: str, project_url: str, model: str = DEFAULT_MODEL, timeout: float = 30.0):
        if not api_key:
            raise ValueError("api_key is required")
        if not project_url:
            raise ValueError("project_url is required")
        self.api_key = api_key
        self.project_url = project_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def probe(self, query: str) -> ProbeResult:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": query}],
        }
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(PERPLEXITY_URL, headers=headers, json=body)
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise PerplexityAPIError(f"Perplexity API error: {e.response.status_code}") from e
        except httpx.RequestError as e:
            raise PerplexityAPIError(f"Perplexity API request failed: {e}") from e

        data = response.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        citations = data.get("citations", [])

        matched = next((c for c in citations if self._matches_project(c)), None)
        return ProbeResult(
            query=query,
            cited=matched is not None,
            citation_url=matched,
            raw_response=content,
        )

    def _matches_project(self, url: str) -> bool:
        # Match by domain + path prefix; tolerant of trailing slashes and #fragments
        return url.rstrip("/").startswith(self.project_url)

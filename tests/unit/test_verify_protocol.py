"""ProbeAdapter Protocol contract test."""
from scripts.verify import ProbeAdapter, ProbeResult


def test_probe_result_is_dataclass():
    r = ProbeResult(query="x", cited=True, citation_url="https://example.com", raw_response="...")
    assert r.cited is True
    assert r.query == "x"


def test_protocol_runtime_checkable():
    class Fake:
        def probe(self, query: str) -> ProbeResult:
            return ProbeResult(query=query, cited=False, citation_url=None, raw_response="")
    assert isinstance(Fake(), ProbeAdapter)

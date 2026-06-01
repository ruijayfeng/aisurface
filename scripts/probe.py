"""Probe adapter for v0.1: stub. Real implementation lands in v0.3."""
from __future__ import annotations

from typing import Protocol


class ProbeAdapter(Protocol):
    """Protocol for v0.3 probe implementations."""

    def query(self, prompt: str, platform: str) -> "ProbeResult": ...


class ProbeResult:
    cited: bool
    citation_context: str
    platform: str


def probe_stub(prompt: str, platform: str) -> ProbeResult:
    """Returns a non-committal result. Replace in v0.3 with real probe."""
    return ProbeResult(
        cited=False,
        citation_context="(probe not yet implemented; coming in v0.3)",
        platform=platform,
    )

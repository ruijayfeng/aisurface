"""Verify subcommand: probe AI platforms for citation rate."""
from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass
class ProbeResult:
    """One platform's response to one query."""
    query: str
    cited: bool                  # True if user's project URL appeared in cited sources
    citation_url: str | None     # The specific URL cited (if any)
    raw_response: str            # Full platform response (for debugging / proof)


@runtime_checkable
class ProbeAdapter(Protocol):
    """Adapter for a single AI search platform."""
    def probe(self, query: str) -> ProbeResult: ...


def cmd_verify(args) -> int:
    """Stub - wired in Task 13."""
    print("verify command not fully wired yet", file=sys.stderr)
    return 1

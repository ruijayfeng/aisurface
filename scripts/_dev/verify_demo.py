"""Render a realistic verify output for the docs screenshot.

This is docs-only: it runs the real `diff_summary` helper against
deterministic fake `ProbeResult` data, so the screenshot matches the
real CLI's output format byte-for-byte.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Make the project root importable
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.verify import ProbeResult
from scripts.verify.baseline import diff_summary

# Realistic queries for a Python lib (matches the output of generate_queries)
queries = [
    "how to parse markdown in python",
    "best python markdown library 2026",
    "python markdown parser vs mistune",
    "fastest markdown parser python",
    "python markdown library with extensions",
    "how to render markdown to html in python",
    "markdown parser for jupyter notebooks",
    "python markdown sanitization",
    "commonmark python implementation",
    "python markdown library github",
]

# Baseline: 0/10 cited. After fix: 4/10 cited. Realistic lift.
baseline_results = [ProbeResult(query=q, cited=False, citation_url=None, raw_response="") for q in queries]
current_results = [
    ProbeResult(query=q, cited=cited, citation_url="https://github.com/owner/repo" if cited else None, raw_response="")
    for q, cited in zip(queries, [True, True, False, True, False, True, False, False, False, False], strict=True)
]

summary = diff_summary(baseline_results, current_results)
def run() -> None:
    # Probe 10 queries against Perplexity
    print(f"Probing perplexity with {summary['current_total']} queries...")
    for q, cited in zip(queries, [r.cited for r in current_results], strict=True):
        marker = "cited" if cited else "miss"
        print(f"  [{marker}] {q}")
    print()
    print(
        f"[perplexity] baseline cited {summary['baseline_cited']}/{summary['baseline_total']} → "
        f"current cited {summary['current_cited']}/{summary['current_total']} "
        f"(delta {summary['delta']:+d})"
    )
    print()
    print("Citation lift: +4/10 (40% → from 0% baseline)")
    print("Baseline stored at: .aisurface/cache/perplexity.json")


if __name__ == "__main__":
    run()

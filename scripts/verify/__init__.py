"""
 * [INPUT]: Depends on `scripts.scanner.scan_repo`, `scripts.verify.queries.generate_queries`, `scripts.verify.perplexity.PerplexityAdapter`, `scripts.verify.perplexity.PERPLEXITY_COST_PER_QUERY_USD`, `scripts.verify.baseline.BaselineStore`, `argparse` args (`--path`, `--platforms`, `--baseline`, `--queries-file`, `--max-queries`).
 * [OUTPUT]: Provides `ProbeResult` dataclass (platform, query, cited, sources), `ProbeAdapter` Protocol, `cmd_verify(args) -> int` (CLI dispatch target for the `verify` subcommand), and helpers `_print_cost_warning(platforms, n_queries)` + `_truncate_queries(queries, max_queries)`. Generates queries, prints cost estimate, truncates by `--max-queries`, probes each platform, loads/stores baseline, prints diff_summary.
 * [POS]: Verify subcommand core. Imported by `cli.py`. Dispatcher layer that sits above the per-platform adapters, the query generator, and the baseline store.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md

Verify subcommand: probe AI platforms for citation rate.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable


@dataclass
class ProbeResult:
    query: str
    cited: bool
    citation_url: str | None
    raw_response: str


@runtime_checkable
class ProbeAdapter(Protocol):
    def probe(self, query: str) -> ProbeResult: ...


def _print_cost_warning(platforms: list[str], n_queries: int) -> None:
    """Print estimated Perplexity cost to stdout. Silent for non-Perplexity platforms."""
    from scripts.verify.perplexity import PERPLEXITY_COST_PER_QUERY_USD
    if "perplexity" not in platforms:
        return
    est_total = n_queries * PERPLEXITY_COST_PER_QUERY_USD
    print(
        f"[verify] this run = {n_queries} Perplexity queries × "
        f"~${PERPLEXITY_COST_PER_QUERY_USD:.4f} ≈ ${est_total:.2f}"
    )


def _truncate_queries(queries: list[str], max_queries: int | None) -> list[str]:
    """Truncate queries to max_queries. Prints a stderr message when truncating."""
    if max_queries is None or len(queries) <= max_queries:
        return queries
    print(
        f"[verify] --max-queries={max_queries} truncates from {len(queries)} queries",
        file=sys.stderr,
    )
    return queries[:max_queries]


def cmd_verify(args) -> int:
    from scripts.scanner import scan_repo
    from scripts.verify.baseline import BaselineStore, diff_summary
    from scripts.verify.queries import generate_queries, load_queries_from_file

    repo_root = Path(args.path).resolve()
    if not repo_root.exists():
        print(f"Error: {repo_root} does not exist", file=sys.stderr)
        return 1

    cache_dir = os.environ.get("AISURFACE_CACHE_DIR")
    store = BaselineStore(cache_root=Path(cache_dir) if cache_dir else None)

    assets = scan_repo(repo_root)
    description = _read_first_paragraph(repo_root) or repo_root.name
    project_url = _infer_project_url(assets, repo_root)

    if args.queries_file:
        queries = load_queries_from_file(Path(args.queries_file))
    else:
        queries = generate_queries(
            project_name=repo_root.name,
            description=description,
            project_type=assets.project_type or "generic",
        )

    queries = _truncate_queries(queries, getattr(args, "max_queries", None))

    platforms = [p.strip() for p in args.platforms.split(",") if p.strip()]
    _print_cost_warning(platforms, len(queries))
    overall_rc = 0
    for platform_name in platforms:
        adapter = _load_adapter(platform_name, project_url=project_url)
        if adapter is None:
            overall_rc = 1
            continue
        results = _run_queries(adapter, queries, platform_name)
        baseline = store.load(repo_root, platform_name)
        if baseline is None or args.baseline:
            store.save(repo_root, platform_name, results)
            cited = sum(1 for r in results if r.cited)
            print(f"[{platform_name}] baseline established: cited {cited}/{len(results)} queries")
        else:
            store.save(repo_root, platform_name, results)
            summary = diff_summary(baseline, results)
            print(
                f"[{platform_name}] baseline cited {summary['baseline_cited']}/{summary['baseline_total']} → "
                f"current cited {summary['current_cited']}/{summary['current_total']} "
                f"(delta {summary['delta']:+d})"
            )
    return overall_rc


def _load_adapter(name: str, project_url: str) -> ProbeAdapter | None:
    if name == "perplexity":
        api_key = os.environ.get("PERPLEXITY_API_KEY", "")
        if not api_key:
            print("Error: PERPLEXITY_API_KEY not set. Get a key at https://perplexity.ai/account/api", file=sys.stderr)
            return None
        from scripts.verify.perplexity import PerplexityAdapter
        return PerplexityAdapter(api_key=api_key, project_url=project_url)
    print(f"Error: unknown platform '{name}'. Supported: perplexity", file=sys.stderr)
    return None


def _run_queries(adapter: ProbeAdapter, queries: list[str], platform_name: str) -> list[ProbeResult]:
    results: list[ProbeResult] = []
    for q in queries:
        try:
            r = adapter.probe(q)
        except Exception as e:
            print(f"[{platform_name}] query failed: {q!r} — {e}", file=sys.stderr)
            r = ProbeResult(query=q, cited=False, citation_url=None, raw_response=f"ERROR: {e}")
        results.append(r)
    return results


def _read_first_paragraph(repo_root: Path) -> str | None:
    readme = repo_root / "README.md"
    if not readme.exists():
        return None
    import re
    text = readme.read_text(encoding="utf-8")
    match = re.search(r"^#\s+\S.*?\n+([^\n#].+?)(?:\n|$)", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def _infer_project_url(assets, repo_root: Path) -> str:
    """Best-effort: read 'homepage' from package.json/pyproject.toml, else fallback to a placeholder."""
    pyproject = repo_root / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text(encoding="utf-8")
        import re
        m = re.search(r'homepage\s*=\s*"([^"]+)"', text)
        if m:
            return m.group(1)
    return f"https://github.com/UNKNOWN/{repo_root.name}"

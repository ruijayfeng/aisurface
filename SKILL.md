---
name: aisurface-audit
description: Use when the user wants to audit a local open-source project for AI-search citation readiness (GEO). Triggers on: "audit my repo for AI search", "check GEO readiness", "evaluate AI citation potential", "is my project AI-search-friendly", "GEO audit", or any request to scan a project directory for AI search optimization opportunities. Runs a 12-check audit (4 structural via Python + 8 semantic via LLM critic) and produces a Markdown report with prioritized fixes. Supports `--learn` teacher mode for users unfamiliar with GEO.
---

# aisurface@audit

Audit a local open-source project for AI-search citation readiness. Run from the project root:

```bash
python -m scripts.cli .
```

Or with the `aisurface` console script (after `pip install -e .`):

```bash
aisurface .
```

## What it checks (12 items)

| # | Check | Type |
|---|---|---|
| 1 | README problem statement | Semantic (LLM critic) |
| 2 | README has FAQ section | Semantic (LLM critic) |
| 3 | README when to use / not to use | Semantic (LLM critic) |
| 4 | README has runnable code examples | Semantic (LLM critic) |
| 5 | Schema.org markup on website | Structural (Python) |
| 6 | `.well-known/llms.txt` present | Structural (Python) |
| 7 | GitHub topics complete (8-12) | Structural (GitHub API) |
| 8 | FAQ section heading in README | Semantic (heuristic) |
| 9 | When to use / not to use in README | Semantic (heuristic) |
| 10 | Citation-worthy content | Semantic (heuristic) |
| 11 | Distribution signals | Structural (heuristic) |
| 12 | AI search platforms named in README | Semantic (heuristic) |

## Modes

- **Engineer mode (default)**: terse output, just the report.
- **Teacher mode (`--learn`)**: prepends 30-second concept primer before each check. Use this if you're new to GEO.
- **`--no-color`** — disable color output. Equivalent to setting the `NO_COLOR=1` environment variable.

## Output

A Markdown report with:
- Health score (0-100)
- 🔴 Must-fix (3-5 items, sorted by impact)
- 🟡 Should-fix (3-5 items)
- 🟢 Nice-to-have (3-5 items)
- ⏭️ Skipped checks + reasons
- ❌ Errors + reasons

## Action options

After the report, pick:
- **Just review** (default): user reads report, modifies themselves
- **Auto-fix**: invoke `aisurface@readme` or `aisurface@llms-txt` for the must-fix items
- **Generate diffs**: `--patch` flag generates a unified diff for the top 3 must-fixes

## What it does NOT do

- Does NOT call live AI APIs to verify citation (that's `aisurface@probe`, coming v0.3)
- Does NOT modify files (use sub-skills for that)
- Does NOT support non-OSS projects (URLs, marketing sites) — see `coreyhaines31/marketingskills@seo-audit` for that

## Requirements

- Python 3.10+
- Local project directory (not URLs)
- For structural checks: read access to repo
- For semantic checks: no LLM needed in v0.1 (offline heuristic); v0.3 will add real LLM

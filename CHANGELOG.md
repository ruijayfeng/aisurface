# Changelog

## [1.0.0] - 2026-06-02

### Added
- PyPI publish-ready: classifiers + project URLs (hatchling-built wheel, `packages = ["scripts"]`)
- 3-verb CLI documented in single root SKILL.md
- `case-studies/ziwei-v100.md`: real-world before/after using the full v1.0 loop

### Changed
- Consolidated 3 SKILL.md files into 1 (`@readme` and `@llms-txt` moved to `skills/_deprecated/`)
- README rewritten with 3-verb opening + screenshots

### Removed
- `scripts/probe.py` stub (already gone in v0.1.3)
- The original "skill collection" decomposition: now 1 unified CLI + skill

### Deprecated
- `skills/_deprecated/aisurface-readme/SKILL.md` — use `aisurface fix .`
- `skills/_deprecated/aisurface-llms-txt/SKILL.md` — use `aisurface fix . --only=llms_txt`
- Both deprecated SKILL.md files will be removed in v1.1.

## [0.1.3] - 2026-06-02

### Added
- `aisurface verify` subcommand: probes AI platforms for citation rate
  - PerplexityAdapter (real API client, mocked in tests)
  - Query generator with per-project-type templates (10 queries default)
  - Baseline store at `~/.aisurface/baselines/<hash>/<platform>.json`
  - `--platforms`, `--baseline`, `--queries-file` flags
- Custom cache dir via `AISURFACE_CACHE_DIR` env var (mainly for testing)
- Actionable error when `PERPLEXITY_API_KEY` is missing

### Changed
- Removed legacy `scripts/probe.py` stub (replaced by `scripts/verify/` module)

### Tests
- 105 tests passing (up from 89 in v0.1.2)

## [0.1.2] - 2026-06-02

### Added
- `aisurface fix` subcommand: generates and applies patches for the 4 highest-impact must-fix items
  - FAQ injection (templated 8 Q&A per project type, defaults to "generic")
  - When-to-use stubs (both halves or just the missing one)
  - `.well-known/llms.txt` (new file, per llmstxt.org spec)
  - `index.schema.json` (SoftwareApplication + FAQPage)
- `fix` flags: `--dry-run`, `--yes`, `--only=faq,when_to_use,llms_txt,schema_org`
- Snapshot tests for patch output (`evals/expected_patches/`)

### Changed
- CLI now uses subparsers: `aisurface audit ./` (was `python -m scripts.cli ./`)
- Old direct invocation `python -m scripts.cli ./` requires `audit` subcommand
- `scripts/audit.py` split out from `scripts/cli.py` for separation of concerns

### Tests
- 89 tests passing (up from 67 in v0.1.1)

## [0.1.1] - 2026-06-02

### Added
- 4th eval fixture: `perfect-readme-and-docs` (sanity-check audit upper bound; hits 96/100 weighted, all 12 checks pass)
- `StructuralFinding(CheckResult)` typed subclass with `file_path` field for file-based structural checks (#5 schema.org, #6 llms.txt)
- `@safe_check` decorator skeleton (v0.3 interface; v0.1.1 staging — catch path exercised only in tests)
- Weighted health score (Citation-Friendliness 40 / Structure 30 / Readability 20 / Distribution 10) replacing the v0.1.0 equal-weight formula
- ANSI color output for the CLI (auto-detected, `--no-color` opt-out, `NO_COLOR` env var support)
- `--no-color` CLI flag (documented in SKILL.md)

### Changed
- `_compute_health_score` now takes a `categories: dict[str, list[CheckResult]]` and returns `(score, max_score=100)` instead of a flat sum/max ratio
- `AuditReport` gains `health_score: int` and `max_score: int` fields (defaults `0` and `100`)
- `render_report` now shows 4 sub-scores (one per category) instead of 2
- `CheckResult` gains `skipped: bool` and `error: str | None` fields (defaults `False` and `None`)
- `AuditReport` gains `skipped: list[CheckResult]` and `errors: list[str]` fields (v0.3 staging; empty in v0.1.1)
- `--json` output now includes `skipped` and `error` keys per result row
- Distribution check #11 threshold lowered from 6 to 5 (v0.1's `github_stars=0` stub made 6 unreachable; threshold matches the locally-observable max from registries + description)
- Distribution check #11 now reads real `has_npm`/`has_pypi` from the scanner (was hardcoded `False`); `RepoAssets` gains those two fields
- `offline_critique` removed arbitrary 9→10 sub-ceilings on `has_faq` and `has_code_examples` (unambiguous max signals)
- 4 eval fixtures' expected JSONs re-recorded (the 3 v0.1.0 fixtures plus the new 4th)
- CHANGELOG "Known gaps for v0.1.1" subsection under `[0.1.0]` removed (4 of 5 items delivered, remaining deferred to v0.1.2+)

### Tests
- 67 tests passing (up from 54 in v0.1.0)

## [0.1.0] - 2026-07-15

### Added
- `aisurface@audit` skill: 12-check GEO audit
- `aisurface@readme` skill: README optimization
- `aisurface@llms-txt` skill: generate `.well-known/llms.txt`
- Python scripts: scanner, schema_gen, llms_txt, github_meta, distribution, critic, report, cli
- 3 eval fixtures: bad-readme-python-lib, good-schema-nextjs-docs, minimal-cli-tool
- Bilingual README (zh + en)
- Case study: ruijayfeng/ziwei before/after

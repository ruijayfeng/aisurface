# scripts/
> L2 | Parent: /CLAUDE.md | Python 3.10+ stdlib + httpx + jsonschema + selectolax

## Member List
- `__init__.py`: Package marker, no logic.
- `cli.py`: CLI entry point, thin dispatcher to `audit` / `fix` / `verify` / `doctor` subcommands. `argparse` subparsers. Console-script target `aisurface = scripts.cli:main`. Each handler is wrapped in `@safe_dispatch` to convert user-facing errors to actionable stderr hints.
- `audit.py`: 12-check GEO audit logic. Returns `AuditReport`. Pure function over `RepoAssets` + README text.
- `report.py`: Render `AuditReport` as Markdown. Owns 40/30/20/10 weighted health score, must-fix/should-fix/nice-to-have bucketing. Exports `AuditReport`, `CheckResult`, `CATEGORY_CHECK_IDS`, `CATEGORY_WEIGHTS`, `_compute_health_score`.
- `scanner.py`: Walk a repo and build `RepoAssets` (README path, project_type, llms.txt presence, schema files). Prunes `node_modules`/`.venv`/`dist`/etc.
- `findings.py`: Defines `StructuralFinding` (subclass of `CheckResult` carrying a `file_path`).
- `critic.py`: Semantic check heuristics (regex over README). Pre-LLM stub; `--llm` flag in v0.1.4 swaps this for a real LLM call.
- `github_meta.py`: GitHub topics count + repo description lookup (uses `gh` CLI, not API).
- `distribution.py`: Distribution-signal heuristic (awesome-list mention, npm/PyPI presence).
- `concepts.py`: 1-2 sentence teacher-mode primers for each of the 12 checks, loaded by `--learn`.
- `colors.py`: ANSI colorize wrapper with `NO_COLOR=1` / `--no-color` opt-out.
- `safe_check.py`: Decorator that wraps each check in try/except, turns failures into `skipped` results with an `error` field.
- `safe_dispatch.py`: Decorator that wraps each `cmd_*` handler. Catches 4 user-facing exception classes (`ModuleNotFoundError` for `scripts.*`, `FileNotFoundError` on `args.path`, `UnicodeEncodeError`, `PermissionError` on the cache dir) and prints actionable hints to stderr before exiting 1. Re-raises everything else.
- `llms_txt.py`: Build a valid llms.txt body per https://llmstxt.org. `build_llms_txt(project_name, description, sections, details)` and `write_llms_txt(repo, ...)`.
- `schema_gen.py`: Build Schema.org JSON-LD objects. `build_software_application(...)`, `build_faq_page(questions)`.
- `probe.py`: Legacy stub from v0.1. Will be removed in v0.1.3 when `scripts/verify/` lands.
- `doctor.py`: Install-health self-check. Exports `cmd_doctor`, `DoctorCheck` dataclass, 7 check_* functions (internet reachability is implicit in `check_pypi_latest_version`), `render_human` / `render_json`. Used by `cli.py` as the 4th subcommand. Exits 0 (all pass/warn) / 1 (any fail) / 2 (Python < 3.10).

## Pending (v0.1.2 — fix verb)
- `fix/__init__.py`: Patch dataclass + `cmd_fix` dispatcher.
- `fix/faq.py`: FAQ-section injection patch (templated 8 Q&A per project type).
- `fix/when_to_use.py`: When-to-use / When-NOT-to-use stub patch.
- `fix/llms_txt.py`: Wraps `llms_txt.py` for the fix context.
- `fix/schema_org.py`: Wraps `schema_gen.py` for the fix context.

## Pending (v0.1.3 — verify verb)
- `verify/__init__.py`: `ProbeAdapter` Protocol + `ProbeResult` dataclass + `cmd_verify` dispatcher.
- `verify/perplexity.py`: `PerplexityAdapter` over httpx.
- `verify/queries.py`: Per-project-type query template generator.
- `verify/baseline.py`: File-backed `BaselineStore` at `~/.aisurface/baselines/<hash>/<platform>.json` + `diff_summary`.

## Rule
One file, one responsibility. No file > 800 lines. If a file grows, split by responsibility, not by technical layer. Every file has an L3 `[INPUT]/[OUTPUT]/[POS]` header at the top — see the GEB protocol in `/CLAUDE.md`.

[PROTOCOL]: Update this header when a file is added, deleted, renamed, or its responsibility/interface changes. Then check the L1 `/CLAUDE.md` directory tree.

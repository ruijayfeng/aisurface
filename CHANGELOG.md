# Changelog

## [0.1.0] - 2026-07-15

### Added
- `aisurface@audit` skill: 12-check GEO audit
- `aisurface@readme` skill: README optimization
- `aisurface@llms-txt` skill: generate `.well-known/llms.txt`
- Python scripts: scanner, schema_gen, llms_txt, github_meta, distribution, critic, report, cli
- 3 eval fixtures: bad-readme-python-lib, good-schema-nextjs-docs, minimal-cli-tool
- Bilingual README (zh + en)
- Case study: ruijayfeng/ziwei before/after

### Known gaps for v0.1.1

These were identified during final code review but deferred to keep v0.1.0 shippable. None of them block the public launch; they are planned for the next patch release.

- **Perfect-readme-and-docs eval fixture (4th).** The 3 current fixtures exercise low/mid/edge cases; a 4th "ideal" fixture is needed to confirm the audit's upper bound (target score ≥ 90) and to regression-test the rubric ceiling.
- **`--patch` flag.** Generate a unified diff for the top 3 must-fixes so users can `git apply` directly. Requires reading the actual repo files and templating per-fix transformations (FAQ injection, when-to-use section stub, etc.).
- **LLM call resilience.** v0.1's `offline_critique` is deterministic and doesn't need try/except. v0.3 will call real LLMs and needs per-check error containment so a single provider failure doesn't abort the whole audit.
- **`GITHUB_TOKEN` integration.** v0.1's scanner uses local files only; `distribution.check_signals` is called with `github_stars=0` placeholder. v0.3 should optionally read the token from env and call `gh api` / REST to fetch real stars, topics, and description.
- **`ProbeAdapter` real implementation.** `scripts/probe.py` ships a stub returning "not yet implemented." v0.3 will wire 4-10 platform adapters (ChatGPT, Perplexity, DeepSeek, Doubao) behind the existing `ProbeAdapter` protocol.
- **`StructuralFinding` vs `CheckResult` cleanup.** v0.1 uses one `CheckResult` dataclass for both structural and semantic checks. If a future check needs structural-only fields (e.g. file path of the missing schema), introduce a typed subclass rather than overloading `CheckResult`.

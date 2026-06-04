# aisurface — Make your open-source project surface in AI search results

> L1 | Python 3.10+ + httpx + jsonschema + selectolax + pytest + ruff

## Current State
**Shipped**: v0.1.1 (tag pushed 2026-06-02). `audit` command works end-to-end (67 tests, 4 eval fixtures).
**In progress**: v1.0 — unify 3 skills into 1, add `fix` + `verify` verbs, publish to PyPI. See `ROADMAP.md` and `docs/superpowers/plans/2026-06-02-aisurface-v100.md`.

## Architecture Principles
- **Skill-first install.** The primary user entry point is `npx skills add ruijayfeng/aisurface`. `pip install aisurface` is an implementation detail handled by the skill at first invocation. See `docs/superpowers/specs/2026-06-02-aisurface-v100-design.md` §11b.
- **User-facing abstraction.** The `SKILL.md` exposes capabilities in plain language and hides CLI flags, subcommand names, and storage paths. See same spec §3 + §11b.
- **GEB fractal docs.** L1 here, L2 in each module's `CLAUDE.md`, L3 as file-header contracts in `scripts/*.py`. Every change touches its layer.

## Directory
```
aisurface/
├── SKILL.md              - Unified skill definition (name: aisurface), single user-facing surface
├── scripts/              - Python implementation (cli, audit, report, fix/, verify/, scanner, doctor, safe_dispatch, ...)
├── skills/
│   └── _deprecated/      - v0.1.x sub-skills (aisurface-readme, aisurface-llms-txt) — will be removed in v1.1
├── tests/                - pytest suite (unit/ + integration/)
├── evals/                - Fixture-based eval suite + trigger_evals.json (for skill description optimization)
├── references/           - Knowledge base (AI platforms, schema templates, GEO checklist, llms.txt spec)
├── case-studies/         - Real-world before/after (ziwei is the canonical case)
├── docs/
│   ├── superpowers/
│   │   ├── plans/        - Implementation plans (this plan + the v1.0 plan)
│   │   └── specs/        - Specs (v1.0 design, etc.)
│   └── (user-facing docs land here)
├── .github/              - CI workflow + issue/PR templates
├── CONTRIBUTING.md       - Contributor guide (Python CLI usage, dev setup, new-check howto)
└── CLAUDE.md             - This file (L1)
```

## Config Files
- `pyproject.toml` — package metadata, deps, console script `aisurface = scripts.cli:main`, pytest/ruff config
- `ROADMAP.md` — release sequence (v0.1.0 → v1.0)
- `CHANGELOG.md` — release notes
- `README.md` / `README.en.md` — bilingual project README (skill-first: lead with `npx skills add` + natural-language demo; no CLI in user-facing surface)
- `CONTRIBUTING.md` — contributor guide (issue/PR, dev setup, adding new checks, Python CLI usage for CI / automation)
- `SKILL.md` — root skill descriptor (unified `aisurface`)

## Active Specs & Plans
- **v1.0 design**: `docs/superpowers/specs/2026-06-02-aisurface-v100-design.md` (or sibling-repo mirror)
- **v1.0 plan**: `docs/superpowers/plans/2026-06-02-aisurface-v100.md` (or sibling-repo mirror)
- **Skill optimization plan** (this one): `docs/superpowers/plans/2026-06-03-aisurface-skill-optimization-and-v1-bridge.md`

## Rule
Minimal · stable · navigation. Update on any architecture-level change (new module, file move, responsibility shift, skill structure change, install story change).

[PROTOCOL]: Update this header when changed, then check all L2 CLAUDE.md files and the L3 file headers in scripts/.

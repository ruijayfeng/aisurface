# aisurface Roadmap

> Single source of truth for what ships when. Updated 2026-06-03.

## Final Form: v1.0

One CLI, three verbs:

```bash
aisurface audit ./         # diagnose: 12-check GEO report
aisurface fix ./           # treat: auto-apply patches for must-fix items
aisurface verify ./        # prove: probe AI platforms for citation rate
```

**Install**: `npx skills add ruijayfeng/aisurface` is the primary path. The skill handles `pip install aisurface` internally on first invocation. `pip install aisurface` standalone is supported for CI and non-Claude-Code users.

**Full v1.0 spec**: `docs/superpowers/specs/2026-06-02-aisurface-v100-design.md` (or sibling-repo mirror in `../SkillsCreate/InitSkill/docs/superpowers/specs/`)
**Full v1.0 plan**: `docs/superpowers/plans/2026-06-02-aisurface-v100.md` (or sibling-repo mirror)
**Skill optimization plan** (this one): `docs/superpowers/plans/2026-06-03-aisurface-skill-optimization-and-v1-bridge.md`

## Release Sequence

| Version | Scope | Status |
|---|---|---|
| v0.1.0 | 3 skills, audit-only, 12-check rubric, weighted score 0/0/0/0 (flat sum) | ✅ shipped 2026-06-02 |
| v0.1.1 | 4th fixture, StructuralFinding, safe_check skeleton, weighted 40/30/20/10, ANSI colors | ✅ shipped 2026-06-02 |
| v0.1.2 | `fix` command — 4 patch generators (FAQ, when-to-use, llms.txt, schema.org) | ✅ shipped 2026-06-02 |
| v0.1.3 | `verify` command — Perplexity adapter + baseline store | ✅ shipped 2026-06-02 |
| **v1.0.0** | **Consolidate 3 skills → 1 unified `aisurface` skill, PyPI publish, screenshots, ziwei re-dogfood** | ✅ shipped 2026-06-02 |
| **v1.0.1** | **Skill abstraction principle — single natural-language-facing SKILL.md, GEB fractal docs (L1/L2/L3), §11b in spec, skill-first install story across README/ROADMAP** | ✅ shipped 2026-06-03 |
| **v1.0.2** | **Windows install / PATH hotfix — `aisurface doctor` self-check + `safe_dispatch` error wrapper + 15-job CI matrix (3 OS × 5 Python). README 5-min self-test now uses `python -m scripts.cli` (cross-platform).** | ✅ shipped 2026-06-03 |
| v0.1.4 (optional) | `--llm` flag — swap regex critic for real LLM | ⏳ optional |
| v1.1.0 | Remove `skills/_deprecated/` (one release deprecation cycle complete); add more platform adapters per real-user signal | ⏳ planned |

## Platform Coverage

**Currently shipped (v1.0.x):**
- **Perplexity** — `verify` uses the real Perplexity API (requires `PERPLEXITY_API_KEY`)

**Diagnose + Treat are platform-agnostic:** they check what every AI engine looks for (README structure, `llms.txt`, Schema.org, FAQ, when-to-use, code examples), so they help regardless of which AI your users actually use.

**On the v1.1+ roadmap:**
- ChatGPT (OpenAI)
- Claude (Anthropic)
- Gemini (Google)
- DeepSeek
- 豆包 (Doubao)
- 文心一言 (Baidu)
- 通义千问 (Alibaba)
- Kimi (Moonshot)
- 智谱 / GLM

**Why slow?** Real-platform citation probing is per-API cost + per-API rate-limit + per-API contract. Each adapter takes ~1-2 weeks. We ship a v1.0 that's honest about one platform rather than claim ten and deliver one.

See "Future (v1.1+, not committed)" below for the trigger criteria that moves a platform from "roadmap" to "shipped".

## Architecture Principles (from spec §11b)

- **Skill-first install.** The primary user entry point is `npx skills add ruijayfeng/aisurface`. `pip install aisurface` is an implementation detail handled by the skill at first invocation.
- **User-facing abstraction.** The `SKILL.md` exposes capabilities in plain language (3 verbs, natural-language triggers) and hides CLI flags, subcommand names, and storage paths. See spec §3 + §11b.
- **GEB fractal docs.** L1 (`/CLAUDE.md`), L2 (each module's `CLAUDE.md`), L3 (`[INPUT]/[OUTPUT]/[POS]` file headers in `scripts/*.py`).

## What v1.0 Is NOT

Killed from the original 2026-06-01 spec (which planned 8 skills + MCP + 4 platforms over W37+):
- ❌ `@schema` `@docs` `@landing-page` as standalone skills — patch targets inside `fix`
- ❌ MCP server — CLI already invocable from Claude Code
- ❌ 4-platform probe — start with 1-2 (Perplexity + DeepSeek)
- ❌ Real LLM critic as default — opt-in `--llm` flag only
- ❌ "Skill collection" model — 1 binary, 3 subcommands

See v1.0 spec §4 for the full kill list and rationale.

## Future (v1.1+, not committed)

These are ideas, not commitments. Re-evaluate after v1.0 launches and real users surface real needs:

- More platform adapters: ChatGPT, Claude, Gemini, DeepSeek, Doubao
- Trend charts for `verify` (historical citation rate over time)
- `aisurface init` — bootstrap a new project with all GEO-ready scaffolding
- MCP server (only if a real user asks)
- Real LLM critic as default (only if regex critic proves insufficient on real-user data)

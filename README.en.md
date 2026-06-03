# aisurface

> Make your open-source project surface in AI search results.

[![PyPI](https://img.shields.io/pypi/v/aisurface)](https://pypi.org/project/aisurface/)
[![Python 3.10+](https://img.shields.io/pypi/pyversions/aisurface)](https://pypi.org/project/aisurface/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-105%20passing-brightgreen)](./tests)

[English](./README.en.md) | [中文](./README.md)

```bash
npx skills add ruijayfeng/aisurface
```

After install, just say "audit my project" — the skill handles the Python environment itself.

```text
"is my project AI-citation-friendly"     →  diagnose
"fix my README for AI search"            →  treat
"does my project show up in AI search"   →  prove
```

![audit](docs/screenshots/audit.png)
![fix](docs/screenshots/fix.png)
![verify](docs/screenshots/verify.png)

## v1.0.1 released (2026-06-03)

- **User-facing abstraction principle** (spec §11b): the skill surface exposes only capabilities, not command names like `aisurface audit` / `fix` / `verify`; triggers are natural language
- **GEB fractal documentation system**: L1 (`CLAUDE.md`) / L2 (per-module `CLAUDE.md`) / L3 (`INPUT/OUTPUT/POS` headers in `scripts/*.py`) — three layers stay in sync
- **Fixed**: L3 header `from __future__ import annotations` is back on line 1 (the L3 string block had been placed before the original docstring, and Python rejected any non-`__future__` string preceding a `__future__` import)

Full changelog: [CHANGELOG.md](./CHANGELOG.md).

aisurface is a Claude Code tool that helps **open-source project maintainers** get their projects **actively cited by AI search** (Doubao / DeepSeek / ChatGPT / Gemini / Claude / Perplexity / Kimi / Wenxin / Tongyi / GLM / ...).

## Why aisurface?

In 2026, developers don't Google "Python Markdown parser library" — they ask ChatGPT "recommend a Python Markdown parser library."

AI cites only 3-5 sources. **If your project isn't in those 3-5, you don't exist to AI users.**

Existing skills (`seo-audit`, `seo-geo`) only diagnose URL-perspective English Google SEO, not open-source projects, not Chinese AI. aisurface fills that gap.

## Three-verb workflow

```bash
# 1) Audit: 12 GEO checks, weighted health score 0-100
aisurface audit .

# 2) Fix: auto-generate 4 highest-impact patches
aisurface fix .

# 3) Verify: probe real AI platforms, diff against stored baseline
export PERPLEXITY_API_KEY=...
aisurface verify .                # first run: establish baseline
aisurface fix .                   # apply patches
aisurface verify .                # second run: measure the lift
```

`fix` generates: FAQ stub in README, When-to-use sections, `.well-known/llms.txt`, `index.schema.json`. Review the diff, confirm, done.

`verify` probes 10 representative queries against Perplexity (more platforms coming) and compares the citation rate to a stored baseline.

## 12-check audit

| # | Check | Type |
|---|---|---|
| 1 | README problem statement | Semantic |
| 2 | README FAQ section | Semantic |
| 3 | README when to use / not to use | Semantic |
| 4 | README runnable code examples | Semantic |
| 5 | Schema.org markup | Structural |
| 6 | `.well-known/llms.txt` | Structural |
| 7 | GitHub topics complete (8-12) | Structural |
| 8 | FAQ section heading in README | Semantic |
| 9 | When to use / not to use in README | Semantic |
| 10 | Citation-worthy content (numbers / code / named entities) | Semantic |
| 11 | Distribution signals (awesome / npm / PyPI) | Structural |
| 12 | AI search platforms named in README | Semantic |

## Case study

We use [ruijayfeng/ziwei](https://github.com/ruijayfeng/ziwei) for v1.0 dogfooding:
- **Baseline**: health score 35/100, 5 🔴 Must-fix items
- **After applying 4 patches**: health score 87/100, all 🔴 cleared (+52)

See [case-studies/ziwei-v100.md](./case-studies/ziwei-v100.md).

## 5-minute self-test

You can verify the package end-to-end **without** Claude Code and **without** an AI platform API — `pip install aisurface` plus the bundled fixtures give you deterministic output.

```bash
# 1) Install / upgrade to the latest PyPI release (should report 1.0.1)
pip install --upgrade aisurface
pip show aisurface                  # Version: 1.0.1

# 2) The 3-verb CLI is wired up
aisurface --help                    # expect {audit, fix, verify}

# 3) Run a known-bad fixture — expect health 16/100, 4 sub-scores, all 12 checks rendered
aisurface audit evals/fixtures/bad-readme-python-lib --no-color

# 4) Run the known-good fixture — expect 90+ (sanity check on the upper bound)
aisurface audit evals/fixtures/perfect-readme-and-docs --no-color

# 5) See what `fix` would write (no disk writes)
aisurface fix evals/fixtures/bad-readme-python-lib --dry-run

# 6) Run on your own project (numbers will differ from the fixtures — that's expected)
aisurface audit /path/to/your/repo --no-color

# 7) (Optional) Real citation verification — needs PERPLEXITY_API_KEY
export PERPLEXITY_API_KEY=pplx-...
aisurface verify /path/to/your/repo        # first run: stores baseline in ~/.aisurface/baselines/
```

Steps 1-5 confirm the v1.0.1 package itself: no broken imports, no missing files, all three CLI verbs work. Step 6 is the real test — run it on an actual repo you maintain. Step 7 needs a paid API key, skip it if you don't have one.

## Installation

Primary path (recommended):

```bash
npx skills add ruijayfeng/aisurface
```

After install, just say "audit my project" — the skill handles the Python environment itself.

Alternative (for CI or non-Claude-Code users):

```bash
pip install aisurface
aisurface audit ./
```

## Contributing

Issues / PRs / case studies welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

MIT

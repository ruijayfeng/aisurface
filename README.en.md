# aisurface

> Make your open-source project surface in AI search results.

[English](./README.en.md) | [中文](./README.md)

aisurface is a collection of Claude Code skills that helps **open-source project maintainers** get their projects **actively cited by AI search** (Doubao / DeepSeek / ChatGPT / Gemini / Claude / Perplexity / Kimi / Wenxin / Tongyi / GLM / ...).

## Why aisurface?

In 2026, developers don't Google "Python Markdown parser library" — they ask ChatGPT "recommend a Python Markdown parser library."

AI cites only 3-5 sources. **If your project isn't in those 3-5, you don't exist to AI users.**

Existing skills (`seo-audit`, `seo-geo`) only diagnose URL-perspective English Google SEO, not open-source projects, not Chinese AI. aisurface fills that gap.

## Installation

```bash
# Flagship: repo audit
npx skills add ruijayfeng/aisurface@audit

# Sub-skill: README optimization
npx skills add ruijayfeng/aisurface@readme

# Sub-skill: generate llms.txt
npx skills add ruijayfeng/aisurface@llms-txt
```

## Quick start

Run from your open-source project root:

```bash
aisurface .
```

It outputs a report: 12 checks, Health score (0-100), 🔴 Must-fix list. The 12 checks contribute to a weighted health score (Citation-Friendliness 40 / Structure 30 / Readability 20 / Distribution 10) reflecting which gaps hurt AI citation most.

### One-command fix

After auditing, you can auto-apply patches for the 4 most common issues:

```bash
aisurface fix .
```

This generates: FAQ stubs in README, When-to-use sections, .well-known/llms.txt, and index.schema.json. Review the diff, confirm, done.

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

We use [ruijayfeng/ziwei](https://github.com/ruijayfeng/ziwei) for dogfooding:

- **before**: health score 35/100, 5 🔴 Must-fix items
- **after** (~30 minutes: run audit + apply 5 must-fixes): health score 66/100, all 🔴 cleared

See [case-studies/ziwei-before-after.md](./case-studies/ziwei-before-after.md).

## Roadmap

- **v0.1** (W6 release): `audit` + `readme` + `llms-txt` (3 skills)
- **v0.2** (W13): + `aisurface@schema` + `aisurface@docs` + `aisurface@landing-page`
- **v0.3** (W25): + `aisurface@probe` (AI platform API verification)
- **v0.4+**: MCP server, IDE integration

## Contributing

Issues / PRs / case studies welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

MIT

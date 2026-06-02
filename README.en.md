# aisurface

> Make your open-source project surface in AI search results.

[English](./README.en.md) | [中文](./README.md)

```bash
pip install aisurface

aisurface audit ./        # diagnose: 12-check GEO report
aisurface fix ./          # treat: auto-apply patches
aisurface verify ./       # prove: probe AI platforms for citation lift
```

![audit](docs/screenshots/audit.png)
![fix](docs/screenshots/fix.png)
![verify](docs/screenshots/verify.png)

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

## Installation

```bash
pip install aisurface
```

## Contributing

Issues / PRs / case studies welcome. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

MIT

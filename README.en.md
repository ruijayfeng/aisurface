# aisurface

> Make your open-source project surface in AI search results.

[![PyPI](https://img.shields.io/pypi/v/aisurface)](https://pypi.org/project/aisurface/)
[![Python 3.10+](https://img.shields.io/pypi/pyversions/aisurface)](https://pypi.org/project/aisurface/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-140%20passing-brightgreen)](./tests)

English | [中文](./README.md)

## 30-second setup

```bash
npx skills add ruijayfeng/aisurface
```

After install, just talk to your agent in plain English — the skill handles the Python environment itself:

```text
"is my project AI-citation-friendly"     →  diagnose
"fix my README for AI search"            →  treat
"does my project show up in AI search"   →  prove
```

No commands to memorize. Say whatever feels natural; the agent does the work.

## v1.0.2 released (2026-06-04)

- **New install self-check**: if your Windows install can't find the command, just ask the agent — it'll tell you exactly which directory to add to PATH
- **Friendly error hints for 4 common failures**: Python missing / bad path / encoding / unwritable cache — no more stack traces
- **5-min self-test now uses a cross-platform form**: same command on macOS, Linux, and Windows
- **CI expanded to 15 jobs**: 3 OS × Python 3.10-3.14, with a self-check smoke test

Full changelog: [CHANGELOG.md](./CHANGELOG.md).

## Why aisurface?

In 2026, developers don't Google "Python Markdown parser library" — they ask ChatGPT "recommend a Python Markdown parser library."

AI cites only 3-5 sources. **If your project isn't in those 3-5, you don't exist to AI users.**

Existing skills (`seo-audit`, `seo-geo`) only diagnose URL-perspective English Google SEO, not open-source projects, not Chinese AI. aisurface fills that gap.

## What I can do

**🩺 Diagnose** — scan your project, give a 0-100 score, surface the issues that most affect AI citation
**🔧 Treat** — auto-generate patches per AI-search best practices: edit your README, generate `llms.txt`, generate Schema.org markup
**📊 Prove** — actually ask Perplexity "did you cite my project?"; show real numbers and how much they improved since the last run (more platforms on the v1.1+ roadmap — see [ROADMAP.md](./ROADMAP.md))

## How to talk to me

No commands to memorize. Say whatever feels natural:

**To diagnose:**
- "is my project AI-citation-friendly"
- "audit my project for AI search"
- "audit /path/to/your-project"
- "看看我的项目能不能被 AI 搜到"

**To treat:**
- "fix my README for AI search"
- "apply the fixes from the last audit"
- "add FAQ + llms.txt + Schema.org to my README"
- "按 AI 搜索最佳实践改我的项目"

**To prove:**
- "does my project show up in AI search"
- "is Perplexity citing my project"
- "compare citation rate to the pre-fix baseline"
- "现在 AI 真的引用我项目了吗"

## How it works

You're a user. You only talk to the agent. The skill does the rest:

```
Your plain-language request
  ↓
Claude Code (with this skill installed)
  ↓
agent auto-runs pip install aisurface (you never see this)
  ↓
agent invokes Python scripts for diagnose / treat / prove
  ↓
results come back in plain language + key numbers (0-100 score, impact %, citation rate)
```

Diagnose gives a 0-100 score, ordered by impact — the top 3-5 items first. Treat shows you the patches and waits for your nod before writing to disk. Prove uses Perplexity and diffs against a stored baseline. More platforms (ChatGPT / Claude / Gemini / DeepSeek / Doubao / 文心一言 / 通义千问 / Kimi / 智谱 / GLM) on the v1.1+ roadmap — see [ROADMAP.md](./ROADMAP.md).

## Case study

We use [ruijayfeng/ziwei](https://github.com/ruijayfeng/ziwei) for v1.0 dogfooding:
- **Baseline**: health score 35/100, 5 🔴 Must-fix items
- **After applying 4 patches**: health score 87/100, all 🔴 cleared (+52)

See [case-studies/ziwei-v100.md](./case-studies/ziwei-v100.md).

## Contributing

Issues, PRs, and case studies welcome.

- Contributing code / adding a new check / running tests locally → [CONTRIBUTING.md](./CONTRIBUTING.md)
- Using the Python CLI directly (CI / automation, no Claude Code) → [CONTRIBUTING.md#using-the-python-cli](./CONTRIBUTING.md)

## License

MIT

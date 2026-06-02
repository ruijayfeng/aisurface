---
name: aisurface
description: Use when the user wants to make their open-source project surface in AI search results. Triggers on: "audit my repo for AI search", "GEO audit", "make my project AI-citation-friendly", "is my project cited by ChatGPT/Perplexity/DeepSeek". Provides 3 verbs — `aisurface audit` (12-check report), `aisurface fix` (auto-apply patches for must-fix items), `aisurface verify` (probe AI platforms for citation rate). Standalone CLI; no Claude required at runtime.
---

# aisurface

Make your open-source project surface in AI search results. Three verbs.

```bash
aisurface audit ./         # diagnose
aisurface fix ./           # treat
aisurface verify ./        # prove
```

## audit — diagnose

Run the 12-check GEO audit:

```bash
aisurface audit .
```

Flags: `--learn` (teacher mode), `--json`, `--no-color`.

## fix — treat

Generate and apply patches for the 4 highest-impact must-fix items:
- FAQ section injection (templated 8 Q&A)
- When-to-use / When-NOT-to-use sections
- `.well-known/llms.txt` (per llmstxt.org)
- `index.schema.json` (SoftwareApplication + FAQPage)

```bash
aisurface fix .                       # interactive review + apply
aisurface fix . --dry-run             # preview only
aisurface fix . --yes                 # apply all without prompting
aisurface fix . --only=faq,llms_txt   # specific patch types only
```

## verify — prove

Probe AI platforms to measure citation rate before/after:

```bash
export PERPLEXITY_API_KEY=...
aisurface verify .                    # first run = baseline
aisurface fix .                       # apply fixes
aisurface verify .                    # measures lift vs baseline
```

Flags: `--platforms=perplexity[,deepseek]`, `--baseline`, `--queries-file`.

## Requirements

- Python 3.10+
- For `verify`: `PERPLEXITY_API_KEY` env var (Perplexity API key from https://perplexity.ai/account/api)
- No API key needed for `audit` or `fix` (offline heuristics)

## What it does NOT do

- Does not modify files without `--yes` or interactive confirmation (in `fix`)
- Does not call real LLMs by default (semantic checks use offline heuristics)
- Does not target non-OSS projects (URLs, marketing sites)

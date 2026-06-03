# references/
> L2 | Parent: /CLAUDE.md

## Member List
- `ai-search-platforms.md`: List of 11 AI search platforms aisurface tracks (ChatGPT, Perplexity, Claude, Gemini, 豆包, DeepSeek, 文心一言, 通义千问, Kimi, 智谱, GLM) plus per-platform citation characteristics. Loaded when the user names a specific platform.
- `schema-templates.md`: Schema.org JSON-LD templates (SoftwareApplication, FAQPage). Loaded when the user asks about structured data / schema markup.
- `citation-patterns.md`: What makes AI cite vs ignore content. Loaded when the user asks "why doesn't AI cite me" or wants README rewrite guidance.
- `llms-txt-spec.md`: The llmstxt.org specification. Loaded when the user asks about llms.txt or wants to generate one.
- `readme-checklist.md`: 12-item GEO README checklist. Loaded when the user wants README optimization guidance.

## Invariants
- These are knowledge-base files, loaded on demand by the skill's agent (not auto-loaded).
- No file in this directory should be longer than 300 lines without an internal table of contents (per the GEB progressive-disclosure rule).
- The trigger-eval table in the root `SKILL.md` ("何时加载 references/") is the single source of truth for which file is read when.

## Rule
Add a new reference file only when the SKILL.md gains a new trigger phrase that needs deeper knowledge than fits in the body.

[PROTOCOL]: Update this header when a reference is added, removed, or its loading trigger changes.

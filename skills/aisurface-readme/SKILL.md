---
name: aisurface-readme
description: Use when the user wants to optimize an open-source project's README for AI-search citation. Triggers on: "optimize my README for AI", "rewrite README for GEO", "make README AI-citation-friendly", "improve README for ChatGPT/Perplexity/Doubao citation". Reads the existing README, applies the GEO checklist (problem statement, FAQ, when-to-use, code examples, originality), and outputs a rewritten README. Standalone — does not require `aisurface@audit` to run first.
---

# aisurface@readme

Optimize an open-source project's README for AI-search citation.

## How to use

1. Point the agent at a project directory: "Optimize the README in `~/code/my-proj`"
2. The agent reads the existing README, applies the GEO README checklist (see `references/readme-checklist.md`), and proposes a rewrite.
3. User reviews the proposed rewrite, accepts or iterates.

## What it does

- Strengthens the **problem statement** (3-sentence hook in the first paragraph)
- Adds a **FAQ section** with 8-12 common Q&A pairs
- Adds **when to use / when not to use** boundaries
- Consolidates **code examples** into a clear "Examples" section
- Adds **comparison** with alternatives (if missing)
- Tightens **language** for AI-citation-friendliness (declarative, specific, fact-rich)

## What it does NOT do

- Does NOT modify the README without user review
- Does NOT add Schema.org markup (use `aisurface@schema` — v0.2)
- Does NOT generate llms.txt (use `aisurface@llms-txt`)

## Output format

A complete proposed README as a Markdown code block, followed by a brief changelog:

```
## Proposed README
<full markdown content>

## Change summary
- Added: FAQ section (8 Q&A)
- Strengthened: Problem statement (1st paragraph)
- Added: "When to use" section
- Consolidated: Code examples into "Examples" section
```

## References

- `references/readme-checklist.md` — the 12-item GEO README checklist
- `references/citation-patterns.md` — what makes AI cite vs ignore content

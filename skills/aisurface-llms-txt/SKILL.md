---
name: aisurface-llms-txt
description: Use when the user wants to add a `.well-known/llms.txt` file to their open-source project. Triggers on: "add llms.txt", "create llms.txt for my project", "generate .well-known/llms.txt", "AI crawler index file", "llms.txt per spec". Reads the project (README, package.json/pyproject.toml, docs/ structure), generates a valid llms.txt per https://llmstxt.org, and writes it to `<repo>/.well-known/llms.txt`. Validates the output before writing. Standalone.
---

# aisurface@llms-txt

Generate a valid `.well-known/llms.txt` for an open-source project.

## What is llms.txt?

A 2024 standard (proposed by Jeremy Howard) that AI crawlers check before indexing a site. Lists LLM-friendly info: project name, description, key URLs, optional details.

Spec: https://llmstxt.org

## How to use

1. Point the agent at a project: "Add llms.txt to `~/code/my-proj`"
2. The agent reads the project (README, manifests, docs) and infers the right content.
3. Writes to `<repo>/.well-known/llms.txt` (creates `.well-known/` if missing).
4. Validates the output.

## Programmatic use

```python
from pathlib import Path
from scripts.llms_txt import write_llms_txt

write_llms_txt(
    Path("~/code/my-proj"),
    project_name="my-proj",
    description="A test project for llms.txt generation",
    sections=[
        {"title": "Docs", "links": [{"url": "/docs/", "title": "Documentation"}]},
        {"title": "Optional", "links": [{"url": "/blog/", "title": "Blog"}]},
    ],
    details={"Language": "Python", "License": "MIT"},
)
```

## What it does NOT do

- Does NOT modify any other files
- Does NOT add Schema.org markup (use `aisurface@schema` — v0.2)

## References

- `references/llms-txt-spec.md` — the llms.txt spec
- `references/ai-search-platforms.md` — which AI platforms check llms.txt

"""
 * [INPUT]: Depends on `subprocess` (stdlib, shells out to `gh` CLI), `scripts.report.CheckResult`.
 * [OUTPUT]: Provides `github_topics_count(repo_root) -> int`, `github_repo_description(repo_root) -> str | None`, and a CheckResult for check #7.
 * [POS]: GitHub-specific data source. Used by `audit.run_audit` to score check #7 (GitHub topics count). Skipped (returns CheckResult with `skipped=True`) if `gh` CLI is unavailable.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""

"""Suggest GitHub topics and evaluate repo descriptions."""
from __future__ import annotations

import re

# Curated topic → keyword mappings
TOPIC_SUGGESTIONS: dict[str, list[str]] = {
    "python": ["python", "py", "pytest", "django", "flask", "fastapi"],
    "javascript": ["javascript", "js", "node", "nodejs", "npm"],
    "typescript": ["typescript", "ts", "tsx"],
    "react": ["react", "reactjs", "nextjs", "next.js"],
    "vue": ["vue", "vuejs", "nuxt"],
    "rust": ["rust", "cargo", "rustlang"],
    "go": ["golang"],
    "cli": ["cli", "command-line", "commandline", "terminal"],
    "api": ["api", "rest", "graphql", "endpoint"],
    "markdown": ["markdown", "md", "commonmark"],
    "documentation": ["docs", "documentation", "wiki"],
    "ai": ["ai", "llm", "gpt", "claude", "openai", "anthropic"],
    "rag": ["rag", "retrieval", "embedding", "vector"],
    "search": ["search", "elasticsearch", "fulltext"],
    "database": ["database", "sql", "nosql", "postgres", "mysql"],
    "devops": ["devops", "kubernetes", "docker", "ci-cd"],
    "testing": ["test", "testing", "e2e", "playwright"],
}


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z][a-z0-9.+#-]{1,30}", text.lower()))


def suggest_topics(readme_text: str, existing: list[str]) -> list[str]:
    """Return up to 12 topic suggestions not in `existing`.

    Algorithm: tokenize readme, match against TOPIC_SUGGESTIONS keys
    and per-topic keywords, dedupe, cap at 12.
    """
    tokens = _tokenize(readme_text)
    existing_set = {t.lower() for t in existing}
    suggested: list[str] = []
    for topic, keywords in TOPIC_SUGGESTIONS.items():
        if topic.lower() in existing_set:
            continue
        for kw in keywords:
            if kw.lower() in tokens:
                if topic not in suggested:
                    suggested.append(topic)
                break
    return suggested[:12]


def evaluate_description(desc: str) -> tuple[int, str]:
    """Score 0-10 a GitHub repo description. Returns (score, notes)."""
    desc = desc.strip()
    issues: list[str] = []
    score = 10

    if len(desc) < 20:
        issues.append("description too short (<20 chars)")
        score -= 4
    elif len(desc) > 200:
        issues.append("description too long (>200 chars, gets truncated)")
        score -= 2
    else:
        issues.append("length: good")

    # Check for vagueness
    vague_words = {"tool", "thing", "stuff", "best", "amazing", "awesome", "ultimate"}
    words = set(re.findall(r"\w+", desc.lower()))
    vague_hits = vague_words & words
    if len(vague_hits) >= 2:
        issues.append(f"vague words used: {vague_hits}")
        score -= 3

    # Penalty for superlative marketing words
    superlatives = {"best", "amazing", "awesome", "ultimate"}
    if words & superlatives:
        score -= 1

    notes = "OK" if not issues else "; ".join(issues)
    return max(0, min(10, score)), notes

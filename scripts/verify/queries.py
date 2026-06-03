"""
 * [INPUT]: Depends on `scripts.scanner.RepoAssets` (project_type, project_name, description). No network.
 * [OUTPUT]: Provides `generate_queries(assets, *, n=10) -> list[str]`. Returns a list of natural-language AI-search queries an actual user would type to discover a project of this type — e.g., "best Python CLI for X" for a python-cli project, "what is a GEO audit tool" for a python-lib named aisurface. Deterministic (seeded by project name) so reruns are comparable.
 * [POS]: Query generator. Imported by `verify.cmd_verify`. The 10 (default) queries are sent to every platform in the probe; baseline diff is computed over the same query set per run.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""

"""Generate representative AI-search queries for a project."""
from __future__ import annotations

from pathlib import Path

_TEMPLATES = {
    "python-library": [
        "best Python library for {topic}",
        "{name} vs alternatives",
        "how to use {name} in Python",
        "is {name} production-ready",
        "{topic} Python package recommendations",
        "open source {topic} library",
        "{name} tutorial",
        "{name} examples",
        "{topic} Python library 2026",
        "{name} documentation",
    ],
    "web-app": [
        "best open source {topic} web app",
        "{name} self-hosted",
        "{name} alternatives",
        "{topic} web tool",
        "open source {topic}",
        "{name} demo",
        "{topic} app recommendations",
        "{name} tutorial",
        "free {topic} tool",
        "{name} documentation",
    ],
    "cli-tool": [
        "best CLI for {topic}",
        "{name} vs alternatives",
        "{topic} command line tool",
        "{name} installation",
        "{name} usage examples",
        "open source {topic} CLI",
        "{name} tutorial",
        "{topic} terminal tool",
        "{name} configuration",
        "{name} GitHub",
    ],
    "generic": [
        "best open source {topic}",
        "{name} alternatives",
        "{topic} tool recommendations",
        "{name} tutorial",
        "{name} documentation",
        "how to use {name}",
        "is {name} good",
        "{topic} GitHub project",
        "{name} examples",
        "open source {topic} 2026",
    ],
}


def generate_queries(project_name: str, description: str, project_type: str, count: int = 10) -> list[str]:
    """Generate `count` representative queries.

    `topic` is derived from the description (first 3-5 keywords, lowercased).
    """
    topic = _extract_topic(description) or project_name
    templates = _TEMPLATES.get(project_type, _TEMPLATES["generic"])
    queries = [t.format(name=project_name, topic=topic) for t in templates]
    return queries[:count]


def load_queries_from_file(path: Path) -> list[str]:
    """One query per line, blank lines and lines starting with # ignored."""
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]


def _extract_topic(description: str) -> str:
    """Cheap topic extraction: first 3-5 content words from the description."""
    words = [w for w in description.split() if w.isalpha() and len(w) > 2]
    return " ".join(words[:5]).lower()

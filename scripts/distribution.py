"""Evaluate distribution signals (awesome-lists, npm, PyPI, stars)."""
from __future__ import annotations

from typing import TypedDict

# Curated list of awesome-* repos by category, for the user to consider submitting to
AWESOME_LISTS = [
    "https://github.com/sindresorhus/awesome",
    "https://github.com/awesome-python/awesome-python",
    "https://github.com/awesome-javascript/awesome-javascript",
    "https://github.com/ripienaar/free-for-dev",
    "https://github.com/topics/awesome-list",
]


class CheckResult(TypedDict):
    score: int
    notes: str
    recommended_actions: list[str]


def check_signals(
    project_name: str,
    description: str,
    github_stars: int,
    has_npm: bool,
    has_pypi: bool,
) -> CheckResult:
    """Score 0-10 the project's distribution signals."""
    score = 0
    actions: list[str] = []
    notes: list[str] = []

    # Stars contribution (max 5)
    if github_stars >= 10000:
        score += 5
    elif github_stars >= 1000:
        score += 4
    elif github_stars >= 100:
        score += 2
    elif github_stars >= 10:
        score += 1
    else:
        notes.append("low stars (<10)")

    # Package registries (max 3)
    registry_count = int(has_npm) + int(has_pypi)
    score += registry_count + (1 if registry_count > 0 else 0)
    if registry_count == 0:
        actions.append("Publish to a package registry (npm or PyPI)")

    # Description quality heuristic (max 2)
    desc_lower = description.lower()
    if len(description) >= 50 and ("open-source" in desc_lower or "self-host" in desc_lower):
        score += 2
    elif len(description) >= 30:
        score += 1
    else:
        actions.append("Improve GitHub description (longer, more specific)")

    if score < 6:
        actions.append(f"Consider submitting {project_name} to awesome lists (e.g. {AWESOME_LISTS[0]})")

    return CheckResult(
        score=min(10, score),
        notes="; ".join(notes) if notes else "OK",
        recommended_actions=actions,
    )

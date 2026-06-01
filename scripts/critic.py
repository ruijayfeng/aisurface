"""LLM-based GEO critic with offline fallback for v0.1.

The offline critic uses simple heuristics. A future version (v0.3) can
swap in a real LLM call via `critique_with_llm()`.
"""
from __future__ import annotations

import json
import re

CRITIC_PROMPT_TEMPLATE = """You are an AI search engine. You are considering whether to cite a
README in response to a user query about "{topic}".

The user query is: "{representative_query}"

Here is the README:
{readme}

Answer the following in JSON:
1. "would_cite": "yes" | "no" | "unsure"
2. "problem_clarity": 0-10
3. "has_faq": 0-10
4. "has_code_examples": 0-10
5. "has_when_to_use": 0-10
6. "summary": one-sentence rationale
"""


def offline_critique(readme_text: str, topic: str) -> dict:
    """Heuristic-based fallback when no LLM is configured.

    Returns dict with keys: problem_clarity, has_faq, has_code_examples,
    has_when_to_use, would_cite, summary.
    """
    text = readme_text.lower()

    # Problem clarity: longer first paragraph + first 30 chars not too generic
    first_para = readme_text.split("\n\n", 1)[1] if "\n\n" in readme_text else readme_text
    first_para = first_para[:300]
    problem_clarity = 5
    if len(first_para) > 80:
        problem_clarity += 2
    if any(kw in first_para.lower() for kw in ["tired of", "struggle", "automate", "fast", "simple"]):
        problem_clarity += 2
    if any(kw in first_para.lower() for kw in ["best", "ultimate", "amazing"]) and len(first_para) < 60:
        problem_clarity -= 2
    problem_clarity = max(0, min(10, problem_clarity))

    # FAQ
    has_faq = 0
    if "## faq" in text or "### faq" in text or "frequently asked" in text:
        has_faq = 9
    elif re.search(r"\?.*\n.*answer", text):
        has_faq = 6

    # Code examples
    has_code_examples = 0
    code_block_count = text.count("```")
    if code_block_count >= 4:
        has_code_examples = 9
    elif code_block_count >= 2:
        has_code_examples = 8
    elif "install" in text and ("pip install" in text or "npm install" in text):
        has_code_examples = 4

    # When to use
    has_when_to_use = 0
    if "when to use" in text or "use cases" in text or "when not to use" in text:
        has_when_to_use = 8
    elif "features" in text or "highlights" in text:
        has_when_to_use = 5

    # Would cite? composite
    composite = (problem_clarity + has_faq + has_code_examples + has_when_to_use) / 4
    if composite >= 7:
        would_cite = "yes"
    elif composite >= 4:
        would_cite = "unsure"
    else:
        would_cite = "no"

    return {
        "would_cite": would_cite,
        "problem_clarity": problem_clarity,
        "has_faq": has_faq,
        "has_code_examples": has_code_examples,
        "has_when_to_use": has_when_to_use,
        "summary": f"Offline heuristic: composite {composite:.1f}/10",
    }


def parse_critique_response(raw: str) -> dict:
    """Parse a JSON critique response, stripping markdown fences if present."""
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE)
    return json.loads(text)


def build_critic_prompt(readme: str, topic: str, representative_query: str) -> str:
    """Build the LLM critic prompt (for v0.3 real-LLM implementation)."""
    return CRITIC_PROMPT_TEMPLATE.format(
        topic=topic,
        representative_query=representative_query,
        readme=readme,
    )

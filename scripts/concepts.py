"""
 * [INPUT]: Depends on stdlib only.
 * [OUTPUT]: Provides `PRIMERS: dict[int, str]` (12 check-id → 1-2 sentence primer), `get_primer(check_id) -> str`.
 * [POS]: Knowledge layer for `--learn` teacher mode. Imported lazily by `report._format_check_line` only when `teacher_mode=True`.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""

"""Short educational primers for the 12 GEO checks, used by --learn teacher mode.

Each primer is 1-2 sentences: factual, terse, educational. Not marketing copy.
"""
from __future__ import annotations

PRIMERS: dict[int, str] = {
    1: "AI search engines decide whether to cite a README largely from the first "
       "paragraph: does it state the problem in concrete terms? Generic intros like "
       "'A tool for X' underperform specific ones like 'Tired of manually doing X? "
       "This automates it in 3 lines.'",

    2: "FAQ sections answer the specific questions users actually ask AI ('how do I "
       "deploy it', 'is it free', 'how does it compare to Y'). AI uses these Q&A "
       "pairs as direct citation targets, so a strong FAQ translates to direct "
       "citation snippets.",

    3: "A 'When to use / When NOT to use' section is a citation magnet because AI "
       "often answers 'should I use this for X' questions. The honest 'not for X' "
       "half is what makes the recommendation trustworthy to the model.",

    4: "Runnable code examples let AI quote your project verbatim in 'how do I get "
       "started' answers. Fenced code blocks (```bash, ```python) are high-signal: "
       "they're the most copy-pasted format in AI responses.",

    5: "Schema.org JSON-LD is structured data that AI search engines read directly "
       "to understand what your project IS. Without it, AI has to guess from prose; "
       "with it, you declare `SoftwareApplication`, `name`, `url`, `author` explicitly.",

    6: "`.well-known/llms.txt` is a proposed standard (llmstxt.org) where LLMs look "
       "first when assessing a project. It lists your project's structure, key docs, "
       "and optional citation guidance in a single LLM-friendly Markdown file.",

    7: "GitHub topics are how AI categorizes your project alongside peers. 8-12 "
       "topics gives the model enough signal to match you to relevant queries "
       "without looking spammy; fewer than 4 leaves categorization ambiguous.",

    8: "The GitHub repo description is the first line an AI sees in search snippets "
       "and 'about' panels. Vague descriptions ('a tool for X') lose to specific "
       "ones ('Python CLI that parses Markdown to HTML in 1 line').",

    9: "A `docs/faq.md` page is the canonical place AI looks when a user query "
       "matches your project's domain. It supplements the README FAQ with deeper, "
       "longer-form answers, increasing the chance your doc is cited over a competitor's.",

    10: "A `docs/comparison.md` or 'alternatives' page directly answers the most "
        "common AI query in any category: 'X vs Y, which should I use?'. Without "
        "it, AI cites someone else's comparison; with it, the model cites yours.",

    11: "Distribution signals (awesome-list inclusion, npm/PyPI publish, GitHub "
        "stars) are authority proxies. AI uses them as tiebreakers between two "
        "otherwise-equal projects: the one with broader distribution wins the citation.",

    12: "Original citable content — your own research data, benchmarks, methodology "
        "writeups — is the highest-leverage GEO asset. Other projects can copy your "
        "structure, but they cannot copy your original findings, so AI cites you as "
        "the primary source.",
}


def get_primer(check_id: int) -> str:
    """Return the teacher-mode primer for `check_id`, or empty string if unknown."""
    return PRIMERS.get(check_id, "")

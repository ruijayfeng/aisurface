<!--
[INPUT]: none (standalone content draft)
[OUTPUT]: Show HN post draft (title + body + posting notes)
[POS]: docs/launch/'s HN draft, consumed by manual posting to news.ycombinator.com
[PROTOCOL]: Update this header when changed
-->

---
task: 25
target: Hacker News (Show HN)
status: draft
date: 2026-06-02
notes: Real case-study numbers (35→66, ~30 min) replace plan's aspirational 42→92 / 4 hours
---

# Show HN Post — aisurface v0.1.0

## Title (70 chars, copy exactly)

```
Show: aisurface – make your open-source project surface in AI search
```

(70 characters with the en-dash; HN accepts up to 80.)

## URL field

```
https://github.com/ruijayfeng/aisurface
```

## Body (copy-paste verbatim)

```
Hi HN,

I built aisurface, a Claude Code skill collection that helps OSS maintainers make their projects cite-worthy by AI search (ChatGPT, Perplexity, Doubao, DeepSeek, Claude, etc.).

Why this matters: when users ask AI "what's a good Python Markdown parser", the AI cites 3-5 sources. If your project isn't in that set, it doesn't exist for AI users. Most OSS maintainers don't know how to optimize for AI citation.

What makes it different from existing SEO skills:
- Local repo (not URL)
- Open-source focused (any kind of project)
- Chinese AI platforms prioritized (Doubao, DeepSeek are the new search giants)
- 12-check audit with teacher mode for GEO newcomers
- v0.1 ships with 3 skills: audit, readme optimizer, llms.txt generator

I dogfooded it on my own 343-star project (ruijayfeng/ziwei, a React 19 + TypeScript Zi Wei Dou Shu web app). After running the audit and applying the must-fix list, the GEO health score went from 35/100 to 66/100 in roughly 30 minutes of work (audit + adding 5 files: schema.json, llms.txt, README FAQ, when-to-use section, and an original research/methodology page). Case study with before/after reports is in the repo.

GitHub: https://github.com/ruijayfeng/aisurface
Install: npx skills add ruijayfeng/aisurface@audit

Happy to answer questions. Looking for feedback on:
1. The 12-check audit — what should be added/removed?
2. The teacher mode (--learn flag) — is it actually useful for newcomers?
3. Roadmap to v0.3 (real AI API probes) — what platforms matter most to you?
```

## Posting notes

### When to post

- **Best window:** weekday 8-10am US Eastern (HN peak hours, ~14:00-16:00 UTC during DST).
- **Best days:** Tuesday, Wednesday, Thursday (avoid Monday morning and Friday afternoon).
- **Avoid:** weekends, US federal holidays, days of major industry news (Google I/O, Apple WWDC week, etc.).

### First 2 hours response strategy

- Respond to **every** comment within 30 minutes. HN's front-page window is 2 hours; engagement velocity is the single biggest predictor of landing the front page.
- Have a short URL shortener or direct permalinks ready for follow-ups (case study, specific checks, etc.).
- If a comment points at a real flaw, **acknowledge it openly** and link the GitHub issue you open. HN rewards honesty and iteration.
- Do NOT defend every critique. Some are correct. "Good catch — opened issue #N" reads better than "actually you're wrong because...".

### Cross-posting

After the HN post is live, cross-post a **shorter version** to:

- **r/programming** (https://www.reddit.com/r/programming/) — same body, no questions, more humble tone ("Happy to answer questions" -> "Would love feedback").
- **r/MachineLearning** (https://www.reddit.com/r/MachineLearning/) — lead with the AI-citation angle, mention GEO explicitly.

Add a `// cross-posted to HN` note in the Reddit body so Reddit users don't flame you for self-promotion.

### Tone guardrails

- **Do NOT** name competing skills (`seo-geo`, `ai-seo`, `seo-audit`) in the body. The current draft only says "existing SEO skills" generically — keep it that way. If a commenter brings them up, engage honestly but don't initiate.
- **Do NOT** mention the project's Chinese audience in the HN post itself; that detail is for the 即刻 / 掘金 posts. HN is English-only.
- **Do NOT** add emojis to the HN body. HN's house style is plain text.
- **Do** lead with the user-facing problem ("your project doesn't exist to AI users"), not the implementation story.

### Pre-flight checklist (verify before clicking submit)

- [ ] GitHub repo `https://github.com/ruijayfeng/aisurface` resolves and shows the v0.1.0 tag
- [ ] `npx skills add ruijayfeng/aisurface@audit` works (skills.sh indexed)
- [ ] Case study link resolves: `https://github.com/ruijayfeng/aisurface/blob/main/case-studies/ziwei-before-after.md`
- [ ] Real numbers in this draft (35→66, ~30 min) match the case-study file — do not regenerate with aspirational numbers
- [ ] Title is exactly 70 chars, no trailing whitespace

### Post-flight (next 48 hours)

- Keep responding to comments for at least 48 hours, even after the post falls off the front page.
- Triage every "I tried it and..." comment into a GitHub issue (with credit and `from-hn` label).
- Collect any "you missed check #13" feedback for the v0.2 audit checklist.

<!--
[INPUT]: show-hn.md, jike.md, juejin.md, twitter.md, recruit-dm.md (5 sibling launch drafts)
[OUTPUT]: Index page for docs/launch/ with posting-order recommendation
[POS]: docs/launch/'s navigation root, consumed by Boss during launch week
[PROTOCOL]: Update this header when changed
-->

---
status: live
date: 2026-06-02
scope: v0.1.0 launch week (W6)
---

# docs/launch/ — aisurface v0.1.0 Launch Materials

This directory holds **copy-paste-ready drafts** for the v0.1.0 public launch. Every file is a draft; nothing here auto-posts. Boss (the human) reviews, edits if needed, and posts manually with their own accounts on each platform.

## Member list

| File | Platform | Format | Status |
|---|---|---|---|
| `show-hn.md` | Hacker News (Show HN) | Title + body + posting notes | draft |
| `jike.md` | 即刻 (Jike) | Chinese short post + timing | draft |
| `juejin.md` | 掘金 (Juejin) | Chinese long-form article (~2600 字) | draft |
| `twitter.md` | Twitter / X | English 6-tweet thread + char counts | draft |
| `recruit-dm.md` | GitHub / email / Twitter DM | Cold outreach template + candidate playbook | draft |

## Posting order (recommended for launch week)

The order matters: warm up English-speaking low-friction channels first, hit Chinese platforms in their peak, then drop the big HN post on a US weekday morning, then start the slow recruit-DM campaign.

### Day 1 (Tuesday, recommended)

- **Morning (9am US Eastern):** Post the **Twitter thread** (`twitter.md`). 6 tweets, low friction, broad reach, 2-hour engagement window before bed.
- **Evening (9pm China time, which is morning US Eastern next day):** Post **即刻** (`jike.md`) and **掘金** (`juejin.md`). Capture the Chinese audience on their commute / before-sleep window.

### Day 2 (Wednesday)

- **Morning (8-10am US Eastern):** Post the **Show HN** (`show-hn.md`). HN peak hours, front-page window is 2 hours — keep the laptop open and respond to every comment within 30 min.
- **After HN is up:** Cross-post shorter versions to r/programming and r/MachineLearning (instructions in `show-hn.md`).

### Days 2-7

- **Send 50 recruit DMs** (`recruit-dm.md`). 10-15 per day, Tuesday-Thursday only, 9-11am in the *maintainer's* timezone (not yours). Track in `recruit-pipeline.md` (create that file the first day of the campaign).
- **Daily:** Respond to every comment, issue, and DM that comes in from any of the above channels. First-day response velocity is the strongest signal of launch health.

### Day 8+

- **Triage:** If 3-5 maintainers shared before/after, draft case-study PRs.
- **Iterate:** Update `references/ai-search-platforms.md` if any new platform appeared in the wild (Task 29).
- **Optional:** Post a "Launch week retrospective" on the aisurface GitHub Discussions.

## Why this order

1. **Twitter first** because it's a non-front-page platform — the worst case is silence, not public failure. It warms up your socials and lets you debug any issues with the link / npx commands before HN sees them.
2. **即刻 + 掘金 second** because they target a different audience (Chinese AI users) and have their own peak hours. They don't compete with HN for attention.
3. **Show HN last in the wave** because HN is the highest-leverage channel with the highest cost of failure (a bad first impression on the front page is permanent). You want all the kinks ironed out before the HN post.
4. **Recruit DMs slow and steady** because the conversion funnel is leaky (20-30% response, 6-10% case-study). Spreading the sends over a week gives you time to iterate the template based on early responses.

## Number discipline

All drafts use the **real case-study numbers** from `case-studies/ziwei-before-after.md`:

- **Before:** 35 / 100
- **After:** 66 / 100
- **Time:** ~30 minutes
- **Project:** ruijayfeng/ziwei (343 stars, React 19 + TypeScript, Zi Wei Dou Shu web app)

The plan file at `D:\Code\MyProject\SkillsCreate\InitSkill\docs\superpowers\plans\2026-06-01-aisurface.md` used aspirational numbers (42→92, 4 hours) in early drafts. **Do not regenerate** with the aspirational numbers; the case-study file is the source of truth.

## Cross-references

- **Source spec:** [`docs/superpowers/specs/2026-06-01-aisurface-design.md`](../../../../SkillsCreate/InitSkill/docs/superpowers/specs/2026-06-01-aisurface-design.md)
- **Source plan:** [`docs/superpowers/plans/2026-06-01-aisurface.md`](../../../../SkillsCreate/InitSkill/docs/superpowers/plans/2026-06-01-aisurface.md) (lines 2995-3125)
- **Case study:** [`case-studies/ziwei-before-after.md`](../../case-studies/ziwei-before-after.md)
- **Release handoff:** [`RELEASE_HANDOFF.md`](../../RELEASE_HANDOFF.md)

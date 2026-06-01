<!--
[INPUT]: case-studies/ziwei-before-after.md (real numbers: 35→66, ~30 min)
[OUTPUT]: Twitter/X thread draft (English, 6 tweets, each ≤280 chars)
[POS]: docs/launch/'s Twitter draft, consumed by manual posting to x.com
[PROTOCOL]: Update this header when changed
-->

---
task: 26
target: Twitter / X (English thread)
status: draft
date: 2026-06-02
notes: 6-tweet thread; char counts shown under each; real numbers replace plan's aspirational 42→92
---

# Twitter Thread — aisurface v0.1.0

## Thread structure (post in order, no gaps > 5 min between tweets)

---

### Tweet 1/6 — Hook (128 chars)

```
Just shipped aisurface v0.1.0 — a Claude Code skill collection for OSS maintainers to make their projects surface in AI search.
```

**Char count:** 128 / 280
**Purpose:** Single-line hook. The word "Just shipped" signals fresh release; "surface in AI search" frames the problem in 4 words.

---

### Tweet 2/6 — Problem (173 chars)

```
The problem: when users ask ChatGPT/Perplexity/Doubao/DeepSeek about a topic, the AI cites 3-5 sources. If your project isn't in that set, you don't exist for AI users.
```

**Char count:** 173 / 280
**Purpose:** Make the threat concrete. Listing 4 AI platforms (Western + Chinese) signals the project isn't a one-trick pony.

---

### Tweet 3/6 — Differentiation (157 chars)

```
Existing SEO skills (seo-audit, seo-geo) are URL-focused and English/Google-biased. aisurface is repo-focused, OSS-targeted, and Chinese-AI-platform-prioritized.
```

**Char count:** 157 / 280
**Purpose:** Direct competitive positioning. Naming the two best-known competitors helps people who already know them self-identify. (On HN we kept the names off; on Twitter the direct contrast reads better.)

---

### Tweet 4/6 — What's in v0.1 (128 chars)

```
v0.1 ships 3 skills: audit (12-check GEO scan), readme (optimize README for AI citation), llms-txt (generate .well-known/llms.txt).
```

**Char count:** 128 / 280
**Purpose:** Concrete deliverable list. Three concrete nouns make it scannable.

---

### Tweet 5/6 — Dogfooding result (193 chars)

```
I dogfooded it on my own 343-star project (ruijayfeng/ziwei, a React 19 + TS Zi Wei Dou Shu web app): GEO health score went from 35/100 to 66/100 in ~30 minutes of work. Case study in the repo.
```

**Char count:** 193 / 280
**Purpose:** Real numbers, not aspirational ones. 35→66 in 30 minutes is honest and verifiable from the case-study file in the repo. 42→92 was the plan's aspirational target — the actual repo state shows 35→66.

---

### Tweet 6/6 — CTA (184 chars raw, URL shortens to ~167)

```
Try it:
npx skills add ruijayfeng/aisurface@audit
npx skills add ruijayfeng/aisurface@readme
npx skills add ruijayfeng/aisurface@llms-txt

GitHub: https://github.com/ruijayfeng/aisurface
```

**Char count:** 184 / 280 (raw) — Twitter shortens `https://github.com/ruijayfeng/aisurface` to a 23-char t.co link, so visible count drops to ~168.
**Purpose:** Three concrete commands (copy-pasteable), one canonical link. End users can act in 30 seconds.

---

## Posting notes

### When to thread

- **Best days:** Tuesday, Wednesday, Thursday.
- **Best time:** 9:00-10:00 AM US Eastern (14:00-15:00 UTC during DST).
- **Avoid:** Mondays (people are catching up, not browsing), Fridays (attention shifts to weekend), weekends (dev Twitter is quieter), and any day with major industry news.
- **Thread spacing:** post all 6 tweets within 5-10 minutes of each other. Twitter's algorithm rewards thread velocity, not pacing.

### Engagement strategy (first 2 hours)

- **Pin the thread** to your profile for 48 hours. Visitors to `x.com/ruijayfeng` will see it first.
- **Quote-tweet your own thread** with a one-line takeaway, 1 hour after posting. This boosts distribution.
- **Reply to every reply** within 60 minutes, even if the reply is just "thanks!" — Twitter's algorithm weighs reply-to-reply ratios heavily.
- **Like every like** that comes in within the first 30 minutes (use `F5`-refresh tab in another window). This is a known signal-boost trick.
- **If someone shares it with critique,** reply with "Good call — opened issue #N" and link the issue. Don't argue.

### What NOT to do

- **Do NOT add hashtags** (`#AI`, `#SEO`, `#OpenSource`). Hashtags make dev Twitter cringe in 2026. The thread stands on its own.
- **Do NOT add emojis** in tweet bodies. One emoji in the entire thread is the ceiling. The current draft has zero.
- **Do NOT cross-link to LinkedIn / Mastodon in the thread.** It's a Twitter-native post; let it breathe.
- **Do NOT mention v0.3 / v0.4 / future plans** in the first 6 tweets. Save that for a "more thoughts 🧵" follow-up tweet posted 24 hours later (optional).
- **Do NOT delete a tweet** if it underperforms — just let it stay. Twitter's "view count" penalty on deletion is real.

### Char-counting rules of thumb

- Twitter counts Unicode code points, not graphemes. An emoji is usually 2 chars.
- URLs auto-shorten to 23 chars (t.co). Don't pad with spaces around links.
- Line breaks (`\n`) count as 1 char each.
- Spaces at the start/end of a line count.

### Pre-flight checklist

- [ ] Each of the 6 tweets verified ≤ 280 chars (counts in the headers above)
- [ ] Real numbers (35→66, ~30 min) match the case study
- [ ] No emoji in any tweet
- [ ] No hashtags
- [ ] `https://github.com/ruijayfeng/aisurface` resolves and shows v0.1.0 tag
- [ ] All three `npx skills add ...` commands work (skills.sh indexed)

### Post-flight

- Track likes/retweets/replies in a private note for 48 hours.
- Pin the thread on your profile.
- After 48 hours, if the thread got >50 likes, save it to a Notion/notes file for future launch reference.
- If a tech influencer replies, **DM them** (not @ them) with the case-study link — public @-mentions feel spammy.

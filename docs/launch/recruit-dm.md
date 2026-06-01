<!--
[INPUT]: case-studies/ziwei-before-after.md (real numbers: 35→66, ~30 min)
[OUTPUT]: Recruit DM template with placeholders + 3 filled examples + candidate-finding playbook
[POS]: docs/launch/'s recruit DM, consumed by manual cold outreach to OSS maintainers
[PROTOCOL]: Update this header when changed
-->

---
task: 27
target: GitHub Issues / Email / Twitter DMs (cold outreach)
status: draft
date: 2026-06-02
notes: 50 cold DMs target, 5-10 responses expected, 3-5 case studies goal
---

# Recruit DM Template — aisurface v0.1.0

## Master template (use placeholders, never send raw)

```
Hi {{maintainer_name}},

I built aisurface, a Claude Code skill for making OSS projects cite-worthy by AI search (ChatGPT, Perplexity, Doubao, DeepSeek, etc.). I dogfooded it on my own 343-star project and went from 35/100 to 66/100 in about 30 minutes of work.

Would you be open to trying it on {{project_name}}? It takes ~30 minutes:
1. npx skills add ruijayfeng/aisurface@audit
2. Run the audit on your repo
3. Apply the top 3 must-fixes
4. Share the before/after score

If you're willing, I'd love to feature your before/after as a case study in the aisurface README (with credit to {{project_name}} and a link to {{repo_url}}). No pressure either way — if you just run the audit and don't share results, that's fine too.

GitHub: https://github.com/ruijayfeng/aisurface

Thanks!
```

**Char count:** ~720 chars (well under Twitter DM 10K limit, under GitHub issue body 65K limit).

---

## 3 filled-in examples (use as reference, do not send these as-is)

### Example 1: Python lib (passive maintainer, hundreds of stars)

```
Hi David,

I built aisurface, a Claude Code skill for making OSS projects cite-worthy by AI search (ChatGPT, Perplexity, Doubao, DeepSeek, etc.). I dogfooded it on my own 343-star project and went from 35/100 to 66/100 in about 30 minutes of work.

Would you be open to trying it on httpie? It takes ~30 minutes:
1. npx skills add ruijayfeng/aisurface@audit
2. Run the audit on your repo
3. Apply the top 3 must-fixes
4. Share the before/after score

If you're willing, I'd love to feature your before/after as a case study in the aisurface README (with credit to httpie and a link to https://github.com/httpie/cli). No pressure either way — if you just run the audit and don't share results, that's fine too.

GitHub: https://github.com/ruijayfeng/aisurface

Thanks!
```

**Why this works:** David is the maintainer of httpie (a famous Python CLI for HTTP). He's passive — not actively pushing the project. The DM offers something (case-study exposure) without demanding time.

### Example 2: JS framework (active maintainer, growing)

```
Hi Sebastian,

I built aisurface, a Claude Code skill for making OSS projects cite-worthy by AI search (ChatGPT, Perplexity, Doubao, DeepSeek, etc.). I dogfooded it on my own 343-star project and went from 35/100 to 66/100 in about 30 minutes of work.

Would you be open to trying it on Astro? It takes ~30 minutes:
1. npx skills add ruijayfeng/aisurface@audit
2. Run the audit on your repo
3. Apply the top 3 must-fixes
4. Share the before/after score

If you're willing, I'd love to feature your before/after as a case study in the aisurface README (with credit to Astro and a link to https://github.com/withastro/astro). No pressure either way — if you just run the audit and don't share results, that's fine too.

GitHub: https://github.com/ruijayfeng/aisurface

Thanks!
```

**Why this works:** Sebastian runs Astro, a much larger project (~50K stars). The DM works because the offer is asymmetric: he spends 30 min, gets a free audit + README feature. Even a project that size benefits from AI-citation optimization.

### Example 3: Rust CLI (solo maintainer, niche tool)

```
Hi BurntSushi,

I built aisurface, a Claude Code skill for making OSS projects cite-worthy by AI search (ChatGPT, Perplexity, Doubao, DeepSeek, etc.). I dogfooded it on my own 343-star project and went from 35/100 to 66/100 in about 30 minutes of work.

Would you be open to trying it on ripgrep? It takes ~30 minutes:
1. npx skills add ruijayfeng/aisurface@audit
2. Run the audit on your repo
3. Apply the top 3 must-fixes
4. Share the before/after score

If you're willing, I'd love to feature your before/after as a case study in the aisurface README (with credit to ripgrep and a link to https://github.com/BurntSushi/ripgrep). No pressure either way — if you just run the audit and don't share results, that's fine too.

GitHub: https://github.com/ruijayfeng/aisurface

Thanks!
```

**Why this works:** BurntSushi is famously a maintainer-of-many (ripgrep, fd, tokei). He's a careful, technical reviewer. The DM signals "I did the homework" by citing real numbers and offering a low-friction ask. He'll either ignore it or try it — there's no in-between, which is fine.

---

## How to find candidates

### GitHub search queries (paste into https://github.com/search)

Use these to find OSS projects in the 50-500 star sweet spot — large enough to be referenced by AI, small enough that the maintainer will read your DM.

```
# Python libraries (broad)
language:python stars:50..500 pushed:>2026-01-01

# JavaScript/TypeScript frameworks
language:typescript stars:100..800 pushed:>2026-02-01

# Rust CLI tools
language:rust stars:50..300 pushed:>2026-01-01

# Go libraries
language:go stars:50..500 pushed:>2026-01-01

# Generic "AI search relevant" — projects with README + topics but no llms.txt
"awesome-" stars:100..1000 in:readme
```

### Filter further

After the search:

1. Open the top 20 results.
2. Check `https://github.com/{owner}/{repo}/.well-known/llms.txt` — if 404, they're a target.
3. Check the GitHub description — if vague ("a tool for X"), they're a target.
4. Check the README — if it lacks a FAQ section, they're a target.
5. Check `git log` — if last commit is within 6 months, the maintainer is active enough to respond.

### Where to find maintainer contact info

- **GitHub profile email:** `https://github.com/{username}.keys` (if public).
- **Twitter/X:** Most OSS maintainers link it on their profile.
- **Project README:** Look for a `Contact` / `Support` / `Discussions` section.
- **Discord/Slack:** Some projects have it; you can DM there.
- **GitHub Discussions:** Better than issues for cold outreach (less aggressive).

### Target mix (50 DMs total)

- **20 Python projects** (largest community, most likely to engage).
- **15 JavaScript/TypeScript projects** (high AI-search relevance).
- **10 Go projects** (server/infrastructure — prime AI-search users).
- **5 Rust projects** (smaller but very engaged maintainers).
- **Bonus 0-5 in any language** if you find good candidates outside the above.

### Diversity

- **Don't send 10 DMs to Python CLI tools in a row.** Mix CLI / lib / framework / docs.
- **Don't send 5 DMs to projects by the same org.** They might forward to each other; one response covers them.
- **Don't send DMs to projects you use daily** unless you disclose that — it'll feel like astroturfing.

---

## What to offer

The DM is the hook, but the offer is what closes. Make sure each DM leads with **three concrete things you're offering**:

1. **Free audit** — `npx skills add ruijayfeng/aisurface@audit` takes 5 minutes, no strings attached.
2. **Credit in README** — if they share before/after, you add a section to the aisurface README linking to their project. This is the highest-value trade.
3. **30-min consultation call** (optional) — for projects that want a deeper walkthrough, offer a video call. Calendar link in the follow-up DM, not the initial DM.

### What NOT to offer

- **Money.** It changes the dynamic from peer-collab to vendor-pitch, and you don't have budget.
- **"Backlink exchange."** Google devalues these; maintainers are rightly skeptical.
- **Free feature work on their project.** That's not your job scope; it confuses the ask.

---

## Response rate expectations

Be honest with yourself before sending — cold outreach ROI is brutal.

| Metric | Target | Notes |
|---|---|---|
| DMs sent | 50 | One batch per day, 10-15 per session, over 4 days. |
| Open rate (if email) | 60-70% | Subject line matters; with DM there's no open rate. |
| Response rate | **20-30%** | 10-15 out of 50 will reply, even if just to say "no thanks." |
| Willing to try | **10-20%** | 5-10 out of 50 will actually run the audit. |
| Share before/after | **6-10%** | 3-5 out of 50 will agree to a case study. |
| Featured in README | 3-5 | Goal for v0.2 cycle. |

### Why the funnel is so leaky

- 30-50% of DMs go to inactive maintainers (left the project, on sabbatical, no longer monitoring DMs).
- 20-30% will read but not reply (silence ≠ no).
- Of the 20-30% who reply, half say "thanks, will try later" and never do.
- Of the 10-20% who actually try, only the most engaged will write up before/after.

### How to improve response rate

- **Personalize the first sentence.** "Hi David" beats "Hi there" 3:1. Always use the real first name from their GitHub profile.
- **Mention their project by name.** "trying it on httpie" beats "trying it on your project" 5:1.
- **Send Tuesday-Thursday 9-11am in the maintainer's timezone** (not yours). If they're in Berlin, send at 9am Berlin time.
- **Follow up once after 5 days** with a shorter "just bumping this" message. Do not follow up a third time.
- **Don't be defensive if they say no.** A graceful "no worries, thanks for reading" is the best reputation-building move.

---

## Tracking

Track responses in a spreadsheet. Recommended path:

```
<your-aisurface-repo>/docs/launch/recruit-pipeline.md
```

(Create this file in your local clone of the repo when you start sending DMs. Suggested columns: date_sent, project_name, maintainer, channel, response_status, before_score, after_score, case_study_status, notes.)

### Suggested tracker schema

| date_sent | project | maintainer | channel | status | before | after | case_study | notes |
|---|---|---|---|---|---|---|---|---|
| 2026-06-03 | httpie/cli | @dtaibi | GH email | sent | - | - | - | Tue 9am CET |
| 2026-06-03 | withastro/astro | @sebastienlorber | GH email | sent | - | - | - | Tue 9am CET |
| 2026-06-04 | BurntSushi/ripgrep | @burntsushi | GH email | sent | - | - | - | Wed 9am PST |

### Status values

- `sent` — DM delivered, no response yet.
- `opened` — they read it (GitHub shows this for emails).
- `replied-yes` — willing to try.
- `replied-no` — declined politely.
- `ran-audit` — actually ran the audit.
- `shared-before-after` — case study in progress.
- `featured` — added to README.
- `bounced` — email invalid / DM account deleted.

---

## Posting notes

- **Do not bulk-send from a script.** GitHub rate-limits DM/email and flags bot-like behavior. Send manually, 10-15 per session.
- **Do not CC multiple maintainers on the same project.** If a project has co-maintainers, send the DM to the most active one and let them forward internally.
- **Do not send on weekends.** OSS maintainers don't read cold DMs on Saturday.
- **Do not promise version-specific features** ("we'll add Python-specific checks in v0.2 just for you"). It overpromises.
- **Do reply within 24 hours** to any response, even a "no thanks." Slow replies kill momentum.

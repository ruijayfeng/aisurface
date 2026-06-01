<!--
[INPUT]: PLATFORM-SOURCES.md (URL list for the 9 tracked AI-search platforms)
[OUTPUT]: Monthly procedure to refresh references/ai-search-platforms.md with current MAU / trends
[POS]: docs/process/'s monthly platform data runbook, consumed by Boss on the 1st of each month
[PROTOCOL]: Update this header when changed
-->

# Monthly AI-Search Platform 热度 Update

## When

The 1st of every month. Set a recurring calendar reminder:
- Title: "Update aisurface references/ai-search-platforms.md"
- Repeat: monthly, first weekday
- Time: 9:00 AM

(If using Google Calendar: Boss to set up. Apple Calendar / Outlook: equivalent.)

## What

Update `references/ai-search-platforms.md` with fresh platform popularity data.

## How

### Step 1: Gather data (15 min)

Pull latest metrics from each source (see `PLATFORM-SOURCES.md` for URLs):

For each of 9 platforms (ChatGPT, Perplexity, Doubao, DeepSeek, Kimi, Wenxin, Tongyi, GLM, Gemini):

1. **MAU / market share** — from the platform source
2. **API access changes** — release notes / changelog
3. **New features affecting citation** — e.g., new search mode, new surface area
4. **Notable outages or deprecations**

### Step 2: Update the table (20 min)

Open `references/ai-search-platforms.md`, update the popularity table:

- Move platforms with growing MAU up the list
- Add a row for any new major AI-search platform launched in the last 30 days
- Update the "Last updated" date at the top

### Step 3: Commit and push (2 min)

```bash
cd /d/Code/MyProject/aisurface
git add references/ai-search-platforms.md
git commit -m "docs(references): update platform popularity for YYYY-MM"
git push origin main
```

(Only commit if there's actual change. If nothing changed, skip the commit and just leave a note in `docs/process/PLATFORM-UPDATE-LOG.md`.)

### Step 4: Log the update (2 min)

Append a line to `docs/process/PLATFORM-UPDATE-LOG.md`:

```markdown
- YYYY-MM-DD: <one-sentence summary of changes>
```

## Skip rules

- If a major release is in progress, defer the update and note it in the log
- If a platform is acquired or shut down, remove it from the table (with a one-line note in commit message)

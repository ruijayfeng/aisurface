<!--
[INPUT]: none (standalone index)
[OUTPUT]: Navigation index for docs/process/
[POS]: docs/process/'s entry point, consumed by Boss when looking for operational runbooks
[PROTOCOL]: Update this header when changed
-->

# docs/process/ — Post-Launch Operations Runbooks

Internal runbooks Boss follows after the v0.1.0 launch. These are **operational procedures** (cadence, checklists, links), not user-facing docs. Tone is terse, actionable, and assumes Boss knows GitHub, calendars, and the repo layout.

## Member list

| File | Cadence | Purpose |
|---|---|---|
| `TRIAGE.md` | Daily / weekly / monthly | Issue & PR triage cadence, labeling rules, response-time targets |
| `STATE-DISCUSSION-SETUP.md` | One-time | GitHub Discussions category setup steps (admin only) |
| `STATE-DISCUSSION-TEMPLATE.md` | Monthly | Template for "State of aisurface" monthly digest posts |
| `PLATFORM-UPDATE-RUNBOOK.md` | Monthly (1st) | Procedure for updating `references/ai-search-platforms.md` |
| `PLATFORM-SOURCES.md` | Reference | URLs to pull fresh MAU / release-note data for the 9 tracked platforms |
| `PLATFORM-UPDATE-LOG.md` | Append-only | Chronological log of every monthly platform-data update |

## Reading order for Boss

1. **First day post-launch:** Read `STATE-DISCUSSION-SETUP.md` and run the one-time GitHub setup.
2. **Every weekday morning:** Open `TRIAGE.md` and run the Daily checklist.
3. **First of every month:** Open `PLATFORM-UPDATE-RUNBOOK.md` and follow steps 1-4.
4. **First Monday of every month:** Write the "State of aisurface" digest using `STATE-DISCUSSION-TEMPLATE.md`.

## Cross-references

- **CHANGELOG.md** — `## [0.1.0] - 2026-07-15` → `### Operations` subsection lists these runbooks
- **references/ai-search-platforms.md** — the file the monthly platform runbook updates

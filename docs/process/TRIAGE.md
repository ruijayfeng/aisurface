<!--
[INPUT]: none (standalone process doc)
[OUTPUT]: Daily / weekly / monthly issue-triage cadence with labeling rules and response-time targets
[POS]: docs/process/'s issue triage runbook, consumed by Boss every weekday morning
[PROTOCOL]: Update this header when changed
-->

# Issue Triage Cadence

## Daily (5-10 min, every weekday morning)

- [ ] Open https://github.com/ruijayfeng/aisurface/issues
- [ ] For each new issue, apply one label: `bug`, `feature`, `question`, `eval-fixture`, `docs`
- [ ] For `bug` issues: attempt to reproduce, ask for missing info if needed
- [ ] For `feature` issues: comment with your initial take (YAGNI or worthwhile)
- [ ] For `question` issues: answer within 4 hours
- [ ] Close any `duplicate`, `stale`, or `not-a-bug` issues with a one-line reason

## Weekly (30 min, Monday morning)

- [ ] Triage all issues still open
- [ ] Close issues with no response for 30+ days (add `stale` label first)
- [ ] For `bug` issues older than 1 week: prioritize, fix or close
- [ ] Review open PRs, request changes or merge
- [ ] Update `WIP.md` with current focus (see file)

## Monthly (1 hour, first Monday of month)

- [ ] Write a "State of aisurface" digest post on GitHub Discussions
  - Use template in `docs/process/STATE-DISCUSSION-TEMPLATE.md`
  - Cover: new releases, top issues, contributor shoutouts, roadmap
- [ ] Review and close issues older than 90 days (with grace note)
- [ ] Update `references/ai-search-platforms.md` per Task 29 cadence
- [ ] Audit docs: README, references/, SKILL.md — anything outdated?

## Labeling rules

- `bug` — confirmed or suspected code defect
- `feature` — enhancement request
- `question` — user is asking how to do X
- `eval-fixture` — request to add a new eval fixture repo
- `docs` — README/references/SKILL.md issue
- `good first issue` — small, well-defined, newcomer-friendly
- `help wanted` — bigger, needs experience
- `stale` — automated 30-day inactivity marker
- `wontfix` — decided not to address; close after applying

## Response time targets

- `bug` — acknowledge within 24 hours, fix within 1 week (or set expectation)
- `question` — answer within 4 hours
- `feature` — initial take within 1 week
- `PR` — review within 48 hours

## Escalation

If a `bug` affects multiple users or breaks a released skill:
1. Pin a notice to README.md via a "Known issues" section
2. Cut a patch release (v0.1.1, v0.1.2, ...)
3. Post in Discussions / Twitter with the fix timeline

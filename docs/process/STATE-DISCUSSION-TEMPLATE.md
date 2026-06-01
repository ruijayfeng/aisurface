<!--
[INPUT]: none (standalone template)
[OUTPUT]: Reusable markdown template for monthly "State of aisurface" digest posts
[POS]: docs/process/'s monthly digest template, consumed by Boss on the first Monday of each month
[PROTOCOL]: Update this header when changed
-->

# State of aisurface — YYYY-MM

## Releases this month
- v0.X.Y: <summary>

## Top issues
- #N: <summary> (status)

## Contributors
- @user — <contribution>

## Roadmap
- v0.X+1: <planned features>
- v0.X+2: <exploratory>

## Metrics
- Total installs (skills.sh): N
- GitHub stars: N
- Open issues: N
- Open PRs: N

## Ask
- <one specific thing you need from the community>

## How to use

1. Copy this file's body (everything below the first `# State of aisurface` heading)
2. Replace `YYYY-MM` with the current month
3. Fill each section with real data from the past 30 days
4. Post in the **State of aisurface** Discussion category (created via `STATE-DISCUSSION-SETUP.md`)
5. Pin the post if it is the month-of-launch digest

## Sourcing the metrics

- `Total installs (skills.sh)`: check https://skills.sh/ruijayfeng/aisurface
- `GitHub stars`: check the repo header badge (or API)
- `Open issues / PRs`: GitHub sidebar counts, or `gh issue list --state open --json number | jq length`

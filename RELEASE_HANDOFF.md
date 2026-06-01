# v0.1.0 Release Handoff

> Sandbox-prepared. Boss needs to run the manual steps below with their own credentials.

## Release Status Summary

| Item | Status |
|---|---|
| 49/49 tests pass | DONE |
| `ruff check .` clean | DONE |
| CHANGELOG.md updated to 2026-07-15 | DONE |
| `chore(release): v0.1.0` commit | DONE (`b427936`) |
| Annotated tag `v0.1.0` created locally | DONE |
| Tag pushed to `origin` | DONE (sandbox SSH worked — unexpected) |
| `main` branch pushed to `origin` | **TODO (Boss)** — 28 commits ahead |
| skills.sh indexing | **TODO (Boss)** — auto-indexed after main push |

## Final Pre-Release Checklist (all green locally)

- [x] Working tree clean
- [x] 49 passed in 0.81s
- [x] `All checks passed!` (ruff)
- [x] `CHANGELOG.md` says `## [0.1.0] - 2026-07-15`
- [x] Commit `b427936 chore(release): v0.1.0`
- [x] Annotated tag `v0.1.0` → `b427936`
- [x] Tag reachable on `origin`: `c7e80ce refs/tags/v0.1.0`

## Manual Steps Boss Needs to Run

### 1. Push the main branch (28 commits ahead)

```bash
cd /d/Code/MyProject/aisurface
git push origin main
```

Expected output: pushes 28 commits, no conflicts (we have a clean fast-forward).

### 2. Re-confirm the tag is on the remote

The sandbox already pushed it, but verify on your end:

```bash
git ls-remote --tags origin | grep v0.1.0
# Expected:
# c7e80ce...  refs/tags/v0.1.0
# b427936...  refs/tags/v0.1.0^{}
```

If for some reason it is missing:

```bash
git push origin v0.1.0
```

### 3. Publish to skills.sh

**Important correction:** the `npx skills` CLI v1.5.9 does **not** have a `publish` subcommand (verified — `npx skills publish` returns `Unknown command: publish`). The skills.sh publishing model is implicit: SKILL.md files in a GitHub repo are auto-indexed by skills.sh once the repo is public and the default branch contains the files.

The actual user-facing install commands (already documented in README.md) are:

```bash
# 旗舰：仓库审计
npx skills add ruijayfeng/aisurface@audit

# 子 skill：README 优化
npx skills add ruijayfeng/aisurface@readme

# 子 skill：生成 llms.txt
npx skills add ruijayfeng/aisurface@llms-txt
```

These three commands are what end users will run to install the skills. They are the equivalent of "publish" — the indexer picks up the SKILL.md files from your public GitHub repo.

### 4. Optional: trigger a re-index via skills.sh

If skills.sh doesn't pick up the skills within a few hours, you can:
- Visit https://skills.sh and search for `ruijayfeng/aisurface`
- If the registry has a "Submit repo" / "Refresh" link, click it
- Otherwise just wait — the indexer crawls periodically

## Verification Links (post-push)

- Repo releases: https://github.com/ruijayfeng/aisurface/releases/tag/v0.1.0
  - After Boss pushes `main`, draft a release for tag `v0.1.0` with notes from CHANGELOG.md
- skills.sh page: https://skills.sh/ruijayfeng/aisurface
  - Should show 3 skills (`aisurface-audit`, `aisurface-readme`, `aisurface-llms-txt`) once indexed
- Install smoke test (run on Boss's machine after indexing):
  ```bash
  npx skills add ruijayfeng/aisurface@audit --list
  # Expected: lists aisurface-audit with the description from SKILL.md
  ```

## Post-Publish Smoke Test

After each user-install command above, verify:

1. The command returns a success message (not "package not found")
2. `npx skills list` shows the newly added skill
3. The skill's `description:` frontmatter matches what's in the repo's `SKILL.md`

If `npx skills add` returns "package not found", the indexer hasn't crawled the repo yet — wait 1-2 hours and retry.

## Local Artifacts for Reference

- Last commit: `b427936 chore(release): v0.1.0`
- Tag: `v0.1.0` (annotated, points to `b427936`)
- Commit count ahead of origin: 28
- Branch: `main`

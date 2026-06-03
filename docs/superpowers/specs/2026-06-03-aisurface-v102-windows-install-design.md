# aisurface v1.0.2 Design — Windows Install + Path Hotfix

> **Status:** design (2026-06-03, awaiting user review)
> **Scope:** hotfix release
> **Supersedes:** nothing
> **Related:** CHANGELOG `[1.0.1]` (what we're fixing)

---

# Context

v1.0.1 was published to PyPI on 2026-06-03. First real-world self-test surfaced two packaging problems:

1. **Windows PATH problem.** `pip install aisurface` (or `pip install --upgrade aisurface`) generates a console script at `C:\Users\<user>\AppData\Roaming\Python\Python3X\Scripts\aisurface.exe`, but this directory is not on Windows PATH by default. Users following the README 5-min self-test hit `command not found` at step 2 (`aisurface --help`). pip itself prints a WARNING about this. Linux/macOS users are unaffected because `~/.local/bin/` is typically on PATH.

2. **Stale-version problem.** No code path detects "you're on 0.1.3, latest is 1.0.1." A user who installed v0.1.x in the past and then ran `pip install --upgrade aisurface` could end up "successfully" on a stale version (depending on Python environment resolution), and the CLI would still work — silently. Nothing surfaces the discrepancy.

Both are quality-of-install problems, not correctness problems — the audit/fix/verify logic itself is fine. v1.0.2 is a hotfix targeting install health and discoverability, with no changes to the 12-check audit logic or patch generators.

The "skill-first install" architecture (`npx skills add` is the primary user path) means most end users never see this. But the 5-min self-test in README is written for the maintainer and CI users, and it's the only direct, deterministic test of the wheel. It must work.

---

# Goals

A user following the README 5-min self-test on a fresh Windows machine (or any OS) can:

1. Run `python -m scripts.cli --help` and see `{audit, fix, verify, doctor}` immediately after `pip install aisurface`.
2. Run `python -m scripts.cli doctor` and get a clear pass/fail report on the installation, with actionable fix hints for any failure.
3. Be told (via `doctor`) if there's a newer aisurface on PyPI, so silent stale-version situations stop being silent.
4. Hit common error conditions (missing install, wrong path, encoding issues) and get messages that point to the fix, not raw tracebacks.

CI on Windows verifies both `aisurface.exe` and `python -m scripts.cli` work, so the gap that produced v1.0.1 cannot recur silently.

---

# Non-goals

- **No new audit checks.** The 12-check rubric is unchanged.
- **No new fix patches.** The 4 fix generators are unchanged.
- **No new verify platforms.** Perplexity only (DeepSeek is v1.1+).
- **No `--llm` flag work.** Still deferred (v0.1.4 optional).
- **No `aisurface init`.** Still v1.1+ future.
- **No standalone .exe binary (PyInstaller).** Out of scope for a hotfix; revisit if Windows packaging pain persists after v1.0.2.
- **No auto-fix mode in `doctor`.** Doctor is diagnostic only; user reads hints, decides.
- **No post-install PATH manipulation hook.** Fragile on Windows (UAC, edge cases); the `python -m` fallback is the durable answer.

---

# Architecture overview

```
                    ┌────────────────────────────────┐
                    │   python -m scripts.cli ...    │  ← README / SKILL.md / docs canonical
                    │   aisurface ...                │  ← convenience, works when on PATH
                    └──────────────┬─────────────────┘
                                   ▼
                            scripts.cli.main()
                                   ▼
                     ┌─────────────┴─────────────┐
                     │  safe_dispatch decorator   │  ← new: error message wrapper
                     └─────────────┬─────────────┘
                                   ▼
              ┌──────────┬──────────┬──────────┬──────────┐
              ▼          ▼          ▼          ▼
           audit        fix      verify      doctor     ← doctor is new verb
```

v1.0.2 keeps the existing 3-verb CLI and adds `doctor` as a 4th. The 12-check audit logic, 4 fix generators, and verify probe code are **unchanged**. The new layer is a safety net: a decorator that catches common user-facing errors, plus a self-check command.

## Entry point strategy

| Context | Primary command | Rationale |
|---|---|---|
| README 5-min self-test | `python -m scripts.cli ...` | Works on all OS without PATH dependency |
| SKILL.md tool dispatch table | `python -m scripts.cli ...` | Explicit, agent cannot get it wrong |
| README install examples | `python -m scripts.cli` primary + `aisurface` alt | Discoverability for new users |
| `pyproject.toml [project.scripts]` | `aisurface = "scripts.cli:main"` | Unchanged; console script keeps generating |

`python -m scripts.cli` and `aisurface` are aliases. Both route to `scripts.cli.main()`. The only difference is whether the OS can find the entry point via PATH or Python's import system — both are guaranteed after `pip install`.

---

# Decision log (micro-decisions made during brainstorming)

| # | Question | Decision | Why |
|---|---|---|---|
| D1 | Should doctor also check `PERPLEXITY_API_KEY`? | Yes, as item #8, **warn-only** | Verify is the third verb; users who haven't set the key get a pre-flight hint without a hard fail |
| D2 | Exit codes | `0` (all pass/warn), `1` (any fail), `2` (Python < 3.10, can't run) | Network warn stays at 0 but visible in output; no need for a 3rd code beyond the "can't run" case |
| D3 | `doctor --fix` mode? | No | Diagnostic only. `--fix` invites "did it just modify my PATH?" confusion. v1.1+ can add a separate `aisurface setup` if automation is wanted |
| D4 | Async version check on every command? | No, only in `doctor` | Hits PyPI on every command is slow + adds a failure point. Doctor is the single place |
| D5 | Post-install PATH hint? | No, document `python -m` fallback instead | Post-install hooks are fragile on Windows (UAC, conda venvs, PEP 668 managed envs). The fallback is durable |

---

# Component: `aisurface doctor` (new verb)

## Output format

```
$ python -m scripts.cli doctor
aisurface doctor — v1.0.2
==========================

✓ Python 3.14.5 (need >= 3.10)
✓ aisurface 1.0.1 installed
✗ 'aisurface' console script not on PATH
   → Workaround: use 'python -m scripts.cli' instead
   → Fix: add C:\Users\administered\AppData\Roaming\Python\Python314\Scripts to PATH
✓ Dependencies: httpx, jsonschema, selectolax (all importable)
✓ Cache dir: C:\Users\administered\.aisurface (writable)
⚠ PyPI latest: 1.0.1 (you're on 1.0.1, up to date)
✓ Internet: pypi.org reachable
⚠ PERPLEXITY_API_KEY not set — `verify` will fail without it
      Get one at: https://perplexity.ai/account/api
```

Each line uses one of three symbols:
- `✓ pass` — check succeeded
- `✗ fail` — check failed, `→ ...` lines below give fix hints
- `⚠ warn` — check incomplete or feature-not-ready; not a hard failure

## The 8 checks (in order)

| # | Check | Pass criterion | Fail hint | Skip condition |
|---|---|---|---|---|
| 1 | Python ≥ 3.10 | `sys.version_info >= (3, 10)` | Current version + Python.org download link | **If Python < 3.10, doctor short-circuits with exit code 2 and does not run remaining checks** (see "Exit codes" below) |
| 2 | `scripts` package importable | `import scripts.audit`, `import scripts.fix`, `import scripts.verify` all succeed | `pip install aisurface` (or `pip install -e .` for dev) | Never skip |
| 3 | Console script on PATH | `shutil.which("aisurface") is not None` | "Use `python -m scripts.cli` instead" + "Add `<Scripts dir>` to PATH" with the actual path from `sysconfig` | Never skip |
| 4 | Required deps | `import httpx`, `import jsonschema`, `import selectolax` all succeed | `pip install --force-reinstall aisurface` | Never skip |
| 5 | Cache dir writable | `~/.aisurface/` exists, `os.access(W_OK)` true; create if missing | "Check permissions on `~/.aisurface/`, or set `AISURFACE_CACHE_DIR` to a writable path" | Never skip |
| 6 | PyPI latest version | `httpx.get("https://pypi.org/pypi/aisurface/json", timeout=5)` seconds; response `info.version` is parseable. **Version comparison rules:** installed == PyPI → pass (up to date); installed < PyPI → warn (`pip install --upgrade aisurface`); installed > PyPI → pass with note (you're on a pre-release or local build) | `pip install --upgrade aisurface` (only on the < case) | Network error or timeout → warn ("couldn't reach PyPI"), not fail |
| 7 | Internet reachable | Implicit: check 6 succeeded | — | — |
| 8 | `PERPLEXITY_API_KEY` env | `os.environ.get("PERPLEXITY_API_KEY")` is set and non-empty | "Get one at: https://perplexity.ai/account/api" | Never skip; always warn-only |

## Exit codes

- `0` — all checks pass, or only warnings (network, PERPLEXITY_API_KEY)
- `1` — at least one check failed
- `2` — Python < 3.10 (doctor itself can't run). Message format:
  ```
  ✗ Python 3.9.5 — aisurface needs >= 3.10
    → Upgrade Python: https://www.python.org/downloads/
  ```
  No further checks are run. The version number in the message comes from `sys.version`.

## Flags

- `--json` — machine-readable output. JSON shape:
  ```json
  {
    "aisurface_version": "1.0.2",
    "python_version": "3.14.5",
    "checks": [
      {"name": "python_version", "status": "pass", "message": "3.14.5 (need >= 3.10)", "fix_hints": []},
      {"name": "scripts_importable", "status": "pass", "message": "aisurface 1.0.2 installed", "fix_hints": []},
      {"name": "console_script_on_path", "status": "fail", "message": "not on PATH", "fix_hints": ["use 'python -m scripts.cli'", "add /c/.../Scripts to PATH"]}
    ],
    "summary": {"pass": 6, "fail": 1, "warn": 1, "exit_code": 1}
  }
  ```
- `--no-color` — same as audit/fix
- `--skip-network` — skip check 6, useful in offline / CI-no-network scenarios

## Implementation

- New file: `scripts/doctor.py`
- L3 header in the same `[INPUT]/[OUTPUT]/[POS]` format as other scripts
- Exports `cmd_doctor(args) -> int` with the same signature as `cmd_audit` / `cmd_fix` / `cmd_verify`
- Internal data class: `DoctorCheck(name: str, status: Literal["pass", "fail", "warn"], message: str, fix_hints: list[str])`
- 8 check functions, each returns one `DoctorCheck`; easy to add a 9th
- Render: human-readable by default (uses `scripts/colors.py`), JSON when `--json`
- L2 (`scripts/CLAUDE.md`): add `doctor.py` to the member list

---

# Component: `safe_dispatch` error wrapper (new file)

Lightweight decorator that wraps each `cmd_*` handler. Catches 4 exception classes, rewrites the message, and exits with code 1.

## The 4 wrapped exception classes

All rewritten messages go to **stderr** (not stdout), so the CLI exit-code-1 contract is preserved and stdout remains clean for piping.

| Exception | Detection | Rewritten message |
|---|---|---|
| `ModuleNotFoundError` | message contains `"scripts."` | `✗ aisurface 没装(或装错环境). 跑: pip install aisurface` |
| `FileNotFoundError` | any (path always comes from `args.path` on the `args` namespace, so we include it in the message) | `✗ 路径不存在: {args.path}. 检查下路径再试` |
| `UnicodeEncodeError` | any | `✗ 控制台编码有问题. 设 PYTHONUTF8=1 和 PYTHONIOENCODING=utf-8` |
| `PermissionError` | message contains `~/.aisurface` or the `AISURFACE_CACHE_DIR` env value | `✗ 写不进 <cache dir>. 看权限,或设 AISURFACE_CACHE_DIR 改路径` |

## Not wrapped (intentional)

- `KeyboardInterrupt` — let the user Ctrl-C
- Network timeouts in verify — already handled in `verify/perplexity.py`
- Audit/fix/verify business exceptions (e.g., `jsonschema.ValidationError`) — let them surface, they're real bugs
- Anything not in the 4 above — original traceback

## Implementation

- New file: `scripts/safe_dispatch.py`
- Exports `safe_dispatch` decorator
- Applied in `scripts/cli.py` to each of the 4 subcommand handlers (audit, fix, verify, doctor)
- L2 (`scripts/CLAUDE.md`): add `safe_dispatch.py` to the member list
- Reuses `scripts/colors.py` for the red ✗ glyph, matching audit/fix output style

---

# CI matrix

## New file: `.github/workflows/ci.yml`

- **Triggers:** push to main, pull_request to main, manual `workflow_dispatch`
- **Matrix:** `os: [ubuntu-latest, macos-latest, windows-latest]` × `python-version: ["3.10", "3.11", "3.12", "3.13", "3.14"]` = **15 jobs**
- **Steps per job:**
  1. `actions/checkout@v4`
  2. `actions/setup-python@v5` with the matrix version
  3. `pip install -e .[dev]`
  4. `pytest` (must pass)
  5. `ruff check` (must pass)
  6. Smoke test (always succeeds on `python -m scripts.cli --help`; on the `aisurface` line, allow failure on Windows because PATH is the very thing we're testing):
     ```
     aisurface --help || echo "console script not on PATH (expected on some Windows configs)"
     python -m scripts.cli --help
     python -m scripts.cli doctor --no-color
     ```

## Why this catches the v1.0.1 gap

The Windows job runs `pip install -e .`, which generates `aisurface.exe`. The smoke step tries both `aisurface` and `python -m`. The `||` on the `aisurface` line is a deliberate allow-fail because we know Windows CI containers can have the same PATH issue we're trying to document. But the existence of `aisurface.exe` (verified by trying to run it) is the signal — if hatchling stops generating the console script, we'll see a different kind of failure.

---

# Documentation changes

| File | Change |
|---|---|
| `README.md` 5-min self-test | All 7 steps rewritten to use `python -m scripts.cli ...`. Add a note: "If your `aisurface` console script is on PATH, that's an alias for the same `scripts.cli.main` — pick whichever you like." Add step 8: `python -m scripts.cli doctor --no-color` |
| `README.en.md` | Same as above (English) |
| `SKILL.md` tool dispatch table | The 3 verb rows changed from `python -m scripts.cli <verb> <path>` (which they already mostly are) to be explicitly and consistently `python -m scripts.cli` form, with a new row for `doctor` |
| `CHANGELOG.md` | New `## [1.0.2] - 2026-06-03` section with Added/Changed/Fixed subsections |
| `ROADMAP.md` | New row in the release sequence: v1.0.2 — install health + doctor + CI matrix |
| `scripts/CLAUDE.md` (L2) | Add `doctor.py` and `safe_dispatch.py` to the member list |
| `CLAUDE.md` (L1) | Add the two new files to the `scripts/` directory tree |

---

# Release process

Same 9-step flow as v1.0.1:

1. All work committed, `git push origin main`
2. `pyproject.toml` version bump: `1.0.1` → `1.0.2`
3. CHANGELOG entry already in place from step 7 of "Documentation changes"
4. `git tag v1.0.2`, `git push origin v1.0.2`
5. `python -m build` (or `hatch build`) → wheel + sdist in `dist/`
6. `twine check dist/*` (metadata validation)
7. `twine upload --repository testpypi dist/*` (auto-verified)
8. In a clean venv: `pip install --index-url https://test.pypi.org/simple/ aisurface==1.0.2`, run `python -m scripts.cli doctor --no-color`, run `python -m scripts.cli audit evals/fixtures/perfect-readme-and-docs --no-color` (expect 90+)
9. `twine upload dist/*` → real PyPI

---

# Test plan

## New: `tests/test_doctor.py` (unit, ~150 lines)

Eight unit tests, one per check, plus exit-code boundary cases:

1. `test_python_version_pass` — mock `sys.version_info = (3, 12, 0)`, expect pass
2. `test_python_version_fail` — mock `sys.version_info = (3, 9, 0)`, expect fail + version mention
3. `test_scripts_importable` — `import scripts.audit` etc. succeed, expect pass
4. `test_scripts_importable_fail` — `unittest.mock.patch.dict("sys.modules", {"scripts.audit": None})`, expect fail + `pip install` hint
5. `test_console_script_on_path` — `mock.patch("shutil.which", return_value="/some/path/aisurface")`, expect pass; `return_value=None` expect fail
6. `test_deps_importable` — try real import (deps are installed in test env)
7. `test_cache_dir_writable` — `mock.patch("os.access", return_value=True)`, expect pass; `return_value=False` expect fail
8. `test_pypi_latest_via_mock` — `mock.patch("httpx.get", return_value=mock_response_with_version("1.0.2"))` + installed `1.0.1` → warn; equal versions → pass; older version in response → fail (you're on a prerelease?)
9. `test_pypi_network_error` — `mock.patch("httpx.get", side_effect=httpx.ConnectError)`, expect warn (not fail)
10. `test_perplexity_key_present` — `mock.patch.dict(os.environ, {"PERPLEXITY_API_KEY": "test"})`, expect pass
11. `test_perplexity_key_missing` — `mock.patch.dict(os.environ, {}, clear=True)`, expect warn
12. `test_exit_code_0_all_pass` — all checks mocked pass, expect `main() == 0`
13. `test_exit_code_1_any_fail` — one check mocked fail, expect `main() == 1`
14. `test_exit_code_2_old_python` — Python 3.9, expect `main() == 2` and the failure message names the version
15. `test_json_output` — `--json` flag, parse stdout, assert all 8 checks present with correct status

## New: `tests/test_safe_dispatch.py` (unit, ~80 lines)

1. `test_catches_module_not_found` — handler raises `ModuleNotFoundError("No module named 'scripts.foo'")`, expect exit 1 with `pip install` hint
2. `test_catches_file_not_found` — handler raises `FileNotFoundError(2, "No such file")` on a path arg, expect exit 1 with path in message
3. `test_catches_unicode_error` — handler raises `UnicodeEncodeError(...)`, expect exit 1 with `PYTHONUTF8` hint
4. `test_catches_permission_error` — handler raises `PermissionError` on cache dir, expect exit 1 with `AISURFACE_CACHE_DIR` hint
5. `test_does_not_catch_keyboard_interrupt` — handler raises `KeyboardInterrupt`, decorator must not catch (re-raise)
6. `test_does_not_catch_value_error` — handler raises `ValueError` (unrelated), decorator must not catch

## Existing tests

Unchanged. All 105 current tests must still pass.

## Regression coverage (existing functionality that must keep working)

Per the v1.0.2 release constraint "将已有的功能都要保持可用", every existing capability must be verified intact:

| Existing capability | How we verify it still works |
|---|---|
| 3-verb CLI (`audit` / `fix` / `verify`) | All 105 existing pytest tests pass on all 15 CI matrix jobs (3 OS × 5 Python) |
| `aisurface` console script generation | `pip install -e .` produces a working `aisurface` (or `aisurface.exe` on Windows) that exits 0 on `--help` — verified in CI smoke step |
| `python -m scripts.cli` entry | Same: exits 0 on `--help` — verified in CI smoke step on all 15 jobs |
| `SKILL.md` natural-language triggers for audit/fix/verify | Manual review: trigger phrases in SKILL.md still map to the same commands (no regressions in dispatch table) |
| 12-check audit rubric | Test fixtures (`evals/fixtures/`) pass with the same expected scores as v1.0.1: `bad-readme-python-lib` → 16/100, `perfect-readme-and-docs` → 90+ |
| `fix` 4 patch generators | Snapshot tests in `evals/expected_patches/` unchanged; `fix --dry-run` on `bad-readme-python-lib` produces the same 4 patches |
| `verify` Perplexity probe | Adapter test still passes; baseline store at `~/.aisurface/baselines/` still works |
| `npx skills add ruijayfeng/aisurface` flow | Out of band for this release — the skill itself is unchanged. README install section still leads with this command |
| README 5-min self-test | Steps 1–5 from the v1.0.1 README still pass deterministically (after the rewrite to use `python -m scripts.cli`) |
| L1/L2/L3 GEB fractal docs | L1 (`/CLAUDE.md`), L2 (`scripts/CLAUDE.md`), L3 (every `scripts/*.py` file header) all remain consistent — the new files (`doctor.py`, `safe_dispatch.py`) get the same L3 treatment, and L1/L2 are updated to mention them |

The "no regression" bar is enforced by:
- 105 existing pytest tests must pass (zero skipped, zero marked xfail, zero modified)
- All 4 evals/fixtures must produce their expected audit scores
- CI smoke runs both `aisurface` and `python -m scripts.cli` on all 15 jobs
- Manual end-to-end run of the 5-min self-test on a clean Windows VM (post-release verification, not in CI)

## CI smoke (covered above)

`python -m scripts.cli doctor --no-color` runs in the CI matrix on all 15 jobs and must exit 0 (the PyPI network call is the only thing that could realistically fail; if it does, it's a warn, not fail).

---

# File changes summary

## New files

| Path | Estimated lines | Purpose |
|---|---|---|
| `scripts/doctor.py` | 200–250 | `cmd_doctor` + 8 check functions + render |
| `scripts/safe_dispatch.py` | 60–80 | `safe_dispatch` decorator |
| `tests/test_doctor.py` | 150 | 15 unit tests for `doctor` |
| `tests/test_safe_dispatch.py` | 80 | 6 unit tests for decorator |
| `docs/superpowers/specs/2026-06-03-aisurface-v102-windows-install-design.md` | (this file) | The spec itself |
| `.github/workflows/ci.yml` | 40 | CI matrix config |

## Modified files

| Path | Change |
|---|---|
| `scripts/cli.py` | Add `doctor` to `_DISPATCH`; wrap each of the 4 subcommand handlers with `@safe_dispatch`; add `doctor` subparser |
| `scripts/CLAUDE.md` (L2) | Add `doctor.py` and `safe_dispatch.py` to member list |
| `CLAUDE.md` (L1) | Add the two new files to the `scripts/` directory tree |
| `README.md` | 5-min self-test rewritten to use `python -m scripts.cli`; add step 8 (doctor) |
| `README.en.md` | Same |
| `SKILL.md` | Tool dispatch table gets a new row mapping natural-language triggers (e.g. "我的 aisurface 装对了吗", "装坏了", "命令找不到", "diagnose installation") → `python -m scripts.cli doctor`. **No command name exposed to the user surface** — this is spec §11b "user-facing abstraction". No new subcommand is mentioned in the user-facing "我能做三件事" / "怎么跟我说" sections |
| `CHANGELOG.md` | New `## [1.0.2] - 2026-06-03` section |
| `ROADMAP.md` | New v1.0.2 row |
| `pyproject.toml` | Version bump `1.0.1` → `1.0.2` |

Total: 6 new files, 9 modified files. ~3–5 commits in implementation.

---

# Out-of-scope follow-ups (parked for v1.1+)

These are real concerns but explicitly **not** in v1.0.2:

- `aisurface init` — bootstrap a fresh project with all GEO-ready scaffolding
- Standalone `.exe` via PyInstaller — revisit if Windows packaging pain persists after v1.0.2 ships
- More verify platforms (ChatGPT, Claude, Gemini, DeepSeek, etc.) — see `references/ai-search-platforms.md`
- `aisurface setup` — automated version of "doctor + apply all fix_hints" (separate from doctor, runs in a separate trust context)
- `--llm` flag — v0.1.4 optional
- v1.1.0: remove `skills/_deprecated/` per the existing deprecation cycle

[PROTOCOL]: Update this header when changed, then check `CLAUDE.md` and `scripts/CLAUDE.md`.

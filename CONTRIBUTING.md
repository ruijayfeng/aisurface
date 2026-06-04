# 贡献指南

欢迎为 aisurface 贡献！

> **关于用户和贡献者:** 这份文档是给**贡献者**看的(写代码、加检查、跑测试、直接用 Python CLI)。
> 如果你只是想**用** aisurface 诊断 / 修 / 验证你的项目,请回到 [README.md](./README.md) — 装完 skill 跟 agent 说大白话就行。

---

## 提 issue

- **Bug**: 用 `Bug report` 模板
- **功能建议**: 用 `Feature request` 模板
- **问题咨询**: 用 `Question` 模板

## 提 PR

1. Fork → 改 → PR
2. 一个 PR 一个改动
3. 所有 PR 必须过 CI(ruff + pytest 128 + 12 = 140)
4. 添加测试覆盖你的改动

## 开发环境

```bash
git clone https://github.com/ruijayfeng/aisurface.git
cd aisurface
pip install -e ".[dev]"
pytest
```

## 添加新的 GEO 检查

`scripts/scanner.py` + `scripts/cli.py` 是主要扩展点。

每个检查必须:
- 跑在 2 个 eval fixture 上不 crash
- 在 `tests/integration/test_full_audit.py` 添加 fixture
- 更新 `references/readme-checklist.md`

---

## Using the Python CLI (without Claude Code) / 直接用 Python CLI

> **Who is this for?** CI pipelines, automation scripts, contributors debugging the
> Python layer, or anyone who wants to bypass the skill and run the underlying
> commands directly. End users should NOT need this section — go back to
> [README.md](./README.md).

### Install

```bash
pip install aisurface
```

Or for dev mode:

```bash
git clone https://github.com/ruijayfeng/aisurface.git
cd aisurface
pip install -e ".[dev]"
```

### Three-verb workflow

```bash
# 1) Audit: 12 GEO checks, weighted health score 0-100
aisurface audit .

# 2) Fix: auto-generate 4 highest-impact patches
aisurface fix .

# 3) Verify: probe real AI platforms, diff against stored baseline
export PERPLEXITY_API_KEY=...
aisurface verify .                # first run: establish baseline
aisurface fix .                   # apply patches
aisurface verify .                # second run: measure the lift
```

`fix` generates: FAQ stub in README, When-to-use sections, `.well-known/llms.txt`,
`index.schema.json`. Review the diff, confirm, done.

`verify` probes 10 representative queries against Perplexity (more platforms coming)
and compares the citation rate to a stored baseline.

> **Windows note:** `aisurface` console script may not be on `PATH` after a default
> Python install. Use `python -m scripts.cli` instead — it's the same call, works
> everywhere. The `doctor` subcommand (`python -m scripts.cli doctor`) tells you
> exactly which directory to add to `PATH` if you want the shorter form.

### 5-minute self-test (verify the install)

You can verify the package end-to-end **without** Claude Code and **without** an
AI platform API — `pip install aisurface` plus the bundled fixtures give you
deterministic output.

```bash
# 1) Install / upgrade to the latest PyPI release
pip install --upgrade aisurface
python -m scripts.cli doctor --no-color  # expect: ✓ Python / ✓ scripts importable / ✓ cache writable

# 2) The 4-verb CLI is wired up
python -m scripts.cli --help              # expect {audit, fix, verify, doctor}

# 3) Run a known-bad fixture — expect health 16/100
python -m scripts.cli audit evals/fixtures/bad-readme-python-lib --no-color

# 4) Run the known-good fixture — expect 90+ (sanity check on the upper bound)
python -m scripts.cli audit evals/fixtures/perfect-readme-and-docs --no-color

# 5) See what `fix` would write (no disk writes)
python -m scripts.cli fix evals/fixtures/bad-readme-python-lib --dry-run

# 6) Run on your own project (numbers will differ from the fixtures — that's expected)
python -m scripts.cli audit /path/to/your/repo --no-color

# 7) (Optional) Real citation verification — needs PERPLEXITY_API_KEY
export PERPLEXITY_API_KEY=pplx-...
python -m scripts.cli verify /path/to/your/repo        # first run: stores baseline in ~/.aisurface/baselines/
```

Steps 1-5 confirm the v1.0.2 package itself: no broken imports, no missing files,
all four CLI verbs work. Step 6 is the real test — run it on an actual repo you
maintain. Step 7 needs a paid API key, skip it if you don't have one.

### 12-check audit (what the audit runs)

| # | Check | Type |
|---|---|---|
| 1 | README problem statement | Semantic |
| 2 | README FAQ section | Semantic |
| 3 | README when to use / not to use | Semantic |
| 4 | README runnable code examples | Semantic |
| 5 | Schema.org markup | Structural |
| 6 | `.well-known/llms.txt` | Structural |
| 7 | GitHub topics complete (8-12) | Structural |
| 8 | FAQ section heading in README | Semantic |
| 9 | When to use / not to use in README | Semantic |
| 10 | Citation-worthy content (numbers / code / named entities) | Semantic |
| 11 | Distribution signals (awesome / npm / PyPI) | Structural |
| 12 | AI search platforms named in README | Semantic |

### Where things live

- `scripts/cli.py` — argparse + subcommand dispatch
- `scripts/audit.py` — 12-check audit logic
- `scripts/fix/` — patch generators
- `scripts/verify/` — AI platform probes
- `scripts/doctor.py` — install-health self-check
- `scripts/safe_dispatch.py` — user-facing error wrapper
- `references/` — knowledge base (platforms, schemas, llms.txt spec, GEO checklist)

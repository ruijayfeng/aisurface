# aisurface Skill Optimization + v1.0 Bridge Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Optimize the aisurface SKILL.md per skill-creator standards, set up GEB fractal documentation across the codebase, and bridge to the v1.0 implementation with updated specs/plans/roadmap and clear development objectives.

**Architecture:** Three-phase roll — (1) finalize the unified `SKILL.md` and run the description-optimization loop so the trigger surface is measured, not guessed; (2) seed the L1/L2/L3 documentation tree per the project's GEB Fractal protocol so every future change has a place to land; (3) propagate the user-facing-abstraction and skill-first install decisions into the v1.0 spec/plan and the user-facing README/ROADMAP.

**Tech Stack:** Python 3.10+ (existing), Claude Code skills (YAML frontmatter + markdown body), JSON for trigger evals, the `skill-creator` package's `run_loop.py` for description optimization, the GEB L1/L2/L3 fractal-doc protocol defined in the project `CLAUDE.md`.

---

# Development Objectives (清晰开发目标)

The whole point of this plan is to land a clean baseline from which v1.0 can be built. Done = all of the following are true and a fresh contributor can answer each with one document:

1. **Skill is unified.** One `SKILL.md` (name `aisurface`) is the single user-facing surface. The two old sub-skill files (`aisurface-readme`, `aisurface-llms-txt`) live in `skills/_deprecated/` with deprecation notices. No SKILL.md in the repo mentions `--patch`, `aisurface@probe`, `aisurface@schema`, or "v0.1/v0.3" version numbers in user-visible text.
2. **Triggers are measured.** A trigger-eval JSON with 8+ should-trigger and 8+ should-not-trigger queries exists at `evals/trigger_evals.json`. The `description` field has been run through the `run_loop` optimizer and the best-scoring variant is committed.
3. **Documentation is fractal-complete.** L1 (`/CLAUDE.md`), L2 (one `CLAUDE.md` per module directory: `scripts/`, `skills/`, `references/`, `tests/`, `evals/`), and L3 (file-header contracts on every `scripts/*.py`) are all in place. Every script file has `[INPUT]`/`[OUTPUT]`/`[POS]` comments.
4. **v1.0 is correctly framed.** The v1.0 spec gains a "user-facing abstraction" principle section; the v1.0 plan's Tasks 15–18 are updated to reflect skill-first install + the new SKILL.md design; `ROADMAP.md` is consistent with all the above; `README.md` / `README.en.md` lead with `npx skills add` and a natural-language demo, not `pip install`.
5. **v1.0 implementation can start cold.** From the artifacts produced here, a fresh agent can open the v1.0 plan and execute Task 1 (CLI subparser refactor) without first having to read the current `SKILL.md` or guess the install story.

Explicit non-goals for this plan: implementing the `fix` or `verify` commands (those are v0.1.2/v0.1.3 work in the existing v1.0 plan), changing the 12-check rubric, breaking the existing 67 tests, modifying the Python CLI's internal subcommand names.

---

# File Structure (post-plan)

```
aisurface/
├── SKILL.md                              # MODIFIED: rewrite to unified `aisurface` skill (was `aisurface-audit`)
├── CLAUDE.md                             # MODIFIED: L1 update — reflect new skill architecture
├── ROADMAP.md                            # MODIFIED: align with new skill model + install story
├── README.md / README.en.md              # MODIFIED: lead with `npx skills add` + natural-language demo
│
├── skills/                               # MODIFIED: 2 sub-skill dirs move to _deprecated/
│   ├── _deprecated/                      # NEW directory
│   │   ├── aisurface-readme/
│   │   │   └── SKILL.md                  # MOVED + deprecation notice added
│   │   └── aisurface-llms-txt/
│   │       └── SKILL.md                  # MOVED + deprecation notice added
│   └── CLAUDE.md                         # NEW: L2 — skills module map
│
├── scripts/                              # EXISTING (unchanged behavior)
│   ├── *.py                              # MODIFIED: add L3 [INPUT]/[OUTPUT]/[POS] headers (14 files)
│   └── CLAUDE.md                         # NEW: L2 — scripts module map
│
├── references/                           # EXISTING
│   ├── *.md                              # (unchanged)
│   └── CLAUDE.md                         # NEW: L2 — references module map
│
├── tests/                                # EXISTING
│   ├── unit/  integration/               # (unchanged)
│   └── CLAUDE.md                         # NEW: L2 — tests module map
│
├── evals/                                # EXISTING
│   ├── fixtures/                         # (unchanged)
│   ├── expected_patches/                 # (unchanged — will be added by v0.1.2 work)
│   ├── trigger_evals.json                # NEW: 16+ trigger queries for description optimization
│   └── CLAUDE.md                         # NEW: L2 — evals module map
│
├── docs/                                 # NEW content directory
│   └── superpowers/
│       └── plans/
│           └── 2026-06-03-aisurface-skill-optimization-and-v1-bridge.md   # this plan
│
└── ../SkillsCreate/InitSkill/docs/superpowers/   # sibling repo (external)
    ├── specs/2026-06-02-aisurface-v100-design.md  # MODIFIED: add user-facing abstraction §11b
    └── plans/2026-06-02-aisurface-v100.md          # MODIFIED: update Task 15/16/17/18
```

---

# Phase 1 — Current Skill Optimization (skill-creator loop)

## Task 1: Replace root `SKILL.md` with the unified skill

**Files:**
- Modify: `D:\Code\MyProject\aisurface\SKILL.md` (full rewrite)

The current `SKILL.md` is named `aisurface-audit` and describes only the audit verb. It also references non-existent `--patch`, `aisurface@probe`, `aisurface@schema` — Lack-of-Surprise violations. v1.0 unifies everything into one skill named `aisurface`. Replace the file in full.

- [ ] **Step 1: Open the current file and confirm the rewrite targets**

```bash
head -5 D:/Code/MyProject/aisurface/SKILL.md
```

Expected: starts with `---` and `name: aisurface-audit`.

- [ ] **Step 2: Replace the file with the unified content**

Use the Write tool on `D:\Code\MyProject\aisurface\SKILL.md` with the exact content below.

```markdown
---
name: aisurface
description: Use when an open-source project maintainer wants their project to surface in AI search results across ChatGPT, Perplexity, Claude, Gemini, 豆包, DeepSeek, 文心一言, 通义千问, Kimi, 智谱, GLM. Triggers on any of: "audit my project for AI search", "is my project AI-citation-friendly", "GEO audit", "improve AI discoverability", "make my project AI-search-ready", "does my project show up in AI search", "fix my README for ChatGPT", "AI 搜索能不能搜到我的项目", "诊断我的项目 GEO", "按 AI 搜索最佳实践改 README", "AI 真的引用我项目了吗", "verify AI platform citation rate", or any request to improve a GitHub repo's citation-friendliness. Even if the user only mentions one concern (e.g., "我的项目 ChatGPT 搜不到" or "我的 README 写得不好") this skill applies. Do NOT trigger for: general questions about what GEO is, questions about closed-source or marketing sites, or SEO for non-AI-search engines.
---

# aisurface

帮你的开源项目在 AI 搜索结果里浮到表面(ChatGPT / Perplexity / Claude / Gemini / 豆包 / DeepSeek / 文心一言 / 通义千问 / Kimi / 智谱 / GLM)。

不管你说"诊断"、"修"、"验证",还是直接说大白话,这件事就找我。

## 我能做三件事

**🩺 诊断** — 扫你的项目,给个 0-100 分,问题在哪按"最影响 AI 引用"排好
**🔧 修** — 按 AI 搜索最佳实践,自动生成补丁,改你的 README、生成 llms.txt、生成 Schema.org 标记
**📊 验证** — 真的去问 AI 平台"你引没引用我项目",给你真实数据,跟修复前比涨没涨

## 怎么跟我说

不用记命令。挑最顺嘴的一句:

**想诊断:**
- "看看我的项目能不能被 AI 搜到"
- "我的项目 GEO 现状怎么样"
- "诊断一下 /path/to/your-project"
- "audit my repo for AI search"
- "is my project AI-citation-friendly"

**想修:**
- "按 AI 搜索最佳实践改我的项目"
- "把刚才诊断的问题修了"
- "给我 README 加 FAQ 段、llms.txt、Schema.org"
- "fix my README for ChatGPT/Perplexity/Claude"
- "rewrite my project for AI citation"

**想验证:**
- "现在 AI 真的引用我项目了吗"
- "Perplexity 提不提我的项目"
- "跟修复前比,引用率涨没涨"
- "verify AI platform citation rate"
- "does my project show up in AI search"

## 你会看到啥

- **诊断**:0-100 分 + 🔴 必改清单(前 3-5 条按 impact 排)
- **修**:我列出要改的文件和具体内容,你点头我才动手
- **验证**:AI 平台回答里有没有你项目链接的真实数字

## 你需要给我的

- 一个开源项目的根目录路径
- 用"验证"时,一个 Perplexity API key(没的话我告诉你去哪拿:https://perplexity.ai/account/api)

## 我不会干的事

- 不会偷偷改你没同意的文件
- 默认不联网调 AI(语义检查是本地启发式,够用大部分情况)
- 不需要你懂 Python / CLI / GEO

## 安装

```bash
npx skills add ruijayfeng/aisurface
```

装完跟我说一句"诊断我的项目"就行,Python 环境我自己处理。

---

# 给 agent 的内部提示

下面这段是给执行这个 skill 的 agent 看的,不要原样转给用户。

## 工具调用(按用户意图选)

| 用户说什么 | 你做什么 |
|---|---|
| "诊断 / audit / 看看" | 调 `python -m scripts.cli audit <path>`(或 `aisurface audit <path>`,先确认 `aisurface` console script 在 PATH 里) |
| "修 / fix / 改 README / 改 llms.txt / 加 Schema" | 调 `python -m scripts.cli fix <path> --dry-run` 先给用户看,用户同意后再 `--yes` 落地 |
| "验证 / verify / AI 真的引用没" | 检查 `PERPLEXITY_API_KEY` 环境变量,缺了告诉用户去 https://perplexity.ai/account/api 拿;然后调 `python -m scripts.cli verify <path>` |
| 路径没说清楚 | 问用户要,别假设 |
| 多种意图(诊断+修+验证) | 按顺序做,每步都给用户看结果,问"继续?" |

## 触发前的前置检查

1. **Python 工具是否可用**:`python -m scripts.cli --help` 跑得起来吗?跑不起来就告诉用户"我在帮你装 aisurface Python 工具",然后跑 `pip install aisurface`(或 `pip install -e .` dev 模式)
2. **项目路径存在吗**:`<path>` 是个目录吗?不在就问用户
3. **GitHub 项目类型**:`scan_repo` 会自动判(python / node / nextjs / rust / go / unknown),别自己问用户

## 何时加载 references/

| 用户提什么 | 读哪个 references/ 文件 |
|---|---|
| 具体平台名(ChatGPT/Perplexity/Claude/豆包/DeepSeek/...) | `references/ai-search-platforms.md` |
| Schema.org / JSON-LD / FAQ schema | `references/schema-templates.md` |
| llms.txt / llmstxt.org | `references/llms-txt-spec.md` |
| README 改写 / 优化 / 改 FAQ / 改 When-to-use | `references/readme-checklist.md` + `references/citation-patterns.md` |
| 用户问"AI 怎么引用 / 为什么 AI 不引我" | `references/citation-patterns.md` |

## 报错时

- **Python 工具没装** → "我先帮你装一下" → `pip install aisurface`
- **路径不存在** → "找不到这个目录,你确认下路径?"
- **PERPLEXITY_API_KEY 缺** → 明确说去哪拿,不要自己瞎填
- **平台 API 失败** → 告诉用户"Perplexity 这次没回应,我先跳过,继续审计/修复",不阻塞整体流程
- **用户的项目是非 OSS(纯 URL、闭源营销站)** → 礼貌拒绝并推荐 coreyhaines31/marketingskills@seo-audit

## 输出格式硬约束

- **审计报告**:用 `report.render_report()` 输出的 markdown 模板(包含 Health score / Sub-scores / 🔴 Must-fix / 🟡 Should-fix / 🟢 Nice-to-have)
- **修复列表**:用 `fix` 子命令的默认输出(列 patch 类型、目标文件、改动摘要)
- **验证结果**:用 `verify` 子命令的默认输出(baseline cited X/N → current cited Y/N,delta +Z)

不要自己重新设计输出格式,直接用代码里的 render 函数。
```

- [ ] **Step 3: Verify the file's YAML frontmatter is well-formed**

```bash
head -3 D:/Code/MyProject/aisurface/SKILL.md
```

Expected: starts with `---`, then `name: aisurface`, then `description: Use when...`. The closing `---` must be on a line by itself right before `# aisurface`.

- [ ] **Step 4: Commit**

```bash
git add SKILL.md
git commit -m "feat(skill): unify to single `aisurface` skill with natural-language triggers"
```

---

## Task 2: Migrate the two deprecated sub-skills

**Files:**
- Create: `D:\Code\MyProject\aisurface\skills\_deprecated\` (directory)
- Move: `skills/aisurface-readme/SKILL.md` → `skills/_deprecated/aisurface-readme/SKILL.md`
- Move: `skills/aisurface-llms-txt/SKILL.md` → `skills/_deprecated/aisurface-llms-txt/SKILL.md`
- Create: empty `skills/aisurface-readme/` and `skills/aisurface-llms-txt/` `.gitkeep` files (or remove the empty dirs; we use `.gitkeep` so the move is unambiguous)

v1.0 collapses the 3-skill model into 1. The two sub-skill files are kept under `skills/_deprecated/` for one release with a deprecation pointer, per the v1.0 spec Task 15.

- [ ] **Step 1: Create the `_deprecated` directory and move the files**

```bash
mkdir -p D:/Code/MyProject/aisurface/skills/_deprecated
git mv D:/Code/MyProject/aisurface/skills/aisurface-readme D:/Code/MyProject/aisurface/skills/_deprecated/aisurface-readme
git mv D:/Code/MyProject/aisurface/skills/aisurface-llms-txt D:/Code/MyProject/aisurface/skills/_deprecated/aisurface-llms-txt
```

Expected: `skills/` now contains only `_deprecated/`. Verify with `ls skills/`.

- [ ] **Step 2: Prepend a deprecation note to each moved file**

For both `skills/_deprecated/aisurface-readme/SKILL.md` and `skills/_deprecated/aisurface-llms-txt/SKILL.md`, use the Edit tool to insert this block immediately after the opening `---` YAML frontmatter close (i.e. on the line right after `---` that ends the frontmatter):

```markdown

> **⚠️ DEPRECATED in v1.0.** This skill has been absorbed into the unified `aisurface` skill (root `SKILL.md`).
> Use `aisurface fix .` to invoke the equivalent functionality.
> This file will be removed in v1.1.

```

For `aisurface-readme/SKILL.md`, also rewrite the description to point at the unified skill. The new `description:` line should read:

```yaml
description: DEPRECATED. Use the unified `aisurface` skill (`npx skills add ruijayfeng/aisurface`). The README-optimization capability is now part of `aisurface fix .`.
```

For `aisurface-llms-txt/SKILL.md`, the new `description:` line should read:

```yaml
description: DEPRECATED. Use the unified `aisurface` skill (`npx skills add ruijayfeng/aisurface`). The llms.txt-generation capability is now part of `aisurface fix . --only=llms_txt`.
```

- [ ] **Step 3: Verify both files now have a deprecation block at the top**

```bash
head -8 D:/Code/MyProject/aisurface/skills/_deprecated/aisurface-readme/SKILL.md
head -8 D:/Code/MyProject/aisurface/skills/_deprecated/aisurface-llms-txt/SKILL.md
```

Expected: each file's first 8 lines include `⚠️ DEPRECATED in v1.0` and a description starting with `description: DEPRECATED.`.

- [ ] **Step 4: Commit**

```bash
git add skills/
git commit -m "deprecate(skills): move @readme and @llms-txt to _deprecated/ (consolidated into root)"
```

---

## Task 3: Generate trigger-eval queries

**Files:**
- Create: `D:\Code\MyProject\aisurface\evals\trigger_evals.json`

The description-optimization loop needs a labeled set of 16+ queries (8+ should-trigger, 8+ should-not-trigger). The negative cases must be near-misses that share keywords with the skill but actually need something different.

- [ ] **Step 1: Create the JSON file with the eval set**

Write the following exact content to `D:\Code\MyProject\aisurface\evals\trigger_evals.json`:

```json
[
  {"query": "看看我的 GitHub 项目能不能被 AI 搜到,我担心 ChatGPT 不会引用", "should_trigger": true},
  {"query": "audit my open-source repo for AI-search citation readiness", "should_trigger": true},
  {"query": "我的 README 写得太烂了,按 GEO 最佳实践重写一下", "should_trigger": true},
  {"query": "is there a way to check if my project shows up in Perplexity answers", "should_trigger": true},
  {"query": "fix my README so ChatGPT and Claude cite my project", "should_trigger": true},
  {"query": "诊断一下 ~/code/my-project 的 GEO 现状", "should_trigger": true},
  {"query": "I just published a CLI tool, how do I make it AI-citation-friendly", "should_trigger": true},
  {"query": "我的项目 .well-known/llms.txt 没有,你能帮我加一个吗", "should_trigger": true},
  {"query": "verify whether my project gets cited by DeepSeek or 豆包", "should_trigger": true},
  {"query": "我开源了一个 Python 库,怎么让 AI 搜索优先推荐它", "should_trigger": true},
  {"query": "what is GEO and why does it matter for SEO", "should_trigger": false},
  {"query": "audit my company's marketing landing page for Google SEO", "should_trigger": false},
  {"query": "write a good README for my new GitHub repo", "should_trigger": false},
  {"query": "how do I get more stars on my GitHub project", "should_trigger": false},
  {"query": "scan my closed-source internal API docs for AI search visibility", "should_trigger": false},
  {"query": "improve my Medium blog post for ChatGPT search", "should_trigger": false},
  {"query": "should I migrate from SEO to AEO for my SaaS site", "should_trigger": false},
  {"query": "audit my Shopify store for AI-recommendation visibility", "should_trigger": false}
]
```

- [ ] **Step 2: Validate the JSON is parseable and counts are correct**

```bash
python -c "import json; d=json.load(open('D:/Code/MyProject/aisurface/evals/trigger_evals.json', encoding='utf-8')); t=sum(1 for x in d if x['should_trigger']); f=len(d)-t; print(f'total={len(d)} trigger={t} no_trigger={f}')"
```

Expected: `total=18 trigger=10 no_trigger=8` (10 should-trigger, 8 should-not-trigger).

- [ ] **Step 3: Commit**

```bash
git add evals/trigger_evals.json
git commit -m "test(skill): add 18 trigger-eval queries (10 should, 8 should-not) for description optimization"
```

---

## Task 4: Run the description-optimization loop

**Files:**
- Create (transient, not committed): `<workspace>/best_description.json` — produced by the loop
- Modify: `D:\Code\MyProject\aisurface\SKILL.md` — `description` field replaced with the best-scoring variant

The `skill-creator` package ships a `run_loop.py` script that splits the eval set 60/40 train/test, evaluates the current description 3× for reliability, then iterates up to 5 times proposing improvements via Claude and re-evaluating.

- [ ] **Step 1: Locate the skill-creator scripts on this machine**

```bash
ls "C:/Users/administered/.claude/skills/skill-creator/scripts/" 2>/dev/null || echo "not-found"
```

Expected output: directory listing including `run_loop.py`, `run_eval.py`, `aggregate_benchmark.py`, `package_skill.py`. If not found, stop and ask the user for the path.

- [ ] **Step 2: Run the optimization loop in the background**

```bash
python -m scripts.run_loop \
  --eval-set D:/Code/MyProject/aisurface/evals/trigger_evals.json \
  --skill-path D:/Code/MyProject/aisurface \
  --model claude-opus-4-7 \
  --max-iterations 5 \
  --verbose
```

Run in the background. Expected duration: 10–30 minutes. The script will print per-iteration scores and at the end emit `best_description` plus train/test score breakdowns.

- [ ] **Step 3: Capture the best description from the run output**

The loop output ends with a JSON block like `{"best_description": "...", "best_train_score": ..., "best_test_score": ...}`. Copy the `best_description` string verbatim.

- [ ] **Step 4: Sanity-check the new description**

The new description must:
- Start with `Use when` (or another active trigger phrase)
- Be ≤ 1024 characters
- Include at least 5 distinct natural-language trigger phrases in both English and Chinese
- Include at least one "even if …" pushy clause
- Include at least one "Do NOT trigger for …" near-miss warning

If the best_description fails any of these, manually edit it to satisfy them, then re-run Step 2 with `--eval-set` pointing at the same JSON and `--max-iterations 1` to confirm the score doesn't drop.

- [ ] **Step 5: Replace the `description:` line in `SKILL.md`**

Use the Edit tool on `D:\Code\MyProject\aisurface\SKILL.md` to replace the existing `description: Use when an open-source project maintainer ...` line with the new `description: <best_description>` line (keeping the YAML block otherwise identical).

- [ ] **Step 6: Commit**

```bash
git add SKILL.md
git commit -m "chore(skill): apply optimized description (best test score from trigger eval loop)"
```

---

## Task 5: Manual sanity check

**Files:** none (read-only verification)

- [ ] **Step 1: Verify the skill is loadable as YAML**

```bash
python -c "import yaml; d=yaml.safe_load(open('D:/Code/MyProject/aisurface/SKILL.md', encoding='utf-8').read().split('---')[1]); print('name=', d['name']); print('desc_len=', len(d['description']))"
```

Expected: `name= aisurface`, `desc_len=` is a positive integer ≤ 1024.

- [ ] **Step 2: Re-run the test suite to ensure no Python regressions**

```bash
cd D:/Code/MyProject/aisurface
python -m pytest -q
```

Expected: all 67 existing tests pass. If any fail, STOP and debug — the skill rewrite should not have touched any Python.

- [ ] **Step 3: Verify deprecation markers are in place**

```bash
grep -l "DEPRECATED in v1.0" D:/Code/MyProject/aisurface/skills/_deprecated/*/SKILL.md
```

Expected: both files listed.

- [ ] **Step 4: Verify the trigger eval file is valid**

```bash
python -c "import json; print(len(json.load(open('D:/Code/MyProject/aisurface/evals/trigger_evals.json', encoding='utf-8'))), 'queries')"
```

Expected: `18 queries`.

---

# Phase 2 — GEB Fractal Documentation Setup

The project's `CLAUDE.md` defines a 3-layer fractal documentation protocol: L1 (`/CLAUDE.md`) is the project constitution, L2 (`/{module}/CLAUDE.md`) is each module's member list and interface, L3 is `[INPUT]/[OUTPUT]/[POS]` file headers. This phase makes every layer real.

## Task 6: Update L1 `/CLAUDE.md`

**Files:**
- Modify: `D:\Code\MyProject\aisurface\CLAUDE.md`

L1 must reflect the new skill architecture (1 unified skill + 2 deprecated sub-skills), the new install story (skill-first, pip is internal), and the updated directory tree (new `docs/superpowers/`, `skills/_deprecated/`, `evals/trigger_evals.json`).

- [ ] **Step 1: Replace the L1 file in full**

Use the Write tool to replace `D:\Code\MyProject\aisurface\CLAUDE.md` with the content below.

```markdown
# aisurface — Make your open-source project surface in AI search results

> L1 | Python 3.10+ + httpx + jsonschema + selectolax + pytest + ruff

## Current State
**Shipped**: v0.1.1 (tag pushed 2026-06-02). `audit` command works end-to-end (67 tests, 4 eval fixtures).
**In progress**: v1.0 — unify 3 skills into 1, add `fix` + `verify` verbs, publish to PyPI. See `ROADMAP.md` and `docs/superpowers/plans/2026-06-02-aisurface-v100.md`.

## Architecture Principles
- **Skill-first install.** The primary user entry point is `npx skills add ruijayfeng/aisurface`. `pip install aisurface` is an implementation detail handled by the skill at first invocation. See `docs/superpowers/specs/2026-06-02-aisurface-v100-design.md` §11b.
- **User-facing abstraction.** The `SKILL.md` exposes capabilities in plain language and hides CLI flags, subcommand names, and storage paths. See same spec §3 + §11b.
- **GEB fractal docs.** L1 here, L2 in each module's `CLAUDE.md`, L3 as file-header contracts in `scripts/*.py`. Every change touches its layer.

## Directory
```
aisurface/
├── SKILL.md              - Unified skill definition (name: aisurface), single user-facing surface
├── scripts/              - Python implementation (cli, audit, report, fix/, verify/, scanner, ...)
├── skills/
│   └── _deprecated/      - v0.1.x sub-skills (aisurface-readme, aisurface-llms-txt) — will be removed in v1.1
├── tests/                - pytest suite (unit/ + integration/)
├── evals/                - Fixture-based eval suite + trigger_evals.json (for skill description optimization)
├── references/           - Knowledge base (AI platforms, schema templates, GEO checklist, llms.txt spec)
├── case-studies/         - Real-world before/after (ziwei is the canonical case)
├── docs/
│   ├── superpowers/
│   │   ├── plans/        - Implementation plans (this plan + the v1.0 plan)
│   │   └── specs/        - Specs (v1.0 design, etc.)
│   └── (user-facing docs land here)
├── .github/              - CI workflow + issue/PR templates
└── CLAUDE.md             - This file (L1)
```

## Config Files
- `pyproject.toml` — package metadata, deps, console script `aisurface = scripts.cli:main`, pytest/ruff config
- `ROADMAP.md` — release sequence (v0.1.0 → v1.0)
- `CHANGELOG.md` — release notes
- `README.md` / `README.en.md` — bilingual project README (lead with `npx skills add` + natural-language demo)
- `SKILL.md` — root skill descriptor (unified `aisurface`)

## Active Specs & Plans
- **v1.0 design**: `docs/superpowers/specs/2026-06-02-aisurface-v100-design.md` (or sibling-repo mirror)
- **v1.0 plan**: `docs/superpowers/plans/2026-06-02-aisurface-v100.md` (or sibling-repo mirror)
- **Skill optimization plan** (this one): `docs/superpowers/plans/2026-06-03-aisurface-skill-optimization-and-v1-bridge.md`

## Rule
Minimal · stable · navigation. Update on any architecture-level change (new module, file move, responsibility shift, skill structure change, install story change).

[PROTOCOL]: Update this header when changed, then check all L2 CLAUDE.md files and the L3 file headers in scripts/.
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(l1): refresh CLAUDE.md for unified skill, skill-first install, GEB layer pointers"
```

---

## Task 7: Create L2 `/scripts/CLAUDE.md`

**Files:**
- Create: `D:\Code\MyProject\aisurface\scripts\CLAUDE.md`

L2 lists every file in the module with a one-line responsibility. Per the GEB template, every line is `<file>: <responsibility>, <tech>, <key params>`.

- [ ] **Step 1: Create the file**

Write the following to `D:\Code\MyProject\aisurface\scripts\CLAUDE.md`:

```markdown
# scripts/
> L2 | Parent: /CLAUDE.md | Python 3.10+ stdlib + httpx + jsonschema + selectolax

## Member List
- `__init__.py`: Package marker, no logic.
- `cli.py`: CLI entry point, thin dispatcher to `audit` / `fix` / `verify` subcommands. `argparse` subparsers. Console-script target `aisurface = scripts.cli:main`.
- `audit.py`: 12-check GEO audit logic. Returns `AuditReport`. Pure function over `RepoAssets` + README text.
- `report.py`: Render `AuditReport` as Markdown. Owns 40/30/20/10 weighted health score, must-fix/should-fix/nice-to-have bucketing. Exports `AuditReport`, `CheckResult`, `CATEGORY_CHECK_IDS`, `CATEGORY_WEIGHTS`, `_compute_health_score`.
- `scanner.py`: Walk a repo and build `RepoAssets` (README path, project_type, llms.txt presence, schema files). Prunes `node_modules`/`.venv`/`dist`/etc.
- `findings.py`: Defines `StructuralFinding` (subclass of `CheckResult` carrying a `file_path`).
- `critic.py`: Semantic check heuristics (regex over README). Pre-LLM stub; `--llm` flag in v0.1.4 swaps this for a real LLM call.
- `github_meta.py`: GitHub topics count + repo description lookup (uses `gh` CLI, not API).
- `distribution.py`: Distribution-signal heuristic (awesome-list mention, npm/PyPI presence).
- `concepts.py`: 1-2 sentence teacher-mode primers for each of the 12 checks, loaded by `--learn`.
- `colors.py`: ANSI colorize wrapper with `NO_COLOR=1` / `--no-color` opt-out.
- `safe_check.py`: Decorator that wraps each check in try/except, turns failures into `skipped` results with an `error` field.
- `llms_txt.py`: Build a valid llms.txt body per https://llmstxt.org. `build_llms_txt(project_name, description, sections, details)` and `write_llms_txt(repo, ...)`.
- `schema_gen.py`: Build Schema.org JSON-LD objects. `build_software_application(...)`, `build_faq_page(questions)`.
- `probe.py`: Legacy stub from v0.1. Will be removed in v0.1.3 when `scripts/verify/` lands.

## Pending (v0.1.2 — fix verb)
- `fix/__init__.py`: Patch dataclass + `cmd_fix` dispatcher.
- `fix/faq.py`: FAQ-section injection patch (templated 8 Q&A per project type).
- `fix/when_to_use.py`: When-to-use / When-NOT-to-use stub patch.
- `fix/llms_txt.py`: Wraps `llms_txt.py` for the fix context.
- `fix/schema_org.py`: Wraps `schema_gen.py` for the fix context.

## Pending (v0.1.3 — verify verb)
- `verify/__init__.py`: `ProbeAdapter` Protocol + `ProbeResult` dataclass + `cmd_verify` dispatcher.
- `verify/perplexity.py`: `PerplexityAdapter` over httpx.
- `verify/queries.py`: Per-project-type query template generator.
- `verify/baseline.py`: File-backed `BaselineStore` at `~/.aisurface/baselines/<hash>/<platform>.json` + `diff_summary`.

## Rule
One file, one responsibility. No file > 800 lines. If a file grows, split by responsibility, not by technical layer. Every file has an L3 `[INPUT]/[OUTPUT]/[POS]` header at the top — see the GEB protocol in `/CLAUDE.md`.

[PROTOCOL]: Update this header when a file is added, deleted, renamed, or its responsibility/interface changes. Then check the L1 `/CLAUDE.md` directory tree.
```

- [ ] **Step 2: Commit**

```bash
git add scripts/CLAUDE.md
git commit -m "docs(l2): add scripts/CLAUDE.md module map (existing + pending fix/verify files)"
```

---

## Task 8: Create L2 `/skills/CLAUDE.md`

**Files:**
- Create: `D:\Code\MyProject\aisurface\skills\CLAUDE.md`

- [ ] **Step 1: Create the file**

Write the following to `D:\Code\MyProject\aisurface\skills\CLAUDE.md`:

```markdown
# skills/
> L2 | Parent: /CLAUDE.md

## Member List
- (root `SKILL.md` lives at /SKILL.md, not in this directory — single unified `aisurface` skill)
- `_deprecated/aisurface-readme/SKILL.md`: DEPRECATED in v1.0. Was the README-optimization sub-skill. Capability now in `aisurface fix .`.
- `_deprecated/aisurface-llms-txt/SKILL.md`: DEPRECATED in v1.0. Was the llms.txt-generation sub-skill. Capability now in `aisurface fix . --only=llms_txt`.

## Invariants
- Exactly ONE user-facing skill in this project: the root `/SKILL.md` (name: `aisurface`).
- Deprecated sub-skill files are kept for one release (v1.0) and removed in v1.1.
- No new sub-skills will be added — the v1.0 design §4 explicitly kills the "skill collection" model.

## Rule
Do not create new entries under `skills/` without updating the v1.0 spec. All new skill-shaped functionality must fold into the unified `/SKILL.md`.

[PROTOCOL]: Update this header when the unified SKILL.md is rewritten or a deprecated sub-skill is removed.
```

- [ ] **Step 2: Commit**

```bash
git add skills/CLAUDE.md
git commit -m "docs(l2): add skills/CLAUDE.md module map (single unified skill + 2 deprecated)"
```

---

## Task 9: Create L2 `/references/CLAUDE.md`

**Files:**
- Create: `D:\Code\MyProject\aisurface\references\CLAUDE.md`

- [ ] **Step 1: Create the file**

Write the following to `D:\Code\MyProject\aisurface\references\CLAUDE.md`:

```markdown
# references/
> L2 | Parent: /CLAUDE.md

## Member List
- `ai-search-platforms.md`: List of 11 AI search platforms aisurface tracks (ChatGPT, Perplexity, Claude, Gemini, 豆包, DeepSeek, 文心一言, 通义千问, Kimi, 智谱, GLM) plus per-platform citation characteristics. Loaded when the user names a specific platform.
- `schema-templates.md`: Schema.org JSON-LD templates (SoftwareApplication, FAQPage). Loaded when the user asks about structured data / schema markup.
- `citation-patterns.md`: What makes AI cite vs ignore content. Loaded when the user asks "why doesn't AI cite me" or wants README rewrite guidance.
- `llms-txt-spec.md`: The llmstxt.org specification. Loaded when the user asks about llms.txt or wants to generate one.
- `readme-checklist.md`: 12-item GEO README checklist. Loaded when the user wants README optimization guidance.

## Invariants
- These are knowledge-base files, loaded on demand by the skill's agent (not auto-loaded).
- No file in this directory should be longer than 300 lines without an internal table of contents (per the GEB progressive-disclosure rule).
- The trigger-eval table in the root `SKILL.md` ("何时加载 references/") is the single source of truth for which file is read when.

## Rule
Add a new reference file only when the SKILL.md gains a new trigger phrase that needs deeper knowledge than fits in the body.

[PROTOCOL]: Update this header when a reference is added, removed, or its loading trigger changes.
```

- [ ] **Step 2: Commit**

```bash
git add references/CLAUDE.md
git commit -m "docs(l2): add references/CLAUDE.md module map (5 knowledge-base files + load triggers)"
```

---

## Task 10: Create L2 `/tests/CLAUDE.md`

**Files:**
- Create: `D:\Code\MyProject\aisurface\tests\CLAUDE.md`

- [ ] **Step 1: Create the file**

Write the following to `D:\Code\MyProject\aisurface\tests\CLAUDE.md`:

```markdown
# tests/
> L2 | Parent: /CLAUDE.md

## Member List
- `unit/`: Pure unit tests (each script's logic in isolation). Currently covers `audit`, `scanner`, `report`, `colors`, `concepts`, `safe_check`, `llms_txt`, `schema_gen`, `critic`, `findings`, `distribution`, `github_meta`.
- `integration/`: End-to-end tests that run the CLI as a subprocess. Currently `test_full_audit.py` exercises `python -m scripts.cli audit <fixture> --json` against the 4 eval fixtures.
- `evals/` (NOTE: this is a different directory — the eval fixtures live at `/evals/`, not under tests).

## Invariants
- 67 tests passing as of v0.1.1.
- Marker `eval` is defined in `pyproject.toml`; deselect with `pytest -m "not eval"`.
- Every new `scripts/*.py` file must have a corresponding `tests/unit/test_<name>.py`.

## Pending test files (from v1.0 plan)
- `unit/test_cli_dispatch.py`, `test_fix_faq.py`, `test_fix_when_to_use.py`, `test_fix_llms_txt.py`, `test_fix_schema_org.py`, `test_verify_protocol.py`, `test_verify_perplexity.py`, `test_verify_queries.py`, `test_verify_baseline.py`
- `integration/test_full_fix.py`, `test_full_verify.py`

## Rule
No fix without a failing test first. TDD is mandatory for new functionality in `scripts/`.

[PROTOCOL]: Update this header when a new test file is added, a test category is introduced, or the marker system changes.
```

- [ ] **Step 2: Commit**

```bash
git add tests/CLAUDE.md
git commit -m "docs(l2): add tests/CLAUDE.md module map (unit + integration + pending from v1.0 plan)"
```

---

## Task 11: Create L2 `/evals/CLAUDE.md`

**Files:**
- Create: `D:\Code\MyProject\aisurface\evals\CLAUDE.md`

- [ ] **Step 1: Create the file**

Write the following to `D:\Code\MyProject\aisurface\evals\CLAUDE.md`:

```markdown
# evals/
> L2 | Parent: /CLAUDE.md

## Member List
- `fixtures/`: 4 hand-crafted OSS-project fixtures used by integration tests + the audit verb.
  - `minimal-cli-tool/`: Bare-minimum CLI in TypeScript. Used to verify "no false positives" on an already-clean project.
  - `bad-readme-python-lib/`: Python lib with intentional GEO gaps. Used to verify the audit catches all must-fix items + the v0.1.2 `fix` verb improves the score.
  - 2 other fixtures (see `fixtures/`).
- `expected_patches/`: (Pending v0.1.2) Snapshot directory of expected `fix` patch outputs per fixture, used by `test_full_fix.py::test_patches_match_snapshot`.
- `trigger_evals.json`: 18 labeled trigger queries (10 should-trigger, 8 should-not-trigger) for `skill-creator` description optimization. Used by the v1.0-onwards SKILL.md description loop.

## Invariants
- Fixture count is stable (4) — adding/removing a fixture is an L1 architecture change.
- `trigger_evals.json` is the single source of truth for "should this skill trigger" evaluation. Update it whenever the SKILL.md description changes meaningfully.

## Rule
Hand-craft fixtures to cover both happy-path (clean) and adversarial (intentionally bad) cases. Avoid auto-generated fixtures — they hide bugs.

[PROTOCOL]: Update this header when a fixture is added/removed or `trigger_evals.json` structure changes.
```

- [ ] **Step 2: Commit**

```bash
git add evals/CLAUDE.md
git commit -m "docs(l2): add evals/CLAUDE.md module map (4 fixtures + trigger_evals.json)"
```

---

## Task 12: Add L3 file headers to all `scripts/*.py` files

**Files (the 14 existing files in `D:\Code\MyProject\aisurface\scripts/` — `audit.py` does not exist yet; it will be created in v0.1.2 per the v1.0 plan's Task 1. The L3 header for `audit.py` is captured in the v1.0 plan instead of here):**
- `__init__.py`, `cli.py`, `report.py`, `scanner.py`, `findings.py`, `critic.py`, `github_meta.py`, `distribution.py`, `concepts.py`, `colors.py`, `safe_check.py`, `llms_txt.py`, `schema_gen.py`, `probe.py`

L3 is the per-file INPUT/OUTPUT/POS contract. Format from the project GEB template:

```python
"""
 * [INPUT]: Depends on {module/file}'s {specific capability}
 * [OUTPUT]: Provides {exported functions/components/types/constants}
 * [POS]: {Module} {role positioning}, {relationship with sibling files}
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""
```

Use this exact block at the top of each file (replacing the existing module docstring if any — keep the original content after the L3 block).

- [ ] **Step 1: Add L3 header to `__init__.py`**

Prepend the following L3 block (then keep the existing empty file content):

```python
"""
 * [INPUT]: None.
 * [OUTPUT]: Marks `scripts` as a Python package. No exports.
 * [POS]: Root of the `scripts/` module, imported by CLI entry point and by tests.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""
```

- [ ] **Step 2: Add L3 header to `cli.py`**

Prepend:

```python
"""
 * [INPUT]: Depends on `argparse` (stdlib), `scripts.audit.cmd_audit` (extracted into a separate file in v0.1.2), `scripts.fix.cmd_fix` (pending v0.1.2), `scripts.verify.cmd_verify` (pending v0.1.3), `scripts.colors.colorize`.
 * [OUTPUT]: Provides `build_parser()`, `main(argv)`, console-script target `aisurface = scripts.cli:main`.
 * [POS]: Single CLI entry point. Dispatches to audit/fix/verify subcommands. Imported by `pyproject.toml`'s `[project.scripts]`.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""
```

(Note: the audit logic currently lives inline in `cli.py`. It will be extracted to `scripts/audit.py` in v0.1.2 per the v1.0 plan's Task 1. The L3 header for `audit.py` is part of the v0.1.2 task, not this plan.)

- [ ] **Step 3: Add L3 header to `report.py`**

Prepend:

```python
"""
 * [INPUT]: Depends on `scripts.findings.StructuralFinding` (lazy-imported via __getattr__ to avoid circular import), `scripts.concepts.get_primer` (lazy-imported for `--learn` mode).
 * [OUTPUT]: Provides `AuditReport`, `CheckResult` dataclasses; `CATEGORY_WEIGHTS` (40/30/20/10), `CATEGORY_CHECK_IDS`, `CATEGORY_LABELS`; `render_report(report, teacher_mode, wrap)`, `_compute_health_score(categories)`, `_compute_sub_scores(results)`, `_bucket_results(results)`, `_format_check_line(r, ...)`.
 * [POS]: Reporting layer. Imported by `audit.py` (to construct results) and `cli.py` (to render). Owns the weighted-score math and must/should/nice bucketing.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""
```

- [ ] **Step 4: Add L3 header to `scanner.py`**

Prepend:

```python
"""
 * [INPUT]: Depends on `pathlib`, `os.walk`, `fnmatch` (stdlib). No internal deps.
 * [OUTPUT]: Provides `scan_repo(root) -> RepoAssets` dataclass, `RepoAssets.to_dict()`, `PROJECT_MARKERS`, `IGNORE_DIRS`, `_detect_project_type(root)`, `_iter_relevant_files(root, pattern)`.
 * [POS]: Repo-inventory layer. Called by `audit.run_audit` and (pending) `fix.cmd_fix` and `verify.cmd_verify`. The single source of truth for "what files does this project have".
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""
```

- [ ] **Step 5: Add L3 header to `findings.py`**

Prepend:

```python
"""
 * [INPUT]: Depends on `scripts.report.CheckResult` (parent class).
 * [OUTPUT]: Provides `StructuralFinding(CheckResult)` dataclass with extra `file_path: Path | None` field.
 * [POS]: Subclass of `CheckResult` used by structural checks (e.g., Schema.org, llms.txt, GitHub topics) that need to point at a specific file. Imported lazily by `report.py` to avoid a circular import.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""
```

- [ ] **Step 6: Add L3 header to `critic.py`**

Prepend:

```python
"""
 * [INPUT]: Depends on `scripts.report.CheckResult` and `scripts.safe_check.safe_check`.
 * [OUTPUT]: Provides `offline_critique(readme, ...) -> list[CheckResult]` (regex-based semantic checks for checks #1, #2, #3, #4, #8, #9, #10, #12).
 * [POS]: Semantic-check layer. The `--llm` flag in v0.1.4 will introduce `llm_critique(...)` as a parallel strategy selectable by the CLI; until then `offline_critique` is the only path.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""
```

- [ ] **Step 7: Add L3 header to `github_meta.py`**

Prepend:

```python
"""
 * [INPUT]: Depends on `subprocess` (stdlib, shells out to `gh` CLI), `scripts.report.CheckResult`.
 * [OUTPUT]: Provides `github_topics_count(repo_root) -> int`, `github_repo_description(repo_root) -> str | None`, and a CheckResult for check #7.
 * [POS]: GitHub-specific data source. Used by `audit.run_audit` to score check #7 (GitHub topics count). Skipped (returns CheckResult with `skipped=True`) if `gh` CLI is unavailable.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""
```

- [ ] **Step 8: Add L3 header to `distribution.py`**

Prepend:

```python
"""
 * [INPUT]: Depends on `scripts.scanner.RepoAssets`, `scripts.report.CheckResult`.
 * [OUTPUT]: Provides `distribution_check(assets) -> CheckResult` for check #11 (awesome-list / npm / PyPI presence).
 * [POS]: Distribution-signal heuristic. Imported by `audit.run_audit`. Pure function over `RepoAssets` — no network.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""
```

- [ ] **Step 9: Add L3 header to `concepts.py`**

Prepend:

```python
"""
 * [INPUT]: Depends on stdlib only.
 * [OUTPUT]: Provides `PRIMERS: dict[int, str]` (12 check-id → 1-2 sentence primer), `get_primer(check_id) -> str`.
 * [POS]: Knowledge layer for `--learn` teacher mode. Imported lazily by `report._format_check_line` only when `teacher_mode=True`.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""
```

- [ ] **Step 10: Add L3 header to `colors.py`**

Prepend:

```python
"""
 * [INPUT]: Depends on `os` (reads `NO_COLOR` env var), `sys` (detects TTY).
 * [OUTPUT]: Provides `colorize(text, color) -> str` — wraps text in ANSI codes; returns text unchanged if `NO_COLOR=1` or stdout is not a TTY.
 * [POS]: Presentation layer. Imported by `cli.py` and `audit.py` to color the rendered report. The `wrap=` parameter in `report.render_report` is this function by convention.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""
```

- [ ] **Step 11: Add L3 header to `safe_check.py`**

Prepend:

```python
"""
 * [INPUT]: Depends on stdlib `functools` only.
 * [OUTPUT]: Provides `@safe_check` decorator that catches exceptions raised inside a check function and converts them to a `CheckResult` with `skipped=True` and an `error` field.
 * [POS]: Reliability layer. Wraps every check in `audit.run_audit` so one bad check never aborts the whole audit. Imported by `audit.py`.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""
```

- [ ] **Step 12: Add L3 header to `llms_txt.py`**

Prepend:

```python
"""
 * [INPUT]: Depends on `pathlib`, `typing.TypedDict` (stdlib).
 * [OUTPUT]: Provides `Link`, `Section` TypedDicts; `build_llms_txt(project_name, description, sections, details) -> str`; `write_llms_txt(repo_root, project_name, description, sections, details) -> Path`.
 * [POS]: llms.txt generation per https://llmstxt.org. Used by the audit verb's check #6 (to test if file exists) and (pending v0.1.2) by `fix/llms_txt.py` to generate the file.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""
```

- [ ] **Step 13: Add L3 header to `schema_gen.py`**

Prepend:

```python
"""
 * [INPUT]: Depends on `typing.Any` (stdlib).
 * [OUTPUT]: Provides `build_software_application(name, description, url, *, application_category, operating_system, offers, author) -> dict[str, Any]`; `build_faq_page(questions) -> dict[str, Any]`.
 * [POS]: Schema.org JSON-LD builder. Used by the audit verb's check #5 (to test if a schema file exists) and (pending v0.1.2) by `fix/schema_org.py` to produce `index.schema.json`.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""
```

- [ ] **Step 14: Add L3 header to `probe.py`**

Prepend:

```python
"""
 * [INPUT]: Depends on stdlib `dataclasses`, `typing.Protocol`.
 * [OUTPUT]: Provides `ProbeAdapter` Protocol (stub), `ProbeResult` dataclass, `probe_stub(prompt, platform) -> ProbeResult` (always returns `cited=False`).
 * [POS]: Legacy stub from v0.1. Will be deleted in v0.1.3 when `scripts/verify/` lands. Currently imported only by tests and by the `--probe` placeholder in the audit output; safe to remove once v0.1.3 ships.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md
"""
```

- [ ] **Step 15: Verify all headers parse correctly**

```bash
cd D:/Code/MyProject/aisurface
for f in scripts/*.py; do
  python -c "import ast; ast.parse(open('$f', encoding='utf-8').read())" && echo "OK: $f" || echo "FAIL: $f"
done
```

Expected: every file prints `OK:`. If any file prints `FAIL:`, fix the syntax (likely a triple-quote mismatch) and re-run.

- [ ] **Step 16: Commit**

```bash
git add scripts/*.py
git commit -m "docs(l3): add INPUT/OUTPUT/POS file headers to all 14 script files"
```

---

# Phase 3 — v1.0 Bridge (spec / plan / roadmap / README updates)

## Task 13: Add user-facing-abstraction principle to v1.0 spec

**Files:**
- Modify: `D:\Code\MyProject\SkillsCreate\InitSkill\docs\superpowers\specs\2026-06-02-aisurface-v100-design.md`

The v1.0 design spec needs a new section that codifies the "user-facing abstraction" principle (skill-first install, natural-language triggers, no exposed flags). This is the doctrine that the SKILL.md, the README, and the v0.1.2+ work all hang off of.

- [ ] **Step 1: Insert a new section §11b after the existing §11 ("Open Questions") and before §12 ("What Changes for the User")**

Find the `## 12. What Changes for the User` heading. Insert the following block immediately above it:

```markdown
## 11b. User-Facing Abstraction Principle

**Rule**: Every artifact the user sees — the `SKILL.md`, the README, the report output, the CLI `--help` — must expose *capabilities* in plain language, never *implementation details*.

**Concretely, this means:**

- The `SKILL.md` is a user interface. It lists **3 capabilities** (diagnose / treat / prove) in plain language, with **natural-language trigger phrases**, **what the user will see**, and **what they need to provide**. It does NOT mention CLI subcommand names (`audit` / `fix` / `verify`), flag names (`--dry-run` / `--yes` / `--only`), check IDs (#1–#12), weighted-score formulas (40/30/20/10), or storage paths (`~/.aisurface/baselines/`). The internal command names, flags, and storage are exposed only in a separate "agent-only" section at the bottom of the SKILL.md that the agent reads but does not show to the user.
- The README's first code block is `npx skills add ruijayfeng/aisurface`, followed by a natural-language demo ("跟我说'诊断我的项目'就行"). `pip install aisurface` is mentioned only in an "Advanced" section.
- The CLI's `--help` text is a separate concern from the SKILL.md. The `--help` is for power users / CI; the SKILL.md is for everyone else.
- Cross-references between skill files are forbidden. Each skill (in v1.0 there is only one) is independently understandable and triggerable.

**Why this matters**: The current v0.1.1 SKILL.md is a developer's doc masquerading as a user doc. It lists 12 check IDs, mentions a `--patch` flag that does not exist, references sub-skills (`aisurface@probe`, `aisurface@schema`) that do not exist, and exposes Python module names in user-facing text. Every one of these is a "Linus bad taste" violation: each is a special case the user has to learn before they can use the tool. The v1.0 SKILL.md and README are the cleanup.

**Skill-first install (sub-rule)**: The primary install path is `npx skills add ruijayfeng/aisurface`. The skill handles Python environment setup (`pip install aisurface` if needed) on first invocation, with a single user prompt for permission. `pip install aisurface` as a standalone install is supported for CI and non-Claude-Code users, but it is NOT the recommended path. See §12 (install row of the comparison table, which now leads with the skill install).
```

- [ ] **Step 2: Update the §12 comparison table to reflect the new install story**

Find the §12 table row that begins with `| Install |`. Replace that single row with:

```markdown
| Install | `npx skills add ruijayfeng/aisurface@audit` (and 2 more for other skills) | `npx skills add ruijayfeng/aisurface` (handles `pip install aisurface` internally); `pip install aisurface` standalone is supported for CI / non-Claude-Code users but is not the recommended path |
```

- [ ] **Step 3: Commit**

```bash
cd D:/Code/MyProject/SkillsCreate/InitSkill
git add docs/superpowers/specs/2026-06-02-aisurface-v100-design.md
git commit -m "docs(spec): add §11b user-facing abstraction principle; flip §12 install story to skill-first"
```

---

## Task 14: Update v1.0 plan tasks 15/16/17/18

**Files:**
- Modify: `D:\Code\MyProject\SkillsCreate\InitSkill\docs\superpowers\plans\2026-06-02-aisurface-v100.md`

The v1.0 plan's Tasks 15 (deprecate sub-skills), 16 (rewrite root SKILL.md), 17 (README polish + screenshots), and 18 (PyPI publish) all need to be updated to reflect the new abstraction principle.

- [ ] **Step 1: Update Task 15 to reference the new abstraction principle**

In Task 15, find the line "Move: `skills/aisurface-readme/SKILL.md` → ...". Immediately above the `**Files:**` block, insert this paragraph:

```markdown
**Pre-work**: This task implements the "User-Facing Abstraction Principle" codified in `2026-06-02-aisurface-v100-design.md` §11b. Read that section first; the deprecation, the SKILL.md rewrite, and the README rewrite are all in service of that one principle.
```

- [ ] **Step 2: Update Task 16 (Rewrite Root SKILL.md) to use the new design**

Replace the entire body of Task 16 (from `**Files:**` through the end of the `Step 2: Commit` block) with the version below. The new body is shorter because the content has already been written in Phase 1 of the skill-optimization plan; the v1.0 plan task now just verifies and integrates.

```markdown
### Task 16: Rewrite Root SKILL.md (integration verification)

**Files:**
- Verify: `/SKILL.md` (was rewritten in `2026-06-03-aisurface-skill-optimization-and-v1-bridge.md` Task 1)
- Verify: `evals/trigger_evals.json` (was created in Task 3 of the same plan)
- Verify: `description` field has been run through `skill-creator`'s `run_loop` and the best-scoring variant is committed (Task 4 of the same plan)

**Principle (from spec §11b)**: The SKILL.md is a user interface, not a developer doc. It exposes 3 capabilities in plain language with natural-language trigger phrases. Internal command names, flag names, check IDs, and storage paths live in a separate "agent-only" section at the bottom.

- [ ] **Step 1: Verify the rewritten SKILL.md matches the §11b invariants**

Open `/SKILL.md` and confirm:
- [ ] `name: aisurface` (not `aisurface-audit`)
- [ ] `description` field starts with `Use when`, includes ≥ 5 trigger phrases in both English and Chinese, includes an "even if …" clause, includes a "Do NOT trigger for" warning, and is ≤ 1024 characters
- [ ] No mention of `--patch`, `aisurface@probe`, `aisurface@schema`, "v0.1", "v0.3" anywhere in user-visible text
- [ ] The "agent-only" section at the bottom has the tool-call table, references-load table, error-handling, and output-format constraints

If any invariant fails, fix it in the SKILL.md directly. Do not rewrite from scratch.

- [ ] **Step 2: Verify the trigger-eval set exists and is loadable**

```bash
python -c "import json; d=json.load(open('evals/trigger_evals.json', encoding='utf-8')); assert len(d) >= 16, 'need at least 16 queries'; t=sum(1 for x in d if x['should_trigger']); f=len(d)-t; assert t >= 8 and f >= 8, f'unbalanced: trigger={t} no_trigger={f}'; print(f'OK: {len(d)} queries ({t} trigger, {f} no-trigger)')"
```

Expected: `OK: 18 queries (10 trigger, 8 no-trigger)`.

- [ ] **Step 3: Run the test suite**

```bash
python -m pytest -q && python -m ruff check .
```

Expected: 67 tests pass, ruff clean. If anything fails, STOP — the SKILL.md rewrite is supposed to be markdown-only and must not have touched Python.

- [ ] **Step 4: Commit (only if Steps 1–3 required fixes)**

```bash
git add SKILL.md evals/trigger_evals.json
git commit -m "docs(skill): align root SKILL.md with v1.0 spec §11b abstraction principle"
```

If no fixes were needed, no commit. The skill optimization plan already produced the commits.
```

- [ ] **Step 3: Update Task 17 (README Polish) to lead with the skill install**

Find Task 17 Step 2 ("Rewrite README top section"). Replace the entire step-2 markdown block (from the heading `# aisurface` through the end of the new opening code block) with the version below.

```markdown
```markdown
# aisurface

> 让你的开源项目在 AI 搜索结果里浮到表面。

## 安装

```bash
npx skills add ruijayfeng/aisurface
```

装完跟我说一句"诊断我的项目"就行,Python 环境我自己处理。

## 怎么用

```text
"看看我的项目能不能被 AI 搜到"          →  诊断
"按 AI 搜索最佳实践改我的项目"          →  修
"现在 AI 真的引用我项目了吗"            →  验证
```

下面三张截图分别展示三个动作的实际效果(占位,真正的截图在 docs/screenshots/)：

![audit](docs/screenshots/audit.png)
![fix](docs/screenshots/fix.png)
![verify](docs/screenshots/verify.png)

[... rest of README ...]
```

(The English version `README.en.md` gets the same treatment in Step 3 of Task 17. The spec is bilingual; both READMEs are required.)

Step 3 of Task 17 ("Re-dogfood on ziwei") is unchanged.

Step 1 of Task 17 ("Capture screenshots") is unchanged.

- [ ] **Step 4: Update Task 18 (PyPI Publish) — change priority framing**

Find Task 18 ("PyPI Publish Prep"). Add a one-paragraph pre-amble at the top of the task body (above the existing `**Files:**` line):

```markdown
**Framing**: PyPI publish is no longer the primary install path (see spec §11b — skill-first install is). PyPI publish is required for: (a) the skill to be able to do `pip install aisurface` on first invocation when the user doesn't already have it, and (b) CI / non-Claude-Code users. The metadata requirements below are unchanged.
```

- [ ] **Step 5: Commit**

```bash
cd D:/Code/MyProject/SkillsCreate/InitSkill
git add docs/superpowers/plans/2026-06-02-aisurface-v100.md
git commit -m "docs(plan): align Tasks 15/16/17/18 with v1.0 spec §11b abstraction principle"
```

---

## Task 15: Update `ROADMAP.md`

**Files:**
- Modify: `D:\Code\MyProject\aisurface\ROADMAP.md`

- [ ] **Step 1: Add a "Install story" line under the "## Final Form: v1.0" section**

Find the heading `## Final Form: v1.0` and the existing "**Full v1.0 spec**" line. Insert this block between the closing code block (`\`\`\``) and the "**Full v1.0 spec**" line:

```markdown
**Install**: `npx skills add ruijayfeng/aisurface` is the primary path. The skill handles `pip install aisurface` internally on first invocation. `pip install aisurface` standalone is supported for CI and non-Claude-Code users.
```

- [ ] **Step 2: Update the v1.0.0 release row in the table**

Find the row that begins with `| **v1.0.0** |`. Replace that row with:

```markdown
| **v1.0.0** | **Consolidate 3 skills → 1 unified `aisurface` skill, PyPI publish, screenshots, ziwei re-dogfood** | ⏳ planned |
```

- [ ] **Step 3: Commit**

```bash
git add ROADMAP.md
git commit -m "docs(roadmap): align v1.0 install story and release description with new skill model"
```

---

## Task 16: Update `README.md` and `README.en.md` tops

**Files:**
- Modify: `D:\Code\MyProject\aisurface\README.md`
- Modify: `D:\Code\MyProject\aisurface\README.en.md`

Both READMEs currently lead with the old 3-skill install story. v1.0 leads with the unified skill install.

- [ ] **Step 1: Replace the "## 安装" / "## Installation" section in both files**

In `README.md`, find the section that begins with `## 安装` and ends right before `## 快速开始`. Replace that section with:

```markdown
## 安装

主路径(推荐):

```bash
npx skills add ruijayfeng/aisurface
```

装完跟我说一句"诊断我的项目"就行,Python 环境我自己处理。

备选(给 CI 或不用 Claude Code 的人):

```bash
pip install aisurface
aisurface audit ./
```
```

In `README.en.md`, do the equivalent replacement for the `## Installation` section (English equivalents):

```markdown
## Installation

Primary path (recommended):

```bash
npx skills add ruijayfeng/aisurface
```

After install, just say "audit my project" — the skill handles the Python environment itself.

Alternative (for CI or non-Claude-Code users):

```bash
pip install aisurface
aisurface audit ./
```
```

- [ ] **Step 2: Verify both READMEs still render their bilingual switcher at the top**

```bash
head -10 D:/Code/MyProject/aisurface/README.md
head -10 D:/Code/MyProject/aisurface/README.en.md
```

Expected: both files begin with `# aisurface` and the bilingual link (`[English](./README.en.md) | 中文` in one, `[中文](./README.md) | English` in the other).

- [ ] **Step 3: Commit**

```bash
git add README.md README.en.md
git commit -m "docs(readme): lead with npx skills add (skill-first install per spec §11b)"
```

---

# Done Criteria Checklist

After all 16 tasks complete, verify:

- [ ] `/SKILL.md` has `name: aisurface` (not `aisurface-audit`) and the description has been run through `skill-creator`'s `run_loop` optimizer
- [ ] `skills/_deprecated/aisurface-readme/SKILL.md` and `skills/_deprecated/aisurface-llms-txt/SKILL.md` both have the deprecation notice and the `description: DEPRECATED.` first line
- [ ] `evals/trigger_evals.json` has ≥ 16 queries (≥ 8 should-trigger, ≥ 8 should-not-trigger) and is valid JSON
- [ ] `/CLAUDE.md` reflects the new skill architecture, the skill-first install story, and the GEB layer pointers
- [ ] `scripts/CLAUDE.md`, `skills/CLAUDE.md`, `references/CLAUDE.md`, `tests/CLAUDE.md`, `evals/CLAUDE.md` all exist and follow the GEB L2 template
- [ ] All 14 `scripts/*.py` files have an L3 `[INPUT]/[OUTPUT]/[POS]/[PROTOCOL]` block at the top and pass `ast.parse`
- [ ] The v1.0 spec (`..\SkillsCreate\InitSkill\docs\superpowers\specs\2026-06-02-aisurface-v100-design.md`) has the new §11b section and the §12 install row updated
- [ ] The v1.0 plan (`..\SkillsCreate\InitSkill\docs\superpowers\plans\2026-06-02-aisurface-v100.md`) has the abstraction-principle pre-amble in Tasks 15/16 and the new README code block in Task 17
- [ ] `ROADMAP.md` and `README.md` / `README.en.md` lead with the `npx skills add` story
- [ ] `python -m pytest -q` still passes 67 tests; `python -m ruff check .` is clean
- [ ] Total commits added by this plan: 13 (Tasks 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 15, 16 — Task 13/14 are in the sibling repo; Task 4 may or may not commit; Task 5 commits nothing)

---

# Notes for Implementers

- **Use subagent-driven-development.** Tasks 1, 6, 7, 8, 9, 10, 11 (the 6 L2-doc tasks) are independent — dispatch them in parallel after Task 12 is done. Task 12 itself is parallelizable per file (14 subagents, one per `scripts/*.py`).
- **Task 4 (`run_loop`) is a long-running step.** Plan for 10–30 minutes. Do not block other work on it; do the L1/L2/L3 doc work in parallel.
- **Skill-creator scripts location**: `C:\Users\administered\.claude\skills\skill-creator\scripts\run_loop.py`. If not present, stop and ask the user.
- **Sibling-repo awareness**: Tasks 13 and 14 modify files in `D:\Code\MyProject\SkillsCreate\InitSkill\`, not in the `aisurface` repo. The implementer must `cd` into the sibling repo for those commits.
- **The v1.0 implementation work itself is OUT OF SCOPE for this plan.** This plan sets up the documentation and skill surface; the v1.0 features (`fix` verb, `verify` verb, PyPI publish, screenshots) are in the existing `2026-06-02-aisurface-v100.md` plan, which Tasks 13 and 14 of this plan bring into alignment with the new abstraction principle.

*End of plan.*

---
name: aisurface
description: 'Use when an open-source project maintainer wants their project to surface in AI search results across ChatGPT, Perplexity, Claude, Gemini, 豆包, DeepSeek, 文心一言, 通义千问, Kimi, 智谱, GLM. Triggers on any of: "audit my project for AI search", "is my project AI-citation-friendly", "GEO audit", "improve AI discoverability", "make my project AI-search-ready", "does my project show up in AI search", "fix my README for ChatGPT", "AI 搜索能不能搜到我的项目", "诊断我的项目 GEO", "按 AI 搜索最佳实践改 README", "AI 真的引用我项目了吗", "verify AI platform citation rate", or any request to improve a GitHub repo''s citation-friendliness. Even if the user only mentions one concern (e.g., "我的项目 ChatGPT 搜不到" or "我的 README 写得不好") this skill applies. Do NOT trigger for: general questions about what GEO is, questions about closed-source or marketing sites, or SEO for non-AI-search engines.'
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
| "装对没 / 为什么命令找不到 / 装坏了 / diagnose install / is my aisurface broken" | 调 `python -m scripts.cli doctor --no-color`。读输出,把 ✗ 行的 `→ ...` 提示直接转给用户。PyPI 显示有新版本(`⚠ ... available`)就追加一句"要不要 `pip install --upgrade aisurface`"。如果 `PERPLEXITY_API_KEY` 是 ⚠,提醒"以后用 `verify` 之前先设上"但**不强制**用户设 |
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

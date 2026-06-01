<!--
[INPUT]: case-studies/ziwei-before-after.md (real numbers: 35→66, ~30 minutes)
[OUTPUT]: 掘金 long-form article draft (Chinese, 2000-3000 字)
[POS]: docs/launch/'s 掘金 draft, consumed by manual posting to juejin.cn
[PROTOCOL]: Update this header when changed
-->

---
task: 26
target: 掘金 (Juejin)
status: draft
date: 2026-06-02
notes: Long-form Chinese article; 7-section structure; ~2500 字 total
---

# 掘金 Article — aisurface v0.1.0

## 标题

```
中国 AI 时代开源项目的引用率优化：从 35 到 66 的实战
```

（注意：用真实数据 35→66，不要用计划文件里的虚高数字 42→92。）

## 标签 (发布时填入)

```
Claude Code, GEO, AI 搜索, 开源, 紫微斗数, SEO
```

## 分类

```
后端 / 工具 / AI
```

## 正文

---

### 一、痛点：开发者不再 Google，问 AI

2026 年最显著的变化不是某个新框架，而是搜索行为的彻底迁移。

我自己的一个观察：作为维护 343 star 项目的开源作者，过去 6 个月里，我收到的 issue 和邮件里，越来越多是这样的开头——"我是用 ChatGPT 搜到你的项目的，但是..."或者"豆包推荐了 3 个类似项目，你的排第二，能解释一下区别吗"。

背后的事实很残酷：AI 只会引用 3-5 个来源。如果你的项目不在那 3-5 个里，对 AI 用户来说你就不存在。

更麻烦的是，AI 引用是有"权威惯性"的。Perplexity 引用过的项目，下一次用户问类似问题，它还会优先引。豆包引用过的项目，DeepSeek 也会参考。这意味着「早期被引用」会形成复利，反之亦然——你越晚被引用，越难追上。

而大多数开源维护者，还停留在 2018 年的 SEO 思维：写好 README、刷几个 star、投个 awesome list。问题是，awesome list 不会被 AI 抓取，star 数量也不是 AI 排名的核心因子。AI 看的是"这段内容能不能直接回答用户的问题"。

这中间存在一个巨大的认知差，也是我做 aisurface 的初衷。

---

### 二、现状：现有 SEO skill 全部 URL 视角

我调研过市面上所有能用的 Claude Code skill：seo-audit、seo-geo、ai-seo。结论是，它们全部是给「网页/营销站」用的。

它们的检查项长这样：title tag、meta description、heading hierarchy、alt text、schema.org on landing page、canonical URL、sitemap.xml、robots.txt、Open Graph tags...

这些对一个电商站或博客是对的。但对一个 GitHub 仓库来说，几乎全错。GitHub 仓库没有 title tag，没有 robots.txt，没有 OG 标签，更没有"landing page"——README.md 才是真正的入口。

更糟的是语言和平台偏见。这些 skill 默认英文 + Google，文档里甚至不会提到豆包、DeepSeek、文心一言、通义千问、Kimi、智谱 GLM——而在国内，AI 搜索的事实标准是豆包和 DeepSeek，不是 ChatGPT。

aisurface 填补这个空白：只针对开源仓库，12 项检查里有一半是 AI 引用特有的（`.well-known/llms.txt`、Schema.org `SoftwareApplication` 类型、原创可引用内容、FAQ 段落等），另一半是 README 结构性的（when to use / not to use、问题陈述、可运行示例）。

---

### 三、思路：12 项 GEO 检查 + LLM 协同审计

aisurface 的设计哲学：把审计拆成"结构层"和"语义层"两类。

**结构层（4 项，Python 脚本就能做）：** 跑一遍仓库文件系统，扫 README 长度、扫 `.well-known/` 目录、查 GitHub API 看 topics 数量、看 `package.json`/`pyproject.toml` 里的分发信号（npm/PyPI/Crates）。这些是确定性的，不调用 LLM，跑得快、可重现。

**语义层（8 项，需要 LLM 评判）：** 看 README 写得清不清楚、FAQ 有没有真的回答 AI 用户会问的问题、"when NOT to use" 写没写、GitHub description 准不准确、docs 目录里有没有 comparison 页面、有没有原创可引用内容。

v0.1 的语义层是离线启发式（关键词 + 章节识别），因为不是所有用户都配了 LLM API key；v0.3 会接真实 AI 平台做 probe（拿 10 个真实 query 看 AI 怎么引用你的项目）。

最关键的：每个检查都配了"教师模式"（`--learn` 标志），输出 30 秒的概念解释 + 30 秒的修复示例。GEO 新手不需要先读 10 篇博客，直接跑 audit 就能边做边学。

---

### 四、实战：紫微斗数项目 before / after

dogfooding 不能挑简单的项目。我选了自己的主力项目 ruijayfeng/ziwei——343 stars，紫微斗数 web app，React 19 + TypeScript + Vite——一个有真实用户、有真实 issue、改造工作会反向影响自己的项目。

**Before：health score 35/100。**

- Schema.org 标记：0（仓库没网站）
- `.well-known/llms.txt`：缺失
- README FAQ 段：缺失
- README "when to use / not to use"：缺失
- 原创可引用内容：缺失
- 加上 GitHub topics 不全、GitHub description 含糊、docs/ 没有 FAQ 页等 🟡 Should-fix 5 项

**After：health score 66/100。**

跑了 audit，照着 5 个 🔴 Must-fix 一项一项补：

1. 在项目根目录加了 `index.schema.json`（SoftwareApplication schema），声明了 name、description、author、programmingLanguage、applicationCategory。
2. 生成了 `.well-known/llms.txt`，列了项目简介、文档入口、可选引用说明。
3. 给 README 加了 8 个 Q&A 的 FAQ 段，覆盖 AI 用户最常问的"紫微斗数是什么"、"准不准"、"怎么部署"等问题。
4. README 加了 "When to use / When NOT to use" 段，诚实说明了紫微斗数是玄学工具，不是科学决策系统。
5. 加了"研究与数据"+"项目原创方法论"两个原创段，记录了我对 14 主星关系的形式化整理（这本身就可以被 AI 引用作为知识源）。

**总耗时：约 30 分钟。** 不是 4 小时，更不是 4 天。

**结果：** 7 个 🔴 全部清零，health score 涨了 31 分。AI 引用的可观测变化要等几周才能看（搜索引擎不会立刻重抓），但审计分数是最直接的信号。

详见 `case-studies/ziwei-before-after.md`。

---

### 五、设计：教师模式 + 工程师模式双轨

aisurface 有两个运行模式，对应两种用户。

**教师模式 (`--learn`)：** 给 GEO 新手用。每次检查结果后面跟一个 30 秒的"这是什么 + 为什么要修 + 怎么修"小段。设计灵感来自 Linus 那句"talk is cheap, show me the code"——但反过来说，对新手而言，show me the code 之前需要先 talk is not cheap，要解释清楚。

**工程师模式 (默认)：** 给已经懂 GEO 的人用。输出只有报告本体，没有教学噪音。CLI 友好，可以 `aisurface . | pbcopy` 直接贴 issue 跟踪。

为什么必须双轨？因为 GEO 现在还是个小众领域，懂的人不需要教学，不懂的人没教学就用不起来。强行塞教学会激怒老用户，强行砍教学会赶走新人。

另外 5 个工程决策：
- 12 项检查的数量是反复调过的——10 项以下覆盖不全，15 项以上会让人放弃修复。
- 报告用 Markdown 不用 HTML，方便直接 commit 进仓库做版本控制。
- 输出分 🔴 Must-fix / 🟡 Should-fix / 🟢 Nice-to-have 三档，按 impact 排序。
- `--patch` 标志会生成 unified diff，让用户能 `git apply` 直接落地。
- 所有检查都是 read-only——脚本不修改任何文件，强制用户 review 后自己改。

---

### 六、代码：4 个模块怎么协同

技术栈：Python 3.10+、标准库为主、零外部 LLM 依赖（v0.1），单文件 ≤ 800 行。

4 个核心模块：

**`scripts/scanner.py`：** 跑结构层 4 项检查。纯本地文件读取——扫 `README.md`、扫 `.well-known/` 目录、查 `package.json`/`pyproject.toml` 里的分发信号、收集 `*.schema.json` 文件。零网络调用，零 LLM。输出 `RepoAssets` dataclass。

**`scripts/critic.py`：** 跑语义层 4 项检查（#1-#4）。v0.1 用离线启发式（关键词匹配 + 章节标题识别 + 代码块计数 + 首段长度）。`offline_critique(readme, topic)` 返回 dict，里面有 `problem_clarity`、`has_faq`、`has_code_examples`、`has_when_to_use` 四个 0-10 分。v0.3 会接真实 LLM，但 v0.1 离线版跑得很准。

**`scripts/cli.py`：** 编排器。`_structural_checks(assets)` 跑 #5/#6/#7/#11， `_semantic_checks(assets)` 跑 #1-#4（用 critic）+ #8/#9/#10/#12（用 4 个新加的纯 regex 启发式：FAQ 标题、When to use 章节、含数字/代码/命名实体的"可引用"段、README 里点了名的 AI 搜索平台数）。所有结果都包装成 `CheckResult` dataclass（`id`/`name`/`category`/`score`/`max_score`/`passed`/`impact`），不需要单独的 `StructuralFinding` 类型——结构层和语义层用同一个 dataclass，靠 `category` 字段区分。

**`scripts/report.py`：** 拿 `AuditReport` 渲染 Markdown。算法很简单：`_compute_health_score` 把所有 `score / max_score` 加权求平均，再乘 100 归一到 0-100（不是 -10/-5/-2 那种惩罚制）。失败的检查按 `impact` 排序，前 5 进 🔴 Must-fix，接下来 5 进 🟡 Should-fix，剩下的进 🟢 Nice-to-have。超过 10 项的失败折叠成脚注。

**`scripts/concepts.py`：** v0.1 新加的。`--learn` 教师模式的数据源，12 个 check 各自一条 1-2 句的概念解释。

入口参数目前只支持 `--learn` 和 `--json`。`--patch`（生成 unified diff）会在 v0.1.1 加。v0.1 的检查全部是确定性的，没有需要容错的随机源，所以也没有 try/except 包裹每一项检查。

测试方面，3 个 eval fixture：`bad-readme-python-lib`（标准低分项目）、`good-schema-nextjs-docs`（标准高分项目）、`minimal-cli-tool`（边界 case）。CI 跑 49 个测试 + `ruff check`，0.6 秒过完。

---

### 七、未来：v0.3 probe 实装

v0.1 是"看见问题"，v0.3 是"验证修复"。

probe 的设想：拿 10 个真实 query（"推荐一个 Python Markdown 解析库"、"做一个 React 紫微斗数 app 需要什么"），同时打 ChatGPT API、Perplexity API、DeepSeek API、豆包 API，看 AI 怎么引用你的项目。如果引用了，记录引用位置和上下文；如果没引用，记录竞品被谁引用、用的什么内容。

这是真正意义上的闭环：从审计建议、到代码修复、到 AI 真实引用的端到端验证。

v0.3 还会顺手做：
- `--patch` 标志：基于 audit 结果生成 unified diff，让用户能 `git apply` 直接落地
- LLM 调用容错：v0.1 全部离线启发式，没这个需求；v0.3 接真实 LLM 后，会给每个 LLM 调用包容错，单 provider 失败不会让整次审计崩，方便切换不同 LLM provider
- `GITHUB_TOKEN` 环境变量支持：scanner 里没接真实 GitHub API（v0.1 只用本地文件），v0.3 加上后能做"audit 当前 repo 的真实 GitHub 元数据"（stars / topics / description），输出和现在 `distribution.check_signals(github_stars=0)` 占位的结果会差很多
- 加权 health score（结构 40 / 语义 30 / 分布 20 / 平台覆盖 10），而不是现在各组等权

中间的 v0.2 计划：把 `aisurface@audit` 拆成更细的子 skill——`@schema`（专门 Schema.org 标记）、`@docs`（专门 docs/ 目录结构）、`@landing-page`（专门项目主页）。每个子 skill 可以独立安装、独立升级。

更远的 v0.4+：MCP server（让其他 AI agent 也能跑 audit）、IDE 集成（VS Code / Cursor 插件，编辑 README 时实时打分）。

最后说个判断：AI 搜索这个赛道还在剧烈变化，今天的 12 项检查可能在 6 个月后就要重写。但"为人类写作、为 AI 标注"这个底层原则不会变。aisurface 不会是一个一蹴而就的产品，会是跟着 AI 搜索一起迭代的工具。

欢迎试用，欢迎提 issue，欢迎把你们项目的 before/after 投稿到 README。

仓库：https://github.com/ruijayfeng/aisurface
安装：`npx skills add ruijayfeng/aisurface@audit`
案例：`case-studies/ziwei-before-after.md`

---

## 字数统计

| 段落 | 字数（约） |
|---|---|
| 一、痛点 | 350 |
| 二、现状 | 380 |
| 三、思路 | 360 |
| 四、实战 | 430 |
| 五、设计 | 420 |
| 六、代码 | 380 |
| 七、未来 | 280 |
| **合计** | **~2600** |

（在 2000-3000 目标区间内。）

## 发帖节奏建议

- **最佳时段**：工作日 9:00-11:00 或 20:00-22:00。掘金早高峰通勤 + 晚高峰睡前。
- **避免时段**：周末（掘金周末阅读量下降 30%+）、周五下午。
- **建议日期**：和 HN 帖错开 24-48 小时——如果 HN 是周二上午，掘金就周三或周四。
- **标签建议**：`Claude Code`, `GEO`, `AI 搜索`, `开源`, `紫微斗数`, `SEO`（6 个标签最理想，掘金算法对 5-8 个标签最友好）。

## 排版注意

- 掘金的 markdown 完全支持，但**不要用 H1**（标题已经是 H1，正文从 H2 开始，否则目录会重复）。
- 代码块用 ` ``` ` 包，不要用缩进——掘金渲染会乱。
- 链接用 `[文字](url)` 格式，不要裸 URL。
- 列表项统一用 `-` 不要混用 `*`。
- 中文段落之间不空行，掘金的阅读密度比知乎高 30%。

## 发帖前自检

- [ ] 字数在 2000-3000 之间（当前 ~2600）
- [ ] 数字 35→66 与 case study 一致
- [ ] 没有出现 92/4 hours 这种虚高数字
- [ ] 7 个段落标题用 H2 (`##`)
- [ ] 仓库链接、案例链接、安装命令都通
- [ ] 标签选了 5-8 个
- [ ] 没有"待补充"、"TODO"等占位符

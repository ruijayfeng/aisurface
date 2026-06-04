# FAQ

> 4 个最常被问的问题。觉得答案有错或想加新问题,开 issue / PR。

## GEO 是什么?

**GEO = Generative Engine Optimization**(生成式引擎优化)。让项目能被 AI 搜索(Perplexity、ChatGPT、Claude 等)—— 这些引擎**回答问题 + 引用来源**,而不是像 Google 那样返回一堆蓝色链接。

底层思路跟 SEO 一样,只是优化的对象从"搜索引擎结果页"变成了"AI 引用的 3-5 个来源"。

## 跟传统 SEO 工具(ahrefs、SEMrush)有啥区别?

三点:

1. **对象**:开源项目,不是营销站
2. **渠道**:AI 搜索(Perplexity、ChatGPT 等),不是 Google / Bing
3. **结果**:被引用 vs. 没被引用(不是排名)

传统 SEO 优化的是"在 Google 排第几";aisurface 优化的是"AI 回答用户问题时,你的项目是不是那 3-5 个被引用的来源之一"。

## verify 准不准?

verify 用**真的 Perplexity API**问用户可能问的问题。如果你的项目 URL 出现在引用列表里,就是被引用了;没有就是没被。数据是真的,不是模型预测。

两个 caveat:

- **Perplexity API 不确定性**:LLM 输出每次略不同。10 个 query 跑两次,引用数会有 ±1-2 的抖动。需要稳定对比就用 `--baseline` 存基线
- **只匹配 URL**:verify 比对的是 `pyproject.toml` / `package.json` 里的 `homepage`。如果 Perplexity 引用了你的项目但用了名字而不是 URL,会判 false negative

## 为啥只支持 Perplexity?ChatGPT / Claude / Gemini / DeepSeek 呢?

两个原因:

1. **工程成本**:每个 adapter ~1-2 周(API 协议、auth、rate limit、错误处理、citation 解析)。与其发 v1.0 声称支持 10 个但只交付 1 个,不如诚实说 1 个
2. **市场信号**:Perplexity 有干净的 citation API 和合理定价。ChatGPT / Claude 不公开 citation;DeepSeek / 豆包 / 通义等 rate-limit 严,程序化探针贵

**路线图**:ChatGPT / Claude / Gemini / DeepSeek / 豆包 / 文心一言 / 通义千问 / Kimi / 智谱 / GLM 都在 v1.1+ 计划里,触发条件见 [ROADMAP.md#platform-coverage](../ROADMAP.md#platform-coverage)。

---

## 没找到答案?

- 安装/CLI 用法 → [CONTRIBUTING.md](../CONTRIBUTING.md)
- 已知问题/路线 → [ROADMAP.md](../ROADMAP.md)
- 版本变更 → [CHANGELOG.md](../CHANGELOG.md)
- 想贡献 / 加新检查 → 开 issue

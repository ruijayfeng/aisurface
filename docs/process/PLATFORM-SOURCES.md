<!--
[INPUT]: none (standalone URL list)
[OUTPUT]: Reference URLs for the 9 tracked AI-search platforms' MAU, release notes, and API changelogs
[POS]: docs/process/'s platform data source index, consumed by Boss during the monthly platform update
[PROTOCOL]: Update this header when changed
-->

# Platform data sources

## ChatGPT (OpenAI)
- MAU: https://openai.com/blog (announced in blog posts, also Reuters)
- Release notes: https://help.openai.com/en/articles/9624314-model-release-notes
- API: https://platform.openai.com/docs/changelog

## Perplexity
- MAU: https://www.perplexity.ai/hub/blog (rarely disclosed; rely on third-party like SimilarWeb)
- Release notes: https://docs.perplexity.ai/guides/changelog

## Doubao (豆包, ByteDance)
- MAU: Chinese tech press (36Kr, 虎嗅)
- Release notes: https://www.volcengine.com/docs (Volcano Engine platform)

## DeepSeek
- MAU: 36Kr / 量子位
- Release notes: https://api-docs.deepseek.com/news/

## Kimi (Moonshot)
- MAU: 36Kr
- Release notes: https://platform.moonshot.cn/docs

## Wenxin (文心, Baidu)
- MAU: Baidu IR / financial reports
- Release notes: https://cloud.baidu.com/doc/

## Tongyi (通义, Alibaba)
- MAU: Alibaba IR
- Release notes: https://help.aliyun.com/

## GLM (Zhipu)
- MAU: Chinese tech press
- Release notes: https://open.bigmodel.cn/

## Gemini (Google)
- MAU: Google IR / Sundar announcements
- Release notes: https://blog.google/products/google-deepmind/

## Notes on sourcing

- Chinese platforms (Doubao, DeepSeek, Kimi, Wenxin, Tongyi, GLM) rarely publish official MAU; use 36Kr / 量子位 / 虎嗅 as primary press, then cross-check with 七麦数据 / SimilarWeb / AppAnnie.
- Global platforms (ChatGPT, Perplexity, Gemini) sometimes publish MAU in earnings calls or quarterly blog posts; otherwise use SimilarWeb traffic data as a proxy.
- When a release note is in Chinese and unaided translation risks error, paste into aisurface@audit as a smoke test — the audit skill is bilingual.

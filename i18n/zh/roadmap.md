---
description: "问卦 Wengua 的里程碑：从双语数据集到托管 MCP 服务和应用目录上架。"
---

# 路线图

| 里程碑 | 范围 | 状态 |
|---|---|---|
| M0 数据集 | 六十四卦全部经传，繁简两体（✅），与宋本校勘（✅），`SOURCES.md` 与校验程序（✅），每段文字（含文言）都有理雅各英译（✅） | ✅ 完成 |
| M1 核心库 | TypeScript 与 Python 核心、共用测试向量、随机数检验 | ✅ 完成 |
| M2 技能、本地 MCP、命令行 | `npx wengua` 与 `uvx wengua` MCP 服务、`wengua` 命令行、`skills/wengua` | ✅ 完成（在 M5 发布） |
| M3 托管 MCP 与卡片 | Cloudflare Worker 上的 `https://wengua.allo.land/mcp`，MCP Apps 卦象卡片 | ✅ 完成 |
| M4 白话注释 | 每卦每爻的 `zh_plain` 与 `en_plain` | 未开始 |
| M5 发布 | npm、PyPI、MCP Registry、Claude 与 ChatGPT 应用目录 | 进行中：PyPI 0.1.0 已发布；npm 发布流程已就绪 |
| 以后 | 梅花易数、本地占卦记录、更多语言 | — |

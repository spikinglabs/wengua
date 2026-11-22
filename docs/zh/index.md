---
description: "问卦 Wengua：为所有 AI 打造的准确、开放的《易经》工具，提供繁简两体原文、公平起卦、MCP 服务与 Agent Skill。"
---

# 问卦 Wengua

**为所有 AI 打造的准确、开放的《易经》工具。**

问卦让你在 Claude、ChatGPT、Codex、Cursor 或任何支持 MCP 的客户端里问《易经》。起卦与取辞交给程序，解卦交给 AI。

> 排卦归程序，解卦归模型。

## 马上试用

- **Claude.ai 或 ChatGPT**：添加自定义连接器，网址填 `https://wengua.allo.land/mcp`。
- **Claude Code**：`claude mcp add --transport http wengua https://wengua.allo.land/mcp`
- **任何 MCP 客户端**：`npx -y wengua` 或 `uvx wengua`。
- **Agent Skill**：把 `skills/wengua` 放进你的智能体。

## 特点

- **原文可靠**：卦辞、爻辞及十翼（彖传、大象、小象、文言），繁简两体，与宋本（四部丛刊本王弼《周易注》）逐字校勘，每卦注明出处并记录每一处校改。
- **起卦公平、可验证**：三钱法与完整的大衍筮法，概率与古法完全一致，使用安全随机数，记录每枚铜钱、每次分蓍，并在 CI 中做统计检验。
- **取辞有据**：按朱熹《易学启蒙·考变占》决定读哪几条爻辞，AI 不必猜，也不会编造。
- **处处可用**：同一核心，提供 Agent Skill、本地 MCP、免费托管 MCP、卦象卡片和命令行。
- **重在反思，不做预言**：解读是启发思考，而非下定论。

## 组成部分

| 部分 | 说明 | 状态 |
|---|---|---|
| 数据集 | 六十四卦全部经传原文，繁简两体，附出处 | ✅ 中文完成，英文计划中 |
| 核心库 | TypeScript 与 Python 的起卦、变卦、取辞、查卦 | ✅ 完成 |
| Agent Skill | 可直接放入 Claude 等智能体的技能包 | ✅ 完成 |
| MCP 服务 | 本地（npx / uvx）与托管（wengua.allo.land/mcp） | ✅ 完成 |
| 卦象卡片 | 在 Claude 和 ChatGPT 中显示，可切换繁简 | ✅ 完成 |
| 命令行 | `wengua cast --json` | ✅ 完成 |

npm 与 PyPI 包即将发布。详细设计见 [Design](../design.md)（英文）。

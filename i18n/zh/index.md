---
description: "问卦 Wengua 让 Claude、ChatGPT、Codex、Cursor 及任何 MCP 客户端都能问《易经》：繁简两体的可靠原文，公平、可验证的起卦。"
---

# 问卦 Wengua

**为所有 AI 打造的准确、开放的《易经》工具。**

问卦让你在 Claude、ChatGPT、Codex、Cursor 或任何 MCP 客户端里问《易经》。起卦和取辞交给程序，AI 只负责解读。

> 排卦归程序，解卦归模型。

## 现在起一卦

在这里直接起卦，看看卦象和对应的原文。想要解读，请在你的 AI 里使用问卦（见下文）。

<div class="wengua-cast"></div>

## 在 AI 里使用

- **MCP 服务：** 把 `https://wengua.allo.land/mcp` 加为连接器或 MCP 服务器。免费，无需账号。
- **Agent Skill：** [下载 wengua-skill.zip](https://wengua.allo.land/wengua-skill.zip)，添加到你的 AI。
- [Claude](setup/claude.md)、[ChatGPT](setup/chatgpt.md)、[Codex](setup/codex.md)、[Gemini](setup/gemini.md)、[GitHub Copilot](setup/copilot.md)、[Cursor](setup/cursor.md) 和[你自己的应用](setup/api.md)的详细步骤都在[快速上手](setup/index.md)。

## 为什么选问卦

- **原文可靠。** 通行本的卦辞、爻辞和十翼（彖、象、文言），繁简两体，与宋本逐字校勘。每卦注明出处，并记录每一处校改。
- **起卦公平、可验证。** 三钱法或完整的大衍筮法，概率与古法完全一致；使用安全随机数，记录每枚铜钱、每次分策，并在 CI 中做统计检验。
- **每次都读对的文字。** 按朱熹的规则决定读哪几条，AI 不必猜，也不会编造爻辞。
- **处处可用。** 同一个核心，支撑 Agent Skill、本地 MCP 服务、免费托管 MCP 服务、卦象卡片和命令行。
- **重在反思，不做预言。** 解读是启发思考的提示，而不是定论。

## 组成部分

| 部分 | 说明 | 状态 |
|---|---|---|
| [数据集](ecosystem/dataset.md) | 六十四卦的全部经传原文，繁简两体，附出处 | ✅ 中文与理雅各英译 |
| [核心库](ecosystem/core.md) | TypeScript 与 Python 的起卦、推演、取辞和查卦 | ✅ 完成 |
| [Agent Skill](ecosystem/skill.md) | 可直接放进 Claude 等智能体的技能包 | ✅ 完成 |
| [MCP 服务](ecosystem/mcp.md) | 本地（`uvx`/`npx`）与托管（`wengua.allo.land/mcp`） | ✅ 完成 |
| [卦象卡片](ecosystem/card.md) | 在 Claude 和 ChatGPT 中直接显示的卦象卡片 | ✅ 完成 |
| [命令行](ecosystem/cli.md) | 供终端和编程智能体使用的 `wengua cast --json` | ✅ 完成 |

Python 包已发布到 [PyPI](https://pypi.org/project/wengua/)（`pip install wengua`）。另见[路线图](roadmap.md)。

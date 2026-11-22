---
description: "问卦 Wengua 的 MCP 服务：可用 uvx 或 npx 在本地运行，也有托管在 wengua.allo.land/mcp 的版本，提供繁简两体的起卦、读卦和查卦工具。"
---

# MCP 服务

MCP 服务内置在两个包里，不需要其他依赖。

- **本地（stdio）：** `uvx wengua` 或 `npx -y wengua`，适用于 Claude 桌面版、Claude Code、Cursor、VS Code、Goose 及任何 MCP 客户端。
- **托管：** `https://wengua.allo.land/mcp`，免费，无需账号和 API Key，适用于 Claude.ai、ChatGPT 等无法运行本地服务的客户端。它是无状态的（Streamable HTTP，返回 JSON），每个 IP 每分钟可发 60 个请求，从不保存或记录问题。

```json
{
  "mcpServers": {
    "wengua": { "command": "uvx", "args": ["wengua"] }
  }
}
```

用 Node.js 时：`"command": "npx", "args": ["-y", "wengua"]`。Claude、ChatGPT、Codex、Gemini、GitHub Copilot、Cursor 以及 Claude 和 OpenAI API 的具体步骤见 [快速上手](../setup/index.md)。

## 卦象卡片

在支持 [MCP Apps](https://github.com/modelcontextprotocol/ext-apps) 的客户端（Claude、ChatGPT 等）里，`cast` 和 `read_cast` 还会显示一张内嵌卡片（`ui://wengua/reading/<hash>`）。卡片画出本卦和之卦并标出变爻，列出选出的文字及其作用，可切换繁體/简体。其他客户端则以文字形式得到同样的结果。

服务支持 MCP 协议版本 2024-11-05 到 2025-11-25，并用官方 MCP Python SDK 测试。工具结果同时包含 `structuredContent` 和同样内容的 JSON 文本。

## 工具

| 工具 | 输入 | 返回 |
|---|---|---|
| `cast` | `question`、`method`（coins / yarrow）、`rule`、`locale` | 完整的一卦 |
| `read_cast` | `lines`：实物起卦的六个爻值或铜钱正反，自下而上 | 完整的一卦 |
| `lookup` | `query`：卦序、卦名、拼音、䷀、二进制或上下卦 | 该卦的全部文字；有歧义时返回所有匹配 |
| `relations` | `hexagram`，可选 `changing_lines` | 之卦、互卦、错卦、综卦及其卦辞 |

每段中文都同时有 `zh_hant` 和 `zh_hans`，模型可以按用户的字体作答。每段文字也都带有 `en_legge`，即理雅各的英译（1882），模型可注明出处后引用。

资源：`wengua://hexagram/{number}` 和 `wengua://trigram/{key}`。提示词：`reading`，引导式占卦。

服务的说明会告诉模型如何读卦：先厘清问题，绝不编造或重新起卦，只引用工具返回的文字，把经文与解读分开，并以引人反思的问题而非定论作结。

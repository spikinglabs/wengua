---
description: "The Wengua MCP server, run locally with uvx or npx, or hosted at wengua.allo.land/mcp, with tools to cast, read and look up I Ching hexagrams in traditional and simplified Chinese."
---

# MCP server

The MCP server ships inside both packages and needs no other dependencies.

- **Local (stdio):** `uvx wengua` or `npx -y wengua`, for Claude Desktop, Claude Code, Cursor, VS Code, Goose and any MCP client.
- **Hosted:** `https://wengua.allo.land/mcp`, free, with no account and no API key, for Claude.ai, ChatGPT and other clients that can't run local servers. It is stateless (Streamable HTTP, JSON responses), allows 60 requests a minute per IP, and never stores or logs questions.

```json
{
  "mcpServers": {
    "wengua": { "command": "uvx", "args": ["wengua"] }
  }
}
```

With Node.js: `"command": "npx", "args": ["-y", "wengua"]`. Exact steps for Claude, ChatGPT, Codex, Gemini, GitHub Copilot, Cursor and the Claude and OpenAI APIs are in [Get started](../setup/index.md).

## Reading card

In clients that support [MCP Apps](https://github.com/modelcontextprotocol/ext-apps) (Claude, ChatGPT and others), `cast` and `read_cast` also show an inline card (`ui://wengua/reading/<hash>`). It draws the primary and relating hexagrams with the changing lines marked, lists the selected texts with their roles, and has a 繁體/简体 toggle. Other clients get the same reading as text.

The server supports MCP protocol versions 2024-11-05 through 2025-11-25 and is tested with the official MCP Python SDK. Tool results include both `structuredContent` and the same JSON as text.

## Tools

| Tool | Input | Returns |
|---|---|---|
| `cast` | `question`, `method` (coins / yarrow), `rule`, `locale` | A full reading |
| `read_cast` | `lines`: six line values or coin faces from a physical cast, bottom to top | A full reading |
| `lookup` | `query`: number, name, pinyin, ䷀, binary or trigrams | The hexagram with all its texts, or the matches if ambiguous |
| `relations` | `hexagram`, optional `changing_lines` | 之 / 互 / 錯 / 綜 with their judgments |

Every Chinese text comes in both `zh_hant` and `zh_hans`, so the model can answer in the user's script. Every text also carries `en_legge`, James Legge's English (1882), which the model can quote with credit.

Resources: `wengua://hexagram/{number}` and `wengua://trigram/{key}`. Prompt: `reading`, a guided reading.

The server's instructions tell the model how to read: clarify the question, never invent or re-roll a result, quote only the texts the tool returned, keep the classical text apart from interpretation, and end with reflective questions rather than a verdict.

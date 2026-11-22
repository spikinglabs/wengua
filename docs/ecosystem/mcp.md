---
description: "The Wengua MCP server, run locally with npx or uvx, with tools to cast, read and look up I Ching hexagrams in traditional and simplified Chinese."
---

# MCP server

The MCP server ships inside both packages and needs no other dependencies.

- **Local (stdio):** `npx -y wengua` or `uvx wengua`, for Claude Desktop, Claude Code, Cursor, VS Code, Goose and any MCP client.
- **Hosted:** a free, stateless endpoint on Cloudflare Workers, for clients that can't run local servers (planned, see the [roadmap](../roadmap.md)).

```json
{
  "mcpServers": {
    "wengua": { "command": "npx", "args": ["-y", "wengua"] }
  }
}
```

With Python: `"command": "uvx", "args": ["wengua"]`. In Claude Code: `claude mcp add wengua -- npx -y wengua`.

The server supports MCP protocol versions 2024-11-05 through 2025-11-25 and is tested with the official MCP Python SDK. Tool results include both `structuredContent` and the same JSON as text.

## Tools

| Tool | Input | Returns |
|---|---|---|
| `cast` | `question`, `method` (coins / yarrow), `rule`, `locale` | A full reading |
| `read_cast` | `lines`: six line values or coin faces from a physical cast, bottom to top | A full reading |
| `lookup` | `query`: number, name, pinyin, ䷀, binary or trigrams | The hexagram with all its texts, or the matches if ambiguous |
| `relations` | `hexagram`, optional `changing_lines` | 之 / 互 / 錯 / 綜 with their judgments |

Every Chinese text comes in both `zh_hant` and `zh_hans`, so the model can answer in the user's script.

Resources: `wengua://hexagram/{number}` and `wengua://trigram/{key}`. Prompt: `reading`, a guided reading.

The server's instructions tell the model how to read: clarify the question, never invent or re-roll a result, quote only the texts the tool returned, keep the classical text apart from interpretation, and end with reflective questions rather than a verdict.

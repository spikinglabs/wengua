---
description: "The Wengua MCP server, local via npx or uvx and hosted for free, with tools to cast, read and look up I Ching hexagrams."
---

# MCP server

Available two ways, with the same tools:

- **Local:** `npx wengua` or `uvx wengua` (stdio), for Claude Desktop, Claude Code, Cursor, VS Code and Goose.
- **Hosted:** a free, stateless endpoint on Cloudflare Workers with no account, no API key and no daily quota. Questions are never stored.

Both follow the MCP 2026-07-28 specification and stay compatible with earlier clients.

## Tools

| Tool | Input | Returns |
|---|---|---|
| `cast` | `question`, `method` (coins / yarrow), `locale` | A reading, plus the reading card where supported |
| `read_cast` | six line values or coin faces from a physical cast | A reading |
| `lookup` | number, name, pinyin, ䷀, binary or trigrams | The hexagram with all text layers |
| `relations` | hexagram, optional changing lines | 之 / 互 / 错 / 综 with their texts |

Resources: `wengua://hexagram/{n}`, `wengua://trigram/{name}`. Prompt: `reading`.

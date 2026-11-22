---
description: "Set up Wengua 问卦 in any MCP client or Agent Skills platform: hosted Streamable HTTP URL, local stdio server with uvx or npx, and the skill folder."
---

# Other clients

## Any MCP client

| | Hosted | Local |
|---|---|---|
| Transport | Streamable HTTP | stdio |
| Address or command | `https://wengua.allo.land/mcp` | `uvx wengua` (or `npx -y wengua`) |
| Auth | None | None |

Most clients accept this shape:

```json
{
  "mcpServers": {
    "wengua": { "url": "https://wengua.allo.land/mcp" }
  }
}
```

```json
{
  "mcpServers": {
    "wengua": { "command": "uvx", "args": ["wengua"] }
  }
}
```

The hosted server is stateless: every POST gets a JSON response, notifications get 202, and GET returns 405. It supports MCP protocol versions 2024-11-05 through 2025-11-25 and allows 60 requests a minute per IP. See [MCP server](../ecosystem/mcp.md) for the tools, resources and prompt.

## Any Agent Skills platform

The skill follows the open [Agent Skills](https://agentskills.io) standard. Download it, unzip it, and put the `wengua` folder wherever your tool loads skills from. Many tools read `~/.agents/skills`.

[Download wengua-skill.zip](https://wengua.allo.land/wengua-skill.zip){ .md-button }

The folder holds `SKILL.md` and `scripts/run.py`. It needs Python 3.10 or later and nothing else.

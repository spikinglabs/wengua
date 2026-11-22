---
description: "Set up Wengua 问卦 in Gemini CLI: one command for the MCP server, or install the Agent Skill into ~/.gemini/skills."
---

# Gemini

## Gemini CLI

### MCP server

Hosted:

```bash
gemini mcp add --scope user --transport http wengua https://wengua.allo.land/mcp
```

Local:

```bash
gemini mcp add --scope user wengua uvx wengua
```

Or edit `~/.gemini/settings.json` (or `.gemini/settings.json` in a project). Gemini CLI uses `httpUrl` for Streamable HTTP servers:

```json
{
  "mcpServers": {
    "wengua": { "httpUrl": "https://wengua.allo.land/mcp" }
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

Check it with `gemini mcp list`, or `/mcp` inside a session.

### Agent Skill

```bash
mkdir -p ~/.gemini/skills
curl -fsSLo /tmp/wengua-skill.zip https://wengua.allo.land/wengua-skill.zip
unzip -o /tmp/wengua-skill.zip -d ~/.gemini/skills
```

Or install it straight from this repository:

```bash
gemini skills install https://github.com/spikinglabs/wengua.git --path skills/wengua --consent
```

Check it with `gemini skills list`. For one project, unzip into `.gemini/skills` instead.

## The Gemini app

The Gemini app on the web and on phones doesn't let you add your own MCP servers or skills yet. Use Gemini CLI, or another app from [Get started](index.md).

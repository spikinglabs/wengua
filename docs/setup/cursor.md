---
description: "Set up Wengua 问卦 in Cursor: one-click MCP install, mcp.json config, and the Agent Skill in ~/.cursor/skills."
---

# Cursor

## MCP server

[Add Wengua to Cursor](cursor://anysphere.cursor-deeplink/mcp/install?name=wengua&config=eyJ1cmwiOiJodHRwczovL3dlbmd1YS5hbGxvLmxhbmQvbWNwIn0=){ .md-button .md-button--primary }

The button opens Cursor and adds the hosted server. To do it by hand, edit `~/.cursor/mcp.json` (for you) or `.cursor/mcp.json` in a project:

```json
{
  "mcpServers": {
    "wengua": { "url": "https://wengua.allo.land/mcp" }
  }
}
```

Local:

```json
{
  "mcpServers": {
    "wengua": { "command": "uvx", "args": ["wengua"] }
  }
}
```

Check it under **Cursor Settings → MCP**, then ask the agent for a reading.

## Agent Skill

```bash
mkdir -p ~/.cursor/skills
curl -fsSLo /tmp/wengua-skill.zip https://wengua.allo.land/wengua-skill.zip
unzip -o /tmp/wengua-skill.zip -d ~/.cursor/skills
```

For one project, unzip into `.cursor/skills` instead. Cursor also reads `.agents/skills` and `.claude/skills`.

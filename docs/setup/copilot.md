---
description: "Set up Wengua 问卦 in GitHub Copilot and VS Code: add the MCP server with one command or a config file, and install the Agent Skill."
---

# GitHub Copilot (VS Code)

## MCP server

Hosted, with one command:

```bash
code --add-mcp '{"name":"wengua","type":"http","url":"https://wengua.allo.land/mcp"}'
```

Local:

```bash
code --add-mcp '{"name":"wengua","type":"stdio","command":"uvx","args":["wengua"]}'
```

Or add it to Copilot's MCP config file, `~/.copilot/mcp-config.json` (for you), or `.mcp.json` at the root of a repository (for your team):

```json
{
  "mcpServers": {
    "wengua": { "type": "http", "url": "https://wengua.allo.land/mcp", "tools": ["*"] }
  }
}
```

```json
{
  "mcpServers": {
    "wengua": { "type": "stdio", "command": "uvx", "args": ["wengua"], "tools": ["*"] }
  }
}
```

Open Copilot Chat in **Agent** mode, check that the Wengua tools are enabled in the tools picker, and ask for a reading.

## Agent Skill

For yourself:

```bash
mkdir -p ~/.copilot/skills
curl -fsSLo /tmp/wengua-skill.zip https://wengua.allo.land/wengua-skill.zip
unzip -o /tmp/wengua-skill.zip -d ~/.copilot/skills
```

For one repository, unzip into `.github/skills` instead and commit it, so Copilot uses it for everyone working in the repository.

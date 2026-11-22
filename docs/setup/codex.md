---
description: "Set up Wengua 问卦 in OpenAI Codex (CLI and IDE extension): one command for the MCP server, or unzip the Agent Skill into ~/.agents/skills."
---

# Codex

These steps work for the Codex CLI and the Codex IDE extension, which share `~/.codex/config.toml`.

## MCP server

Hosted:

```bash
codex mcp add wengua --url https://wengua.allo.land/mcp
```

Local:

```bash
codex mcp add wengua -- uvx wengua
```

Or edit `~/.codex/config.toml` yourself (use one of the two):

```toml
# Hosted
[mcp_servers.wengua]
url = "https://wengua.allo.land/mcp"
```

```toml
# Local
[mcp_servers.wengua]
command = "uvx"
args = ["wengua"]
```

Check it with `codex mcp list`.

## Agent Skill

For yourself:

```bash
mkdir -p ~/.agents/skills
curl -fsSLo /tmp/wengua-skill.zip https://wengua.allo.land/wengua-skill.zip
unzip -o /tmp/wengua-skill.zip -d ~/.agents/skills
```

For one repository, unzip into `.agents/skills` at the repository root instead. Codex picks up the skill when you ask for a reading, or call it with `$wengua`.

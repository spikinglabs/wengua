---
description: "Set up Wengua 问卦 in Claude: custom connector in claude.ai, Claude Desktop and mobile, skill upload, and Claude Code commands."
---

# Claude

## Claude.ai, Claude Desktop and mobile

### MCP server (custom connector)

Connectors you add on the web also work in the Claude Desktop app and on mobile. Custom connectors are available on every plan; the Free plan allows one.

**Pro, Max and Ultra**

1. Open [Customize → Connectors](https://claude.ai/customize/connectors).
2. Click **+ Add**, then **Add custom connector**.
3. Name: `Wengua`. URL:
    ```text
    https://wengua.allo.land/mcp
    ```
4. Leave authentication empty and click **Add**.

**Team and Enterprise:** an Owner adds it once in **Organization settings → Connectors → Add → Custom → Web** with the same URL. Members then turn it on under **Customize → Connectors → Connect**.

In a chat, open the **+** menu, make sure **Wengua** is enabled, and ask for a reading. Claude shows the reading card (the hexagrams, the changing lines and the selected texts, with a 繁/简 toggle) inline.

### Agent Skill

Skills need code execution to be enabled (**Settings → Capabilities**).

1. [Download wengua-skill.zip](https://wengua.allo.land/wengua-skill.zip){ .md-button }
2. Open [Customize → Skills](https://claude.ai/customize/skills).
3. Click **+**, then **+ Create skill**, then **Upload a skill**, and choose the zip. Don't unzip it first.

Claude uses the skill automatically when you ask for an I Ching reading.

### Claude Desktop with the local server

The custom connector above is the easiest way. To run the server on your own computer instead, edit `claude_desktop_config.json`:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "wengua": { "command": "uvx", "args": ["wengua"] }
  }
}
```

Restart Claude Desktop. If it can't find `uvx`, use the full path from `which uvx` (macOS) or `where uvx` (Windows). With Node.js, use `"command": "npx", "args": ["-y", "wengua"]`.

## Claude Code

### MCP server

Hosted:

```bash
claude mcp add --transport http wengua https://wengua.allo.land/mcp
```

Local:

```bash
claude mcp add wengua -- uvx wengua
```

Add `--scope user` to use it in all your projects, or `--scope project` to share it with your team through `.mcp.json`.

### Agent Skill

For yourself (all projects):

```bash
mkdir -p ~/.claude/skills
curl -fsSLo /tmp/wengua-skill.zip https://wengua.allo.land/wengua-skill.zip
unzip -o /tmp/wengua-skill.zip -d ~/.claude/skills
```

For one project, unzip into `.claude/skills` in the repository instead and commit it. Then ask Claude Code for a reading, or type `/wengua`.

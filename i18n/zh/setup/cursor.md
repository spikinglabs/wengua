---
description: "在 Cursor 中使用问卦 Wengua：一键安装 MCP 服务、mcp.json 配置，以及 ~/.cursor/skills 中的 Agent Skill。"
---

# Cursor

## MCP 服务

[把问卦加到 Cursor](cursor://anysphere.cursor-deeplink/mcp/install?name=wengua&config=eyJ1cmwiOiJodHRwczovL3dlbmd1YS5hbGxvLmxhbmQvbWNwIn0=){ .md-button .md-button--primary }

这个按钮会打开 Cursor 并添加托管服务。手动添加时，编辑 `~/.cursor/mcp.json`（给自己用）或项目里的 `.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "wengua": { "url": "https://wengua.allo.land/mcp" }
  }
}
```

本地服务：

```json
{
  "mcpServers": {
    "wengua": { "command": "uvx", "args": ["wengua"] }
  }
}
```

在 **Cursor Settings → MCP** 里检查，然后请智能体起卦。

## Agent Skill

```bash
mkdir -p ~/.cursor/skills
curl -fsSLo /tmp/wengua-skill.zip https://wengua.allo.land/wengua-skill.zip
unzip -o /tmp/wengua-skill.zip -d ~/.cursor/skills
```

只用于某个项目时，改为解压到 `.cursor/skills`。Cursor 也会读取 `.agents/skills` 和 `.claude/skills`。

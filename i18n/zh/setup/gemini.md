---
description: "在 Gemini CLI 中使用问卦 Wengua：一条命令添加 MCP 服务，或把 Agent Skill 安装到 ~/.gemini/skills。"
---

# Gemini

## Gemini CLI

### MCP 服务

托管服务：

```bash
gemini mcp add --scope user --transport http wengua https://wengua.allo.land/mcp
```

本地服务：

```bash
gemini mcp add --scope user wengua uvx wengua
```

也可以编辑 `~/.gemini/settings.json`（或项目里的 `.gemini/settings.json`）。Gemini CLI 对 Streamable HTTP 服务使用 `httpUrl`：

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

用 `gemini mcp list` 检查，或在会话中输入 `/mcp`。

### Agent Skill

```bash
mkdir -p ~/.gemini/skills
curl -fsSLo /tmp/wengua-skill.zip https://wengua.allo.land/wengua-skill.zip
unzip -o /tmp/wengua-skill.zip -d ~/.gemini/skills
```

也可以直接从本仓库安装：

```bash
gemini skills install https://github.com/spikinglabs/wengua.git --path skills/wengua --consent
```

用 `gemini skills list` 检查。只用于某个项目时，改为解压到 `.gemini/skills`。

## Gemini 应用

网页版和手机上的 Gemini 应用目前还不能添加自己的 MCP 服务或技能。请使用 Gemini CLI，或 [快速上手](index.md) 里的其他应用。

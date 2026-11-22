---
description: "在 GitHub Copilot 和 VS Code 中使用问卦 Wengua：用一条命令或配置文件添加 MCP 服务，并安装 Agent Skill。"
---

# GitHub Copilot（VS Code）

## MCP 服务

托管服务，一条命令：

```bash
code --add-mcp '{"name":"wengua","type":"http","url":"https://wengua.allo.land/mcp"}'
```

本地服务：

```bash
code --add-mcp '{"name":"wengua","type":"stdio","command":"uvx","args":["wengua"]}'
```

也可以写进 Copilot 的 MCP 配置文件：`~/.copilot/mcp-config.json`（给自己用），或仓库根目录下的 `.mcp.json`（给团队用）：

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

以 **Agent** 模式打开 Copilot Chat，在工具选择器里确认 Wengua 的工具已开启，然后请它起卦。

## Agent Skill

只给自己用：

```bash
mkdir -p ~/.copilot/skills
curl -fsSLo /tmp/wengua-skill.zip https://wengua.allo.land/wengua-skill.zip
unzip -o /tmp/wengua-skill.zip -d ~/.copilot/skills
```

只用于某个仓库时，改为解压到 `.github/skills` 并提交，这样在该仓库工作的每个人都能用上。

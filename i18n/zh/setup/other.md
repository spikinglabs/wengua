---
description: "在任何 MCP 客户端或 Agent Skills 平台中使用问卦 Wengua：托管的 Streamable HTTP 网址、用 uvx 或 npx 运行的本地 stdio 服务，以及技能文件夹。"
---

# 其他客户端

## 任何 MCP 客户端

| | 托管服务 | 本地服务 |
|---|---|---|
| 传输方式 | Streamable HTTP | stdio |
| 网址或命令 | `https://wengua.allo.land/mcp` | `uvx wengua`（或 `npx -y wengua`） |
| 认证 | 无 | 无 |

大多数客户端接受这种格式：

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

托管服务是无状态的：每个 POST 都返回 JSON，通知返回 202，GET 返回 405。它支持 MCP 协议版本 2024-11-05 到 2025-11-25，每个 IP 每分钟可发 60 个请求。工具、资源和提示词见 [MCP 服务](../ecosystem/mcp.md)。

## 任何 Agent Skills 平台

这个技能遵循开放的 [Agent Skills](https://agentskills.io) 标准。下载、解压，然后把 `wengua` 文件夹放到你的工具加载技能的位置。很多工具会读取 `~/.agents/skills`。

[下载 wengua-skill.zip](https://wengua.allo.land/wengua-skill.zip){ .md-button }

文件夹里有 `SKILL.md` 和 `scripts/run.py`。只需要 Python 3.10 或更高版本，别的都不需要。

---
description: "在 OpenAI Codex（命令行和 IDE 扩展）中使用问卦 Wengua：一条命令添加 MCP 服务，或把 Agent Skill 解压到 ~/.agents/skills。"
---

# Codex

以下步骤适用于 Codex 命令行和 Codex IDE 扩展，两者共用 `~/.codex/config.toml`。

## MCP 服务

托管服务：

```bash
codex mcp add wengua --url https://wengua.allo.land/mcp
```

本地服务：

```bash
codex mcp add wengua -- uvx wengua
```

也可以自己编辑 `~/.codex/config.toml`（二选一）：

```toml
# 托管服务
[mcp_servers.wengua]
url = "https://wengua.allo.land/mcp"
```

```toml
# 本地服务
[mcp_servers.wengua]
command = "uvx"
args = ["wengua"]
```

用 `codex mcp list` 检查。

## Agent Skill

只给自己用：

```bash
mkdir -p ~/.agents/skills
curl -fsSLo /tmp/wengua-skill.zip https://wengua.allo.land/wengua-skill.zip
unzip -o /tmp/wengua-skill.zip -d ~/.agents/skills
```

只用于某个仓库时，改为解压到仓库根目录下的 `.agents/skills`。你请它占卦时 Codex 会自动使用这个技能，也可以用 `$wengua` 调用。

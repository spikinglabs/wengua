---
description: "在 Claude 中使用问卦 Wengua：在 claude.ai、Claude 桌面版和手机版添加自定义连接器、上传技能，以及 Claude Code 的命令。"
---

# Claude

## Claude.ai、Claude 桌面版和手机版

### MCP 服务（自定义连接器）

在网页上添加的连接器，在 Claude 桌面应用和手机上也能用。所有方案都可以添加自定义连接器，免费版限一个。

**Pro、Max 和 Ultra**

1. 打开 [Customize → Connectors](https://claude.ai/customize/connectors)。
2. 点 **+ Add**，再点 **Add custom connector**。
3. 名称填 `Wengua`，网址填：
    ```text
    https://wengua.allo.land/mcp
    ```
4. 认证留空，点 **Add**。

**Team 和 Enterprise：** 由所有者（Owner）在 **Organization settings → Connectors → Add → Custom → Web** 用同一网址添加一次，成员再到 **Customize → Connectors → Connect** 里开启。

在对话中打开 **+** 菜单，确认 **Wengua** 已开启，然后请它起卦。Claude 会在对话里直接显示卦象卡片（本卦、之卦、变爻和选出的原文，可切换繁简）。

**如果卡片一直停在“正在起卦…”：** 删掉 Wengua 连接器，重新添加，再开一个新对话。Claude 会一直用添加连接器时加载的那版卡片，所以更新之前添加的连接器可能显示旧卡片。卦象本身在 Claude 的回答里照样有。

### Agent Skill

使用技能需要开启代码执行（**Settings → Capabilities**）。

1. [下载 wengua-skill.zip](https://wengua.allo.land/wengua-skill.zip){ .md-button }
2. 打开 [Customize → Skills](https://claude.ai/customize/skills)。
3. 点 **+**，再点 **+ Create skill**，然后点 **Upload a skill**，选择这个压缩包。不要先解压。

你请 Claude 占卦时，它会自动使用这个技能。

### Claude 桌面版使用本地服务

上面的自定义连接器最简单。如果想在自己的电脑上运行服务，请编辑 `claude_desktop_config.json`：

- macOS：`~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows：`%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "wengua": { "command": "uvx", "args": ["wengua"] }
  }
}
```

重启 Claude 桌面版。如果找不到 `uvx`，请填完整路径（macOS 用 `which uvx` 查，Windows 用 `where uvx` 查）。用 Node.js 的话，填 `"command": "npx", "args": ["-y", "wengua"]`。

## Claude Code

### MCP 服务

托管服务：

```bash
claude mcp add --transport http wengua https://wengua.allo.land/mcp
```

本地服务：

```bash
claude mcp add wengua -- uvx wengua
```

加上 `--scope user` 可在你所有项目中使用；加上 `--scope project` 则通过 `.mcp.json` 与团队共享。

### Agent Skill

只给自己用（所有项目）：

```bash
mkdir -p ~/.claude/skills
curl -fsSLo /tmp/wengua-skill.zip https://wengua.allo.land/wengua-skill.zip
unzip -o /tmp/wengua-skill.zip -d ~/.claude/skills
```

只用于某个项目时，改为解压到仓库里的 `.claude/skills` 并提交。然后请 Claude Code 起卦，或输入 `/wengua`。

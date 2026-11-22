---
description: "在 Claude、ChatGPT、Codex、Gemini、GitHub Copilot、Cursor 等 AI 中安装问卦：下载 Agent Skill，或添加免费的托管 MCP 服务。"
---

# 快速上手

问卦有两种用法，任选其一，也可以两个都装。

<div class="grid cards" markdown>

-   **MCP 服务（推荐）**

    ---

    什么都不用装，把这个网址加为连接器或 MCP 服务器：

    ```text
    https://wengua.allo.land/mcp
    ```

    免费，无需账号和 API Key，不保存你的问题。

-   **Agent Skill**

    ---

    一个压缩包，含技能说明、起卦程序和全部原文。只需 Python 3.10 以上，不联网，不需要服务器。

    [下载 wengua-skill.zip](https://wengua.allo.land/wengua-skill.zip){ .md-button .md-button--primary }

</div>

装好后直接问，例如：「帮我起一卦：这次搬家要注意什么？」或「我掷铜钱得到 7 8 9 7 6 8（自下而上），怎么解？」

## Claude

**网页版、桌面版、手机版（MCP）**：打开 [Customize → Connectors](https://claude.ai/customize/connectors)，点 **+ Add → Add custom connector**，名称填 `Wengua`，网址填 `https://wengua.allo.land/mcp`，不需要认证，点 **Add**。所有方案都可用，免费版限一个。Team / Enterprise 由所有者在 **Organization settings → Connectors → Add → Custom → Web** 添加。

**Skill**：先在 **Settings → Capabilities** 打开代码执行。下载压缩包，打开 [Customize → Skills](https://claude.ai/customize/skills)，点 **+ → + Create skill → Upload a skill**，直接上传 zip（不要解压）。

**Claude Desktop 本地服务**：编辑 `claude_desktop_config.json`（macOS：`~/Library/Application Support/Claude/`，Windows：`%APPDATA%\Claude\`）：

```json
{ "mcpServers": { "wengua": { "command": "uvx", "args": ["wengua"] } } }
```

**Claude Code**：

```bash
claude mcp add --transport http wengua https://wengua.allo.land/mcp   # 托管
claude mcp add wengua -- uvx wengua                                   # 本地
# Skill
mkdir -p ~/.claude/skills && curl -fsSLo /tmp/wengua-skill.zip https://wengua.allo.land/wengua-skill.zip && unzip -o /tmp/wengua-skill.zip -d ~/.claude/skills
```

## ChatGPT

**MCP**：在网页版打开 [chatgpt.com/plugins](https://chatgpt.com/plugins)，点 **+ → Add custom MCP server**，名称 `Wengua`，**Server URL** 填 `https://wengua.allo.land/mcp`，认证选 **No authentication**，勾选 **I understand and want to continue**，点 **Create as a plugin**，再在个人插件里安装。对话时输入 **@** 选择 Wengua。能否使用取决于你的方案和工作区管理员的设置。

**Skill**：在 ChatGPT 桌面版侧边栏打开 **Skills**，添加下载的技能。

## Codex

```bash
codex mcp add wengua --url https://wengua.allo.land/mcp   # 托管
codex mcp add wengua -- uvx wengua                        # 本地
# Skill
mkdir -p ~/.agents/skills && curl -fsSLo /tmp/wengua-skill.zip https://wengua.allo.land/wengua-skill.zip && unzip -o /tmp/wengua-skill.zip -d ~/.agents/skills
```

也可以在 `~/.codex/config.toml` 写 `[mcp_servers.wengua]` 加 `url = "https://wengua.allo.land/mcp"`。

## Gemini CLI

```bash
gemini mcp add --scope user --transport http wengua https://wengua.allo.land/mcp   # 托管
gemini mcp add --scope user wengua uvx wengua                                      # 本地
# Skill
gemini skills install https://github.com/spikinglabs/wengua.git --path skills/wengua --consent
```

在 `~/.gemini/settings.json` 中，托管服务写作 `"wengua": { "httpUrl": "https://wengua.allo.land/mcp" }`。Gemini 网页版和手机 App 目前还不能添加自定义 MCP 或技能。

## GitHub Copilot（VS Code）

```bash
code --add-mcp '{"name":"wengua","type":"http","url":"https://wengua.allo.land/mcp"}'
# Skill
mkdir -p ~/.copilot/skills && curl -fsSLo /tmp/wengua-skill.zip https://wengua.allo.land/wengua-skill.zip && unzip -o /tmp/wengua-skill.zip -d ~/.copilot/skills
```

或在 `~/.copilot/mcp-config.json` 中写入 `{"mcpServers": {"wengua": {"type": "http", "url": "https://wengua.allo.land/mcp", "tools": ["*"]}}}`。在 Copilot Chat 的 **Agent** 模式中使用。

## Cursor

[一键添加到 Cursor](cursor://anysphere.cursor-deeplink/mcp/install?name=wengua&config=eyJ1cmwiOiJodHRwczovL3dlbmd1YS5hbGxvLmxhbmQvbWNwIn0=){ .md-button .md-button--primary }

或在 `~/.cursor/mcp.json` 中写入 `{"mcpServers": {"wengua": {"url": "https://wengua.allo.land/mcp"}}}`。Skill 解压到 `~/.cursor/skills`。

## 自己的程序

- **Claude API**：`client.beta.messages.create(..., betas=["mcp-client-2025-11-20"], mcp_servers=[{"type": "url", "url": "https://wengua.allo.land/mcp", "name": "wengua"}], tools=[{"type": "mcp_toolset", "mcp_server_name": "wengua"}])`
- **OpenAI API**：`tools=[{"type": "mcp", "server_label": "wengua", "server_url": "https://wengua.allo.land/mcp", "require_approval": "never"}]`
- **Python 库**：`pip install wengua`，然后 `wengua.cast(question="…")`。

完整英文说明与配置见 [Get started](../setup/index.md)。

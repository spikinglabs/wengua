---
description: "在 Claude、ChatGPT、Codex、Gemini、GitHub Copilot、Cursor 或任何 MCP 客户端中使用问卦 Wengua：下载 Agent Skill，或添加免费的托管 MCP 服务。"
---

# 快速上手

问卦有两种用法。看你的 AI 支持哪一种就用哪一种，也可以两个都装。

<div class="grid cards" markdown>

-   **MCP 服务（推荐）**

    ---

    什么都不用装。把这个网址加为连接器或 MCP 服务器：

    ```text
    https://wengua.allo.land/mcp
    ```

    免费，无需账号，无需 API Key，从不保存你的问题。

-   **Agent Skill**

    ---

    一个压缩包，含技能说明、起卦程序和全部原文。只需要 Python 3.10 或更高版本，不联网，不需要服务器。

    [下载 wengua-skill.zip](https://wengua.allo.land/wengua-skill.zip){ .md-button .md-button--primary }

</div>

## 选择你的 AI

| AI | MCP 服务 | Agent Skill | 指南 |
|---|---|---|---|
| Claude（网页版、桌面版、手机版） | ✅ 自定义连接器 | ✅ 上传压缩包 | [Claude](claude.md) |
| Claude Code | ✅ 一条命令 | ✅ 解压到 `~/.claude/skills` | [Claude](claude.md#claude-code) |
| ChatGPT | ✅ 自定义 MCP 服务器 | ✅ 桌面应用 | [ChatGPT](chatgpt.md) |
| Codex | ✅ 一条命令 | ✅ 解压到 `~/.agents/skills` | [Codex](codex.md) |
| Gemini CLI | ✅ 一条命令 | ✅ 解压到 `~/.gemini/skills` | [Gemini](gemini.md) |
| GitHub Copilot（VS Code） | ✅ 一条命令 | ✅ 解压到 `~/.copilot/skills` | [GitHub Copilot](copilot.md) |
| Cursor | ✅ 一键安装 | ✅ 解压到 `~/.cursor/skills` | [Cursor](cursor.md) |
| 你自己的应用或智能体 | ✅ Claude API、OpenAI API | ✅ Python 与 TypeScript 库 | [API 与程序库](api.md) |
| 其他 MCP 客户端 | ✅ 网址或 `uvx wengua` | ✅ 任何 Agent Skills 文件夹 | [其他客户端](other.md) |

## 然后直接问

可以试试：

- 「帮我起一卦：关于换工作，我应当明白什么？」
- 「我掷铜钱得到 7 8 9 7 6 8（自下而上），怎么解？」
- 「讲讲第三卦屯卦。」
- "Cast an I Ching hexagram for me. My question: what should I understand about this move?"

AI 会用真正的随机数起卦，用繁体或简体引用选出的原文，说明是按哪条规则选的，然后再解读。

## 不用托管服务，改用本地服务

每份指南也介绍了本地服务：它通过 stdio 在你自己的电脑上运行，需要 [uv](https://docs.astral.sh/uv/getting-started/installation/)（提供 `uvx`）：

```bash
uvx wengua            # 运行 MCP 服务
uvx wengua cast -q "这次搬家我应当明白什么？"
```

也可以用 `pip install wengua` 安装，然后运行 `wengua`。装有 Node.js 20 或更高版本时，`npx -y wengua` 效果相同。

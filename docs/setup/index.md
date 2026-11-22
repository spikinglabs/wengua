---
description: "Set up Wengua 问卦 in Claude, ChatGPT, Codex, Gemini, GitHub Copilot, Cursor or any MCP client: download the Agent Skill or add the free hosted MCP server."
---

# Get started

Wengua works in two ways. Pick whichever your AI supports, or use both.

<div class="grid cards" markdown>

-   **MCP server (recommended)**

    ---

    Nothing to install. Add this URL as a connector or MCP server:

    ```text
    https://wengua.allo.land/mcp
    ```

    Free, no account, no API key. Your questions are never stored.

-   **Agent Skill**

    ---

    One zip with the skill, the casting code and the full text. It needs only Python 3.10 or later, with no network and no server.

    [Download wengua-skill.zip](https://wengua.allo.land/wengua-skill.zip){ .md-button .md-button--primary }

</div>

## Pick your AI

| AI | MCP server | Agent Skill | Guide |
|---|---|---|---|
| Claude (claude.ai, Desktop, mobile) | ✅ Custom connector | ✅ Upload the zip | [Claude](claude.md) |
| Claude Code | ✅ One command | ✅ Unzip into `~/.claude/skills` | [Claude](claude.md#claude-code) |
| ChatGPT | ✅ Custom MCP server | ✅ Desktop app | [ChatGPT](chatgpt.md) |
| Codex | ✅ One command | ✅ Unzip into `~/.agents/skills` | [Codex](codex.md) |
| Gemini CLI | ✅ One command | ✅ Unzip into `~/.gemini/skills` | [Gemini](gemini.md) |
| GitHub Copilot (VS Code) | ✅ One command | ✅ Unzip into `~/.copilot/skills` | [GitHub Copilot](copilot.md) |
| Cursor | ✅ One click | ✅ Unzip into `~/.cursor/skills` | [Cursor](cursor.md) |
| Your own app or agent | ✅ Claude API, OpenAI API | ✅ Python and TypeScript library | [APIs and libraries](api.md) |
| Any other MCP client | ✅ URL or `uvx wengua` | ✅ Any Agent Skills folder | [Other clients](other.md) |

## Then ask

Try one of these:

- "Cast an I Ching hexagram for me. My question: what should I understand about changing jobs?"
- "I threw coins and got 7 8 9 7 6 8, bottom to top. What does it say?"
- "Tell me about hexagram 3, 屯."
- 「帮我起一卦：这次搬家要注意什么？」

The AI casts with real randomness, quotes the selected Chinese text in traditional or simplified script, explains which rule chose it, and then interprets.

## Local server instead of hosted

Every guide also shows the local server, which runs on your own computer over stdio. It needs [uv](https://docs.astral.sh/uv/getting-started/installation/) (for `uvx`):

```bash
uvx wengua            # runs the MCP server
uvx wengua cast -q "What should I understand about this move?"
```

Or install it with `pip install wengua`, then run `wengua`. With Node.js 20 or later, `npx -y wengua` does the same.

---
description: "Set up Wengua 问卦 in ChatGPT: add the hosted MCP server as a custom plugin, or add the Agent Skill in the ChatGPT desktop app."
---

# ChatGPT

## MCP server (custom plugin)

On the ChatGPT website:

1. Go to [chatgpt.com/plugins](https://chatgpt.com/plugins).
2. Click **+**, then **Add custom MCP server**.
3. Name: `Wengua`. Under **Connection**, set **Server URL** to:
    ```text
    https://wengua.allo.land/mcp
    ```
4. Authentication: **No authentication**.
5. Tick **I understand and want to continue**, then click **Create as a plugin**.
6. Find Wengua under your personal plugins and install it.

In a chat, type **@**, pick **Wengua**, and ask for a reading. ChatGPT shows the reading card inline. Whether custom MCP servers are available depends on your plan and, in a workspace, on what your admin allows.

## Agent Skill

The ChatGPT desktop app supports Agent Skills:

1. [Download wengua-skill.zip](https://wengua.allo.land/wengua-skill.zip){ .md-button }
2. Open **Skills** in the sidebar of the ChatGPT desktop app and add the downloaded skill.
3. In a chat, type **@** and pick **wengua**, or just ask for an I Ching reading.

For Codex (the CLI and the IDE extension), see [Codex](codex.md).

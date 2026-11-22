---
description: "在 ChatGPT 中使用问卦 Wengua：把托管 MCP 服务添加为自定义插件，或在 ChatGPT 桌面应用中添加 Agent Skill。"
---

# ChatGPT

## MCP 服务（自定义插件）

在 ChatGPT 网站上：

1. 打开 [chatgpt.com/plugins](https://chatgpt.com/plugins)。
2. 点 **+**，再点 **Add custom MCP server**。
3. 名称填 `Wengua`。在 **Connection** 下把 **Server URL** 设为：
    ```text
    https://wengua.allo.land/mcp
    ```
4. 认证选 **No authentication**。
5. 勾选 **I understand and want to continue**，再点 **Create as a plugin**。
6. 在你的个人插件里找到 Wengua 并安装。

在对话中输入 **@**，选 **Wengua**，然后请它起卦。ChatGPT 会在对话里直接显示卦象卡片。能否添加自定义 MCP 服务器取决于你的方案；在工作区里，还取决于管理员的设置。

## Agent Skill

ChatGPT 桌面应用支持 Agent Skills：

1. [下载 wengua-skill.zip](https://wengua.allo.land/wengua-skill.zip){ .md-button }
2. 在 ChatGPT 桌面应用的侧边栏打开 **Skills**，添加下载的技能。
3. 在对话中输入 **@** 并选 **wengua**，或者直接请它占卦。

Codex（命令行和 IDE 扩展）请看 [Codex](codex.md)。

---
description: "问卦 Wengua 隐私政策：托管 MCP 服务和网站不保存问题、卦象或任何个人数据。"
---

# 隐私

最后更新：2026 年 11 月 22 日（加入网页起卦）

问卦是 SpikingLabs 运营的开源项目。本政策适用于 `wengua.allo.land` 上的网站和托管 MCP 服务。中文版与英文版如有出入，以[英文版](https://wengua.allo.land/privacy/)为准。

## 托管 MCP 服务

- **没有账号，也没有 API Key。** 你不需要注册或登录。
- **不保存你的问题和卦象。** 服务在内存中处理每个请求，回答后立即忘记。它没有数据库，请求日志也已关闭。
- **限流。** 为了让免费服务保持可用，托管服务商（Cloudflare）会按 IP 地址统计 60 秒内的请求数。这些计数与你问了什么无关，也不会保留。
- **不追踪。** 没有 Cookie，没有统计分析，没有广告。

你使用的 AI 应用（例如 Claude 或 ChatGPT）在调用工具时会把你的问题发给问卦。该应用如何处理你的对话，由它自己的隐私政策规定。

## 网站

文档网站是静态的，不设置 Cookie，也不做统计分析。首页的起卦框会像 AI 应用一样向上面的托管服务请求起卦。它只发送起卦方法，从不发送你的问题：问题只留在你的浏览器里，仅用于显示给你看，以及放进你可以复制给 AI 的文字里。托管网站的 Cloudflare 可能按 [Cloudflare 隐私政策](https://www.cloudflare.com/privacypolicy/) 保留一般的安全和流量数据。

## 本地使用

Python 和 npm 包、命令行、本地 MCP 服务和 Agent Skill 完全在你自己的电脑上运行，不发出任何网络请求，也不向我们发送任何内容。

## 联系

如有疑问或顾虑，请在 <https://github.com/spikinglabs/wengua/issues> 提交 issue。

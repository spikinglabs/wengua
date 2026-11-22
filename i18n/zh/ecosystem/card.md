---
description: "问卦 Wengua 卦象卡片：一个 MCP Apps 视图，在 Claude 和 ChatGPT 对话中直接画出所起之卦、变爻和选出的文字。"
---

# 卦象卡片

一个 [MCP Apps](https://github.com/modelcontextprotocol/ext-apps) 视图，`ui://wengua/reading/<hash>`，由 `cast` 和 `read_cast` 工具引用。支持 MCP Apps 的客户端会在回答下方直接显示它，其他客户端则只以文字形式得到结果。

卡片会：

- 画出本卦并标出变爻（○ 老阳，✕ 老阴），旁边是之卦；
- 列出选出的文字及其作用（主、辅；三爻变时为贞、悔）和选出它们的规则；
- 可切换繁體 / 简体，如果起卦时的 `locale` 要求简体，就以简体打开；
- 跟随宿主应用的主题颜色和字体，并标出用种子生成的测试结果。

它是一个不发出任何外部请求的 HTML 文件（`spec/reading-card.html`），直接使用 MCP Apps 的 postMessage 协议，不依赖 SDK。

它与宿主的通信方式：

1. 发送 `ui/initialize`（带 `appInfo` 和 `appCapabilities`），然后发送 `ui/notifications/initialized`。即使宿主拒绝或一直不回应，它最多 1.5 秒后也会发送 `initialized`，因为宿主要看到它才会送出工具数据。
2. 根据 `ui/notifications/tool-result` 画出结果，用 `structuredContent`，没有的话就用文字内容里的 JSON。
3. 以读者的字体打开。依次参考：读者自己的繁简选择（宿主允许存储时会记住）、模型传给工具的 `locale`、宿主的语言（zh-CN、zh-SG、zh-MY 为简体，zh-TW、zh-HK、zh-MO 为繁体），否则用繁体。读者切换字体时，如果宿主支持 `ui/update-model-context`，卡片会告诉模型，之后的回答和起卦就用同一字体。
4. 回应宿主请求（如 `ui/resource-teardown`），并跟随 `ui/notifications/host-context-changed`。
5. 如果 12 秒内没有收到结果，就提示结果在回答里，而不是一直显示“正在起卦…”。有些手机应用会显示卡片，但还不会送出结果。

`cast` 和 `read_cast` 的结果也在 `_meta.ui.resourceUri` 中带有卡片链接，供在那里查找的宿主使用。

卡片的 URI 以其 HTML 的哈希值结尾，所以缓存 UI 资源的客户端在卡片改动后会马上用上新版。占位画面会显示一个小小的版本标签（如“card 4”），可以看出客户端用的是哪一版卡片。

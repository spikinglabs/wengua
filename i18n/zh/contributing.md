---
description: "如何用 Zensical 编辑问卦 Wengua 的文档、维护三种语言的版本，以及如何发布。"
---

# 参与贡献

## 编辑文档

网站用 [Zensical](https://zensical.org) 构建。英文页面在 `docs/`，导航在 `zensical.toml`。

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-docs.txt
zensical serve                   # 在 http://localhost:8000 实时预览英文网站
python scripts/build_site.py     # 把三种语言都构建到 site/
```

### 语言

网站有英文（`/`）、简体中文（`/zh/`）和繁体中文（`/zh-hant/`）三个版本，页面一一对应：

- 英文页面在 `docs/`。
- 简体中文页面在 `i18n/zh/`，路径与英文页面相同，由人工撰写。
- 繁体中文在构建时由 [OpenCC](https://github.com/BYVoid/OpenCC)（`s2twp`：台湾标准字形和用词）从 `i18n/zh/` 生成。行内代码保持原样；代码块也会转换，除非它前一行是 `<!-- no-convert -->`。不要编辑生成的文件。
- 中文导航标题和网站名称在 `scripts/build_site.py` 里。

如果某个英文页面没有中文版本（或反过来），`python scripts/build_site.py` 会拒绝构建，所以新增或修改页面的拉取请求应当同时更新两种语言。页眉的语言菜单会让读者停留在同一页面。

每个拉取请求都会构建网站。每次推送到 `main` 都会部署到 <https://wengua.allo.land>，这是唯一的正式网址。一个 Cloudflare Worker（`worker/`）以静态资源的方式提供网站，并在 `/mcp` 提供托管 MCP 服务。旧地址 `spikinglabs.github.io/wengua` 的每个页面都会跳转到这里。

### 拉取请求预览

本仓库的每个拉取请求都有一个预览网址 `https://pr-<编号>.wengua-docs-preview.pages.dev`，链接会由机器人发在评论里。预览放在单独的 Cloudflare Pages 域名上，不会被收录：每个页面都带 `noindex`，服务器发送 `X-Robots-Tag: noindex`，`robots.txt` 禁止抓取，没有站点地图，规范链接指向正式网站。

预览和正式部署使用两个仓库密钥：`CLOUDFLARE_API_TOKEN`（需要 *Cloudflare Pages: Edit*、*Workers Scripts: Edit*，以及 allo.land 上的 *Workers Routes: Edit* 和 *DNS: Edit* 权限）和 `CLOUDFLARE_ACCOUNT_ID`。没有它们，预览任务会被跳过。

### 搜索与 AI 可见性（SEO 与 GEO）

- 每个页面的 front matter 都要有 `description`。它会成为页面的 meta description，以及 `llms.txt` 里的摘要。
- `scripts/llms_txt.py` 在每次构建后生成 [`llms.txt`](https://llmstxt.org) 和 `llms-full.txt`，让 AI 助手和回答引擎能干净地读取文档。
- `docs/robots.txt` 允许所有爬虫（包括 AI 爬虫），并指向三种语言的站点地图。
- 只有正式网站是规范版本。不要在别处发布不带 `noindex` 的文档副本。

**保持文档最新：** 改变行为、新增工具或完成里程碑的拉取请求，应在同一个请求里更新相应页面（英文和中文）以及[路线图](roadmap.md)。

## 发布

两个包使用同一个版本号（`python/pyproject.toml` 和 `js/package.json`）。

- **PyPI：** 发布一个标签为 `vX.Y.Z` 的 GitHub release，或运行 *Publish to PyPI* 工作流。它使用可信发布（环境 `pypi`），不存储任何令牌。
- **npm：** 运行 *Publish to npm* 工作流（环境 `npm`）。它带出处证明发布，并拒绝发布 npm 上已有的版本。在 npmjs.com 上设好可信发布者之前，它需要 `NPM_TOKEN` 密钥。

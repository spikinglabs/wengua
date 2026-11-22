---
description: "Privacy policy for Wengua 问卦: the hosted MCP server and website store no questions, no readings and no personal data."
---

# Privacy

Last updated: 22 November 2026

Wengua is run by SpikingLabs as an open-source project. This policy covers the website and the hosted MCP server at `wengua.allo.land`.

## The hosted MCP server

- **No accounts and no API keys.** You don't sign up or sign in.
- **Your questions and readings are not stored.** The server handles each request in memory and forgets it as soon as it has answered. It has no database, and request logging is turned off.
- **Rate limiting.** To keep the free service available, the hosting provider (Cloudflare) counts requests per IP address for 60 seconds. Those counters aren't linked to what you asked, and they aren't kept.
- **No tracking.** No cookies, no analytics and no advertising.

The AI app you use (for example Claude or ChatGPT) sends your question to Wengua when it calls a tool. What that app does with your conversation is covered by its own privacy policy.

## The website

The documentation site is static. It sets no cookies and runs no analytics. Cloudflare, which hosts it, may keep standard security and traffic data under the [Cloudflare privacy policy](https://www.cloudflare.com/privacypolicy/).

## Local use

The Python and npm packages, the CLI, the local MCP server and the Agent Skill run entirely on your own computer. They make no network requests and send nothing to us.

## Contact

Questions or concerns: open an issue at <https://github.com/spikinglabs/wengua/issues>.

/**
 * wengua.allo.land: the docs site as static assets, and the hosted MCP server at
 * /mcp (Streamable HTTP, stateless, JSON responses, no logging of questions).
 */
import { handlePayload } from "../../js/src/mcp.js";

interface RateLimit { limit(o: { key: string }): Promise<{ success: boolean }> }
interface Env { RATE_LIMITER?: RateLimit; ASSETS?: { fetch(r: Request): Promise<Response> } }

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Accept, Mcp-Protocol-Version, Mcp-Session-Id, Authorization",
  "Access-Control-Expose-Headers": "Mcp-Protocol-Version",
};

const json = (body: unknown, status = 200, extra: Record<string, string> = {}) =>
  new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json", ...CORS, ...extra } });

const rpcError = (code: number, message: string, status: number) =>
  json({ jsonrpc: "2.0", id: null, error: { code, message } }, status);

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });

    if (url.pathname !== "/mcp" && url.pathname !== "/mcp/") {
      return env.ASSETS ? env.ASSETS.fetch(request) : json({ error: "not found" }, 404);
    }
    // No server-initiated streams: this server is stateless.
    if (request.method === "GET" || request.method === "DELETE") {
      return new Response(null, { status: 405, headers: { Allow: "POST, OPTIONS", ...CORS } });
    }
    if (request.method !== "POST") return new Response(null, { status: 405, headers: { Allow: "POST, OPTIONS", ...CORS } });

    if (env.RATE_LIMITER) {
      const ip = request.headers.get("CF-Connecting-IP") ?? "unknown";
      const { success } = await env.RATE_LIMITER.limit({ key: ip });
      if (!success) return rpcError(-32000, "Too many requests, please slow down.", 429);
    }

    if (Number(request.headers.get("Content-Length") ?? 0) > 64 * 1024) return rpcError(-32600, "Request too large", 413);
    let payload: unknown;
    try {
      payload = await request.json();
    } catch {
      return rpcError(-32700, "Parse error", 400);
    }
    const out = handlePayload(payload);
    if (out === null) return new Response(null, { status: 202, headers: CORS });
    const version = request.headers.get("Mcp-Protocol-Version");
    return json(out, 200, version ? { "Mcp-Protocol-Version": version } : {});
  },
};

/**
 * A dependency-free MCP server core. `handle` answers one JSON-RPC message and is
 * shared by the stdio server (`npx wengua`) and the hosted Cloudflare Worker.
 * Tool definitions, instructions and the prompt come from mcp.json, shared with Python.
 */
import specJson from "./mcp.json" with { type: "json" };
import { bundle, hexagram, hexagramByBinary, trigrams, type Hexagram } from "./data.js";
import { inverse, nuclear, opposite } from "./derive.js";
import { find, get } from "./lookup.js";
import { cast, readCast, summary, type Method } from "./reading.js";
import { VERSION } from "./version.js";

export const PROTOCOL_VERSIONS = ["2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"];

interface Prompt { name: string; title: string; description: string; arguments: unknown[]; template: string }
interface UiResource { uri: string; name: string; title: string; description: string; mimeType: string; text: string }
interface Spec { name: string; title: string; instructions: string; tools: { name: string; _meta?: Json }[]; prompts: Prompt[]; ui_resources?: UiResource[] }
export const spec = specJson as unknown as Spec;

type Json = Record<string, unknown>;
export interface Message { jsonrpc?: string; id?: string | number | null; method?: string; params?: Json }

class ToolError extends Error {}

const withText = (h: Hexagram) => ({ ...summary(h), judgment: h.judgment });

function relations(args: Json) {
  const h = get(args.hexagram as string);
  const changing = [...new Set((args.changing_lines as number[] | undefined) ?? [])].sort((a, b) => a - b);
  if (changing.some((p) => !(p >= 1 && p <= 6))) throw new ToolError("changing_lines are positions 1 to 6");
  const bits = [...h.binary];
  for (const p of changing) bits[p - 1] = bits[p - 1] === "1" ? "0" : "1";
  return {
    hexagram: withText(h),
    changing_lines: changing,
    relating: changing.length ? withText(hexagramByBinary(bits.join(""))) : null,
    nuclear: withText(hexagramByBinary(nuclear(h.binary))),
    opposite: withText(hexagramByBinary(opposite(h.binary))),
    inverse: withText(hexagramByBinary(inverse(h.binary))),
  };
}

function lookup(args: Json) {
  const found = find(args.query as string);
  if (!found.length) throw new ToolError(`No hexagram matches ${JSON.stringify(args.query)}. Try a number 1-64, a Chinese name or pinyin.`);
  if (found.length > 1) {
    return { ambiguous: true, matches: found.map(summary), hint: "Several hexagrams match; ask the user which one, or look up by number." };
  }
  return found[0];
}

export function callTool(name: string, args: Json = {}): unknown {
  const rule = (args.rule as string | undefined) ?? undefined;
  const locale = (args.locale as string | undefined) ?? undefined;
  const question = (args.question as string | undefined) ?? undefined;
  switch (name) {
    case "cast":
      return cast({ question, method: ((args.method as Method | undefined) ?? "coins"), rule, locale });
    case "read_cast":
      if (!Array.isArray(args.lines)) throw new ToolError("lines is required: six values bottom to top");
      return readCast(args.lines as never, { question, rule, locale });
    case "lookup":
      return lookup(args);
    case "relations":
      return relations(args);
    default:
      throw new ToolError(`Unknown tool ${JSON.stringify(name)}`);
  }
}

function resources() {
  return [
    ...bundle.hexagrams.map((h) => ({
      uri: `wengua://hexagram/${h.number}`, name: `hexagram-${h.number}`,
      title: `${h.unicode} ${h.number} ${h.name.zh_hant} / ${h.name.zh_hans} ${h.name.pinyin} · ${h.name.en}`,
      mimeType: "application/json",
    })),
    ...trigrams().map((t) => ({
      uri: `wengua://trigram/${t.key}`, name: `trigram-${t.key}`,
      title: `${t.symbol} ${t.name.zh_hant} ${t.name.pinyin} · ${t.name.en}`, mimeType: "application/json",
    })),
    ...(spec.ui_resources ?? []).map(({ text: _t, ...r }) => r),
  ];
}

function readResource(uri: string) {
  const ui = spec.ui_resources?.find((r) => r.uri === uri);
  if (ui) return { contents: [{ uri, mimeType: ui.mimeType, text: ui.text }] };
  let body: unknown;
  if (uri.startsWith("wengua://hexagram/")) body = hexagram(Number(uri.slice("wengua://hexagram/".length)));
  else if (uri.startsWith("wengua://trigram/")) body = trigrams().find((t) => t.key === uri.slice("wengua://trigram/".length));
  if (!body) throw new Error("not found");
  return { contents: [{ uri, mimeType: "application/json", text: JSON.stringify(body) }] };
}

/** Handle one JSON-RPC message; returns the response, or null for a notification. */
export function handle(msg: Message): Json | null {
  const { method, id, params = {} } = msg;
  if (id === undefined || id === null) return null;
  const ok = (result: unknown) => ({ jsonrpc: "2.0", id, result });
  const err = (code: number, message: string) => ({ jsonrpc: "2.0", id, error: { code, message } });

  switch (method) {
    case "initialize": {
      const requested = params.protocolVersion as string;
      return ok({
        protocolVersion: PROTOCOL_VERSIONS.includes(requested) ? requested : PROTOCOL_VERSIONS[0],
        capabilities: { tools: {}, resources: {}, prompts: {} },
        serverInfo: { name: spec.name, title: spec.title, version: VERSION },
        instructions: spec.instructions,
      });
    }
    case "ping":
      return ok({});
    case "tools/list":
      return ok({ tools: spec.tools });
    case "tools/call": {
      try {
        const result = callTool(params.name as string, (params.arguments as Json) ?? {});
        const meta = spec.tools.find((t) => t.name === params.name)?._meta;
        // Some hosts look for the card on the result as well as on tools/list.
        return ok({ content: [{ type: "text", text: JSON.stringify(result) }], structuredContent: result, ...(meta ? { _meta: meta } : {}) });
      } catch (e) {
        return ok({ content: [{ type: "text", text: (e as Error).message }], isError: true });
      }
    }
    case "resources/list":
      return ok({ resources: resources() });
    case "resources/templates/list":
      return ok({
        resourceTemplates: [
          { uriTemplate: "wengua://hexagram/{number}", name: "hexagram", mimeType: "application/json", description: "A hexagram by King Wen number, 1-64, with all texts" },
          { uriTemplate: "wengua://trigram/{key}", name: "trigram", mimeType: "application/json", description: "A trigram: qian, dui, li, zhen, xun, kan, gen, kun" },
        ],
      });
    case "resources/read":
      try { return ok(readResource(String(params.uri ?? ""))); } catch { return err(-32002, `Resource not found: ${params.uri}`); }
    case "prompts/list":
      return ok({ prompts: spec.prompts.map(({ template: _t, ...p }) => p) });
    case "prompts/get": {
      const p = spec.prompts.find((x) => x.name === params.name);
      if (!p) return err(-32602, `Unknown prompt: ${params.name}`);
      const q = (params.arguments as Json | undefined)?.question as string | undefined;
      const text = p.template.replace("{question_part}", q ? ` My question: ${q}` : "");
      return ok({ description: p.description, messages: [{ role: "user", content: { type: "text", text } }] });
    }
    default:
      return err(-32601, `Method not found: ${method}`);
  }
}

/** Handle a raw JSON-RPC payload (a message or a batch). Returns the response body, or null. */
export function handlePayload(payload: unknown): unknown {
  if (Array.isArray(payload)) {
    const out = payload.map((m) => handle(m as Message)).filter((r) => r !== null);
    return out.length ? out : null;
  }
  return handle(payload as Message);
}

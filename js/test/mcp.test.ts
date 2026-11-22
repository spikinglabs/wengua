import { test } from "node:test";
import assert from "node:assert/strict";
import { handle, handlePayload, spec } from "../src/mcp.js";

const rpc = (method: string, params: Record<string, unknown> = {}) =>
  handle({ jsonrpc: "2.0", id: 1, method, params }) as { result?: any; error?: any };

test("initialize negotiates the protocol version", () => {
  assert.equal(rpc("initialize", { protocolVersion: "2025-06-18" }).result.protocolVersion, "2025-06-18");
  assert.equal(rpc("initialize", { protocolVersion: "1999-01-01" }).result.protocolVersion, "2025-11-25");
  assert.match(rpc("initialize").result.instructions, /Never invent/);
});

test("tools and their results", () => {
  assert.deepEqual(rpc("tools/list").result.tools.map((t: any) => t.name), spec.tools.map((t) => t.name));
  const r = rpc("tools/call", { name: "cast", arguments: { method: "yarrow", question: "q" } }).result;
  assert.equal(r.structuredContent.method, "yarrow");
  const t = r.structuredContent.selection.texts[0].text;
  assert.ok(t.zh_hant && t.zh_hans);
  assert.deepEqual(JSON.parse(r.content[0].text), r.structuredContent);
  const rel = rpc("tools/call", { name: "relations", arguments: { hexagram: "屯", changing_lines: [1] } }).result;
  assert.equal(rel.structuredContent.relating.number, 8);
  assert.equal(rpc("tools/call", { name: "lookup", arguments: { query: "kun" } }).result.structuredContent.ambiguous, true);
});

test("errors", () => {
  assert.equal(rpc("tools/call", { name: "read_cast", arguments: { lines: [1, 2] } }).result.isError, true);
  assert.equal(rpc("tools/call", { name: "lookup", arguments: { query: "zzz" } }).result.isError, true);
  assert.equal(rpc("nope").error.code, -32601);
  assert.equal(handle({ jsonrpc: "2.0", method: "notifications/initialized" }), null);
  assert.equal(handlePayload([{ jsonrpc: "2.0", method: "notifications/initialized" }]), null);
});

test("resources and prompt", () => {
  assert.equal(rpc("resources/list").result.resources.length, 72);
  const body = JSON.parse(rpc("resources/read", { uri: "wengua://hexagram/1" }).result.contents[0].text);
  assert.equal(body.name.zh_hant, "乾");
  assert.match(rpc("prompts/get", { name: "reading", arguments: { question: "my job" } }).result.messages[0].content.text, /my job/);
});

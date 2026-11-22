/** The MCP server over stdio: one JSON-RPC message per line. */
import { createInterface } from "node:readline";
import { handlePayload } from "./mcp.js";

export function serveStdio(): void {
  const rl = createInterface({ input: process.stdin });
  rl.on("line", (line) => {
    if (!line.trim()) return;
    let out: unknown;
    try {
      out = handlePayload(JSON.parse(line));
    } catch {
      out = { jsonrpc: "2.0", id: null, error: { code: -32700, message: "Parse error" } };
    }
    if (out !== null) process.stdout.write(JSON.stringify(out) + "\n");
  });
}

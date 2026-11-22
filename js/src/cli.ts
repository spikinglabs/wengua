#!/usr/bin/env node
/** wengua command line. With no arguments (as `npx wengua` in an MCP client), runs the MCP server over stdio. */
import { find } from "./lookup.js";
import { cast, readCast, METHODS, type Method, type Reading } from "./reading.js";
import { RULES } from "./selection.js";
import { serveStdio } from "./stdio.js";
import { VERSION } from "./version.js";
import type { Hexagram, Text } from "./data.js";

const YANG = "━━━━━━━━━", YIN = "━━━   ━━━";
const both = (t: Text) => (t.zh_hant === t.zh_hans ? t.zh_hant : `${t.zh_hant} / ${t.zh_hans}`);
const title = (h: { unicode: string; number: number; name: Hexagram["name"] }) =>
  `${h.unicode} ${h.number} ${both(h.name)} ${h.name.pinyin} · ${h.name.en}`;

function render(r: Reading): string {
  const out: string[] = [];
  if (r.question) out.push(`Question: ${r.question}`);
  out.push(title(r.primary) + (r.relating ? `  →  ${title(r.relating)}` : ""));
  for (let i = 5; i >= 0; i--) {
    const v = r.values[i]!;
    out.push(`  ${v === 7 || v === 9 ? YANG : YIN}${v === 9 ? " ○ 9" : v === 6 ? " ✕ 6" : `   ${v}`}`);
  }
  const s = r.selection;
  out.push("", s.explanation.zh_hant, s.explanation.zh_hans, s.explanation.en);
  for (const t of s.texts) {
    out.push(`  [${t.hexagram} ${t.label ? both(t.label) : "卦辭 / 卦辞"}] (${t.role})`);
    out.push(`    ${t.text.zh_hant}`);
    if (t.text.zh_hans !== t.text.zh_hant) out.push(`    ${t.text.zh_hans}`);
  }
  out.push("", `互 ${both(r.nuclear.name)} · 錯/错 ${both(r.opposite.name)} · 綜/综 ${both(r.inverse.name)}`);
  const a = r.audit;
  out.push(`${r.method} · rng ${a.rng}${a.test ? " (TEST, not a real reading)" : ""} · ${a.library} · ${a.dataset}`);
  return out.join("\n");
}

const HELP = `wengua ${VERSION}: consult the I Ching. Code casts, the model reads.

  wengua                      run the MCP server over stdio (for MCP clients)
  wengua mcp                  the same
  wengua cast [-q QUESTION] [-m coins|yarrow] [--rule zhuxi|all] [--json] [--seed N]
  wengua read V1 .. V6 [-q QUESTION] [--rule zhuxi|all] [--json]   six values bottom to top, e.g. 7 8 9 7 6 8
  wengua lookup QUERY [--json]
`;

function main(argv: string[]): number {
  const [cmd, ...rest] = argv;
  if (!cmd || cmd === "mcp") { serveStdio(); return -1; }
  if (cmd === "-h" || cmd === "--help" || cmd === "help") { process.stdout.write(HELP); return 0; }
  if (cmd === "--version" || cmd === "-v") { console.log(`wengua ${VERSION}`); return 0; }

  const opts: Record<string, string | boolean> = {};
  const pos: string[] = [];
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i]!;
    if (a === "--json") opts.json = true;
    else if (a === "-q" || a === "--question") opts.question = rest[++i] ?? "";
    else if (a === "-m" || a === "--method") opts.method = rest[++i] ?? "";
    else if (a === "--rule") opts.rule = rest[++i] ?? "";
    else if (a === "--seed") opts.seed = rest[++i] ?? "";
    else pos.push(a);
  }
  try {
    if (cmd === "lookup") {
      const found = find(pos.join(" "));
      if (!found.length) { console.error("No hexagram matches."); return 1; }
      if (opts.json) console.log(JSON.stringify(found.length > 1 ? found : found[0], null, 2));
      else for (const h of found) {
        console.log(title(h));
        console.log(`  ${h.judgment.zh_hant}`);
        if (h.judgment.zh_hans !== h.judgment.zh_hant) console.log(`  ${h.judgment.zh_hans}`);
      }
      return 0;
    }
    let r: Reading;
    const rule = (opts.rule as string) || undefined;
    if (rule && !(RULES as readonly string[]).includes(rule)) throw new RangeError(`--rule must be one of ${RULES.join(", ")}`);
    if (cmd === "cast") {
      const method = ((opts.method as string) || "coins") as Method;
      if (!METHODS.includes(method)) throw new RangeError(`--method must be one of ${METHODS.join(", ")}`);
      const seed = opts.seed !== undefined ? Number(opts.seed) : undefined;
      r = cast({ question: (opts.question as string) || null, method, rule, ...(seed !== undefined ? { seed, mode: "test" as const } : {}) });
    } else if (cmd === "read") {
      if (pos.length !== 6) throw new RangeError("give six values, bottom to top");
      r = readCast(pos, { question: (opts.question as string) || null, rule });
    } else {
      process.stderr.write(HELP);
      return 2;
    }
    console.log(opts.json ? JSON.stringify(r, null, 2) : render(r));
    return 0;
  } catch (e) {
    console.error(`wengua: ${(e as Error).message}`);
    return 2;
  }
}

const code = main(process.argv.slice(2));
if (code >= 0) process.exitCode = code;

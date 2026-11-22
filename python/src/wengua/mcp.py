"""A dependency-free MCP server over stdio (JSON-RPC 2.0, one message per line).

Tool definitions, instructions and the prompt live in data/mcp.json, shared with
the TypeScript server so both behave the same.
"""

from __future__ import annotations

import json
import sys
from functools import lru_cache
from importlib import resources

from . import __version__
from .data import bundle, hexagram, hexagram_by_binary, trigrams
from .derive import inverse, nuclear, opposite
from .lookup import find, get
from .reading import cast, read_cast, summary

PROTOCOL_VERSIONS = ("2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05")


@lru_cache(maxsize=1)
def spec() -> dict:
    with resources.files(__package__).joinpath("data/mcp.json").open(encoding="utf-8") as f:
        return json.load(f)


class ToolError(Exception):
    pass


def _relations(args: dict) -> dict:
    h = get(args["hexagram"])
    changing = sorted(set(args.get("changing_lines") or []))
    if any(not 1 <= p <= 6 for p in changing):
        raise ToolError("changing_lines are positions 1 to 6")
    bits = list(h["binary"])
    for p in changing:
        bits[p - 1] = "0" if bits[p - 1] == "1" else "1"
    with_text = lambda x: {**summary(x), "judgment": x["judgment"]}  # noqa: E731
    return {
        "hexagram": with_text(h),
        "changing_lines": changing,
        "relating": with_text(hexagram_by_binary("".join(bits))) if changing else None,
        "nuclear": with_text(hexagram_by_binary(nuclear(h["binary"]))),
        "opposite": with_text(hexagram_by_binary(opposite(h["binary"]))),
        "inverse": with_text(hexagram_by_binary(inverse(h["binary"]))),
    }


def _lookup(args: dict) -> dict:
    found = find(args["query"])
    if not found:
        raise ToolError(f"No hexagram matches {args['query']!r}. Try a number 1-64, a Chinese name or pinyin.")
    if len(found) > 1:
        return {"ambiguous": True, "matches": [summary(h) for h in found],
                "hint": "Several hexagrams match; ask the user which one, or look up by number."}
    return found[0]


def call_tool(name: str, args: dict) -> dict:
    args = args or {}
    opts = {k: args.get(k) for k in ("rule", "locale") if args.get(k) is not None}
    if name == "cast":
        return cast(args.get("question"), args.get("method") or "coins", **opts)
    if name == "read_cast":
        if "lines" not in args:
            raise ToolError("lines is required: six values bottom to top")
        return read_cast(args["lines"], args.get("question"), **opts)
    if name == "lookup":
        return _lookup(args)
    if name == "relations":
        return _relations(args)
    raise ToolError(f"Unknown tool {name!r}")


def _resources() -> list[dict]:
    out = [{"uri": f"wengua://hexagram/{h['number']}", "name": f"hexagram-{h['number']}",
            "title": f"{h['unicode']} {h['number']} {h['name']['zh_hant']} / {h['name']['zh_hans']} {h['name']['pinyin']} · {h['name']['en']}",
            "mimeType": "application/json"} for h in bundle()["hexagrams"]]
    out += [{"uri": f"wengua://trigram/{t['key']}", "name": f"trigram-{t['key']}",
             "title": f"{t['symbol']} {t['name']['zh_hant']} {t['name']['pinyin']} · {t['name']['en']}",
             "mimeType": "application/json"} for t in trigrams()]
    out += [{k: r[k] for k in ("uri", "name", "title", "description", "mimeType")} for r in spec().get("ui_resources", [])]
    return out


def _read_resource(uri: str) -> dict:
    prefix_h, prefix_t = "wengua://hexagram/", "wengua://trigram/"
    ui = next((r for r in spec().get("ui_resources", []) if r["uri"] == uri), None)
    if ui:
        return {"contents": [{"uri": uri, "mimeType": ui["mimeType"], "text": ui["text"]}]}
    if uri.startswith(prefix_h):
        body = hexagram(int(uri[len(prefix_h):]))
    elif uri.startswith(prefix_t):
        key = uri[len(prefix_t):]
        body = next((t for t in trigrams() if t["key"] == key), None)
        if body is None:
            raise KeyError(uri)
    else:
        raise KeyError(uri)
    return {"contents": [{"uri": uri, "mimeType": "application/json", "text": json.dumps(body, ensure_ascii=False)}]}


def _prompt(name: str, args: dict) -> dict:
    p = next((p for p in spec()["prompts"] if p["name"] == name), None)
    if p is None:
        raise KeyError(name)
    q = (args or {}).get("question")
    text = p["template"].replace("{question_part}", f" My question: {q}" if q else "")
    return {"description": p["description"], "messages": [{"role": "user", "content": {"type": "text", "text": text}}]}


def handle(msg: dict) -> dict | None:
    """Handle one JSON-RPC message; return the response, or None for notifications."""
    method, mid, params = msg.get("method"), msg.get("id"), msg.get("params") or {}
    if mid is None:
        return None

    def ok(result):
        return {"jsonrpc": "2.0", "id": mid, "result": result}

    def err(code, message):
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": code, "message": message}}

    s = spec()
    if method == "initialize":
        requested = params.get("protocolVersion")
        return ok({
            "protocolVersion": requested if requested in PROTOCOL_VERSIONS else PROTOCOL_VERSIONS[0],
            "capabilities": {"tools": {}, "resources": {}, "prompts": {}},
            "serverInfo": {"name": s["name"], "title": s["title"], "version": __version__},
            "instructions": s["instructions"],
        })
    if method == "ping":
        return ok({})
    if method == "tools/list":
        return ok({"tools": s["tools"]})
    if method == "tools/call":
        try:
            result = call_tool(params.get("name"), params.get("arguments") or {})
        except (ToolError, ValueError, TypeError, KeyError) as e:
            return ok({"content": [{"type": "text", "text": str(e)}], "isError": True})
        return ok({"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}],
                   "structuredContent": result})
    if method == "resources/list":
        return ok({"resources": _resources()})
    if method == "resources/templates/list":
        return ok({"resourceTemplates": [
            {"uriTemplate": "wengua://hexagram/{number}", "name": "hexagram", "mimeType": "application/json",
             "description": "A hexagram by King Wen number, 1-64, with all texts"},
            {"uriTemplate": "wengua://trigram/{key}", "name": "trigram", "mimeType": "application/json",
             "description": "A trigram: qian, dui, li, zhen, xun, kan, gen, kun"}]})
    if method == "resources/read":
        try:
            return ok(_read_resource(params.get("uri", "")))
        except (KeyError, ValueError):
            return err(-32002, f"Resource not found: {params.get('uri')}")
    if method == "prompts/list":
        return ok({"prompts": [{k: v for k, v in p.items() if k != "template"} for p in s["prompts"]]})
    if method == "prompts/get":
        try:
            return ok(_prompt(params.get("name"), params.get("arguments")))
        except KeyError:
            return err(-32602, f"Unknown prompt: {params.get('name')}")
    return err(-32601, f"Method not found: {method}")


def serve(stdin=None, stdout=None) -> None:
    stdin = stdin or sys.stdin
    stdout = stdout or sys.stdout
    for line in stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            out = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
        else:
            if isinstance(msg, list):
                out = [r for r in (handle(m) for m in msg) if r is not None] or None
            else:
                out = handle(msg)
        if out is not None:
            stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
            stdout.flush()

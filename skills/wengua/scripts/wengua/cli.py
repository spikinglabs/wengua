"""wengua command line: cast, read a physical cast, look up, or run the MCP server."""

from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .lookup import find
from .reading import METHODS, cast, read_cast
from .selection import RULES

YANG, YIN = "━━━━━━━━━", "━━━   ━━━"


def draw(values: list[int]) -> list[str]:
    rows = []
    for i in range(5, -1, -1):
        v = values[i]
        mark = {9: " ○ 9", 6: " ✕ 6"}.get(v, f"   {v}")
        rows.append(f"  {YANG if v in (7, 9) else YIN}{mark}")
    return rows


def both(t: dict) -> str:
    """Traditional and simplified, shown once when they are the same."""
    return t["zh_hant"] if t["zh_hant"] == t["zh_hans"] else f"{t['zh_hant']} / {t['zh_hans']}"


def title(h: dict) -> str:
    n = h["name"]
    return f"{h['unicode']} {h['number']} {both(n)} {n['pinyin']} · {n['en']}"


def render(r: dict) -> str:
    out = []
    if r["question"]:
        out.append(f"Question: {r['question']}")
    out.append(title(r["primary"]) + (f"  →  {title(r['relating'])}" if r["relating"] else ""))
    out += draw(r["values"])
    sel = r["selection"]
    out += ["", sel["explanation"]["zh_hant"], sel["explanation"]["zh_hans"], sel["explanation"]["en"]]
    for t in sel["texts"]:
        label = both(t["label"]) if t["label"] else "卦辭 / 卦辞"
        out.append(f"  [{t['hexagram']} {label}] ({t['role']})")
        out.append(f"    {t['text']['zh_hant']}")
        if t["text"]["zh_hans"] != t["text"]["zh_hant"]:
            out.append(f"    {t['text']['zh_hans']}")
        if t["text"].get("en_legge"):
            out.append(f"    {t['text']['en_legge']} (Legge)")
    a = r["audit"]
    out.append("")
    out.append(f"互 {both(r['nuclear']['name'])} · 錯/错 {both(r['opposite']['name'])} · 綜/综 {both(r['inverse']['name'])}")
    out.append(f"{r['method']} · rng {a['rng']}{' (TEST, not a real reading)' if a['test'] else ''} · {a['library']} · {a['dataset']}")
    return "\n".join(out)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="wengua", description="Wengua 问卦: consult the I Ching. Code casts, the model reads.")
    p.add_argument("--version", action="version", version=f"wengua {__version__}")
    sub = p.add_subparsers(dest="cmd")

    def common(sp):
        sp.add_argument("-q", "--question")
        sp.add_argument("--rule", choices=RULES, default="zhuxi")
        sp.add_argument("--json", action="store_true", help="print the full Reading as JSON")

    c = sub.add_parser("cast", help="cast a hexagram")
    common(c)
    c.add_argument("-m", "--method", choices=METHODS, default="coins")
    c.add_argument("--seed", type=int, help="replay with a seed (test mode, not a real reading)")

    rd = sub.add_parser("read", help="read a physical cast: six values bottom to top, e.g. 7 8 9 7 6 8")
    common(rd)
    rd.add_argument("values", nargs=6)

    lk = sub.add_parser("lookup", help="look up a hexagram by number, name, pinyin, symbol, bits or trigrams")
    lk.add_argument("query", nargs="+")
    lk.add_argument("--json", action="store_true")

    sub.add_parser("mcp", help="run the MCP server over stdio")

    a = p.parse_args(argv)
    try:
        if a.cmd in (None, "mcp"):  # bare `wengua` (as `uvx wengua` in an MCP client) runs the server
            from .mcp import serve
            serve()
            return 0
        if a.cmd == "lookup":
            found = find(" ".join(a.query))
            if not found:
                print("No hexagram matches.", file=sys.stderr)
                return 1
            if a.json:
                print(json.dumps(found if len(found) > 1 else found[0], ensure_ascii=False, indent=2))
            else:
                for h in found:
                    print(title(h))
                    print(f"  {h['judgment']['zh_hant']}")
                    if h["judgment"]["zh_hans"] != h["judgment"]["zh_hant"]:
                        print(f"  {h['judgment']['zh_hans']}")
                    print(f"  {h['judgment']['en_legge']} (Legge)")
            return 0
        if a.cmd == "cast":
            r = cast(a.question, a.method, rule=a.rule, seed=a.seed, mode="test" if a.seed is not None else None)
        else:
            r = read_cast(a.values, a.question, rule=a.rule)
    except ValueError as e:
        print(f"wengua: {e}", file=sys.stderr)
        return 2
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else render(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())

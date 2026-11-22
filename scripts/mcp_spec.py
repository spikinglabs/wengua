"""Write spec/mcp.json: the MCP tool definitions, server instructions and prompt
shared by the Python and TypeScript servers (and the hosted Worker)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INSTRUCTIONS = """Wengua 问卦 casts and looks up I Ching (易经 / 周易) hexagrams. Code casts, the model reads.

When someone wants a reading:
1. Help them turn a vague worry into one clear, open question ("What should I understand about…", not yes/no).
2. Call `cast` (or `read_cast` if they cast coins or stalks themselves). Never invent, change or re-roll a result. If they want to ask the same question again right away, gently mention the tradition of not asking twice (不再三).
3. Show the hexagram: symbol, number, Chinese name and English name, the changing lines, and the relating hexagram (之卦) if there is one.
4. Quote the texts in `selection.texts` in Chinese (traditional or simplified, matching the user) with your own translation, and say which rule chose them (`selection.explanation`). Never quote a line or judgment that the tool did not return.
5. Interpret by connecting the text and its imagery to their situation. Keep the classical text clearly apart from your interpretation.
6. End with one or two reflective questions, not a verdict.

Boundaries: a reading is a prompt for reflection, not a prediction. Don't give medical, legal or financial verdicts, don't make claims about third parties, and if someone seems in distress, point them to real help. Readings made with a seed are marked `audit.test: true`: say clearly that they are tests."""

LOCALE = {"type": "string", "description": "The user's language, e.g. \"en\", \"zh-Hans\", \"zh-Hant\". Echoed back so you answer in it."}
RULE = {"type": "string", "enum": ["zhuxi", "all"], "default": "zhuxi",
        "description": "Which texts to select: \"zhuxi\" (Zhu Xi's rules, the classical default) or \"all\" (every relevant text)."}
QUESTION = {"type": "string", "description": "The question the user is asking. Optional but encouraged; it is not stored."}

TOOLS = [
    {
        "name": "cast",
        "title": "Cast a hexagram",
        "description": "Cast an I Ching hexagram with a secure random number generator and return the full reading: "
                       "primary hexagram, changing lines, relating (之), nuclear (互), opposite (錯) and inverse (綜) "
                       "hexagrams, and the classical texts to read, chosen by Zhu Xi's rules. Use this whenever the "
                       "user wants a reading. Never make up a hexagram yourself.",
        "inputSchema": {"type": "object", "properties": {
            "question": QUESTION,
            "method": {"type": "string", "enum": ["coins", "yarrow"], "default": "coins",
                       "description": "\"coins\" (three coins, 1/8 3/8 3/8 1/8) or \"yarrow\" (the stalk method, 1/16 5/16 7/16 3/16)."},
            "rule": RULE, "locale": LOCALE}, "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False, "idempotentHint": False},
    },
    {
        "name": "read_cast",
        "title": "Read a physical cast",
        "description": "Turn a cast the user made themselves (coins or yarrow stalks) into a full reading. Give the "
                       "six lines from the bottom up, each as a line value (6, 7, 8 or 9) or as three coin faces "
                       "(\"h\" for heads = 3, \"t\" for tails = 2).",
        "inputSchema": {"type": "object", "properties": {
            "lines": {"type": "array", "minItems": 6, "maxItems": 6,
                      "description": "Six lines, bottom to top.",
                      "items": {"anyOf": [
                          {"type": "integer", "enum": [6, 7, 8, 9]},
                          {"type": "array", "minItems": 3, "maxItems": 3,
                           "items": {"anyOf": [{"type": "string", "enum": ["h", "t", "heads", "tails"]},
                                               {"type": "integer", "enum": [2, 3]}]}}]}},
            "question": QUESTION, "rule": RULE, "locale": LOCALE},
            "required": ["lines"], "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False, "idempotentHint": True},
    },
    {
        "name": "lookup",
        "title": "Look up a hexagram",
        "description": "Get a hexagram's full text: judgment (卦辭), Tuan (彖), Image (象), all six lines with their "
                       "small images, and 用九/用六 and 文言 for 乾 and 坤, in traditional and simplified Chinese with "
                       "sources. Accepts a number (1-64), a Chinese name (乾, 讼, 水雷屯, 乾為天), pinyin with or "
                       "without tones, the English name, the symbol (䷂), six bits bottom to top, or a trigram pair "
                       "(坎上震下, \"water over thunder\").",
        "inputSchema": {"type": "object", "properties": {
            "query": {"type": ["string", "integer"], "description": "Any identifier of the hexagram."}},
            "required": ["query"], "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False, "idempotentHint": True},
    },
    {
        "name": "relations",
        "title": "Related hexagrams",
        "description": "For a hexagram and optional changing lines, return the relating (之), nuclear (互), opposite "
                       "(錯) and inverse (綜) hexagrams with their judgments.",
        "inputSchema": {"type": "object", "properties": {
            "hexagram": {"type": ["string", "integer"], "description": "Any identifier of the hexagram."},
            "changing_lines": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": 6},
                               "description": "Positions of changing lines, 1 = bottom."}},
            "required": ["hexagram"], "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False, "idempotentHint": True},
    },
]

PROMPTS = [{
    "name": "reading",
    "title": "I Ching reading",
    "description": "A guided I Ching reading: clarify the question, cast, and reflect on the texts.",
    "arguments": [{"name": "question", "description": "What the user wants to reflect on", "required": False}],
    "template": "I'd like an I Ching reading.{question_part}\n\nPlease follow this flow:\n" + INSTRUCTIONS.split("\n\n", 1)[1],
}]

CARD_URI = "ui://wengua/reading"
for t in TOOLS:
    if t["name"] in ("cast", "read_cast"):
        t["_meta"] = {"ui": {"resourceUri": CARD_URI}}
UI_RESOURCES = [{
    "uri": CARD_URI, "name": "reading-card", "title": "Wengua reading card",
    "description": "Draws the cast: primary and relating hexagrams, changing lines and the selected texts, with a 繁/简 toggle.",
    "mimeType": "text/html;profile=mcp-app",
    "text": (ROOT / "spec" / "reading-card.html").read_text(encoding="utf-8"),
}]

ICONS = [
    {"src": "https://wengua.allo.land/assets/icon-512.png", "mimeType": "image/png", "sizes": ["512x512"]},
    {"src": "https://wengua.allo.land/assets/icon.svg", "mimeType": "image/svg+xml", "sizes": ["any"]},
]
out = {"name": "wengua", "title": "Wengua 问卦", "websiteUrl": "https://wengua.allo.land/", "icons": ICONS, "instructions": INSTRUCTIONS, "tools": TOOLS, "prompts": PROMPTS, "ui_resources": UI_RESOURCES}
(ROOT / "spec" / "mcp.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("Wrote spec/mcp.json")

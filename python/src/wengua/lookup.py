"""Find hexagrams from whatever identifier a person or model has at hand."""

from __future__ import annotations

import re
import unicodedata

from .data import bundle, hexagram, hexagram_by_binary, trigrams

# Nature images of the trigrams, as used in full names such as 水雷屯 and 乾為天.
IMAGES = {"天": "qian", "地": "kun", "雷": "zhen", "風": "xun", "风": "xun", "水": "kan",
          "火": "li", "山": "gen", "澤": "dui", "泽": "dui"}
# Common alternative characters for hexagram names.
ALIASES = {"恆": 32, "遁": 33, "豐": 55, "旣濟": 63}


def normalize_latin(s: str) -> str:
    """Lower case, no tone marks, no spaces or punctuation; ü becomes v."""
    s = unicodedata.normalize("NFD", s.strip().lower()).replace("u\u0308", "v").replace("u:", "v")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[\s\-'’_.]", "", s)


def _trigram_key(token: str) -> str | None:
    if token in IMAGES:
        return IMAGES[token]
    t = normalize_latin(token)
    for tri in trigrams():
        n = tri["name"]
        if token in (n["zh_hant"], n["zh_hans"], tri["symbol"]) or t in (tri["key"], normalize_latin(n["en"])):
            return tri["key"]
    return None


def _from_trigrams(upper: str, lower: str) -> dict | None:
    u, lo = _trigram_key(upper), _trigram_key(lower)
    if not (u and lo):
        return None
    from .data import trigram
    return hexagram_by_binary(trigram(lo)["binary"] + trigram(u)["binary"])


def find(query) -> list[dict]:
    """All hexagrams matching `query`, best first. An empty list means no match.

    Accepts a number (1-64), a Chinese name in traditional or simplified script
    (乾, 小畜, 訟/讼), a full name (水雷屯, 乾為天), pinyin with or without tones
    (xiǎo chù, xiaochu), the English name, the Unicode symbol (䷂), six bits
    bottom to top (100010), or a trigram pair (坎上震下, 上坎下震, water over thunder).
    """
    if isinstance(query, int) and not isinstance(query, bool):
        return [hexagram(query)] if 1 <= query <= 64 else []
    q = str(query).strip()
    if not q:
        return []
    if re.fullmatch(r"[01]{6}", q):
        return [hexagram_by_binary(q)]
    if q.isdigit():
        n = int(q)
        return [hexagram(n)] if 1 <= n <= 64 else []
    if len(q) == 1 and 0x4DC0 <= ord(q) <= 0x4DFF:
        return [hexagram(ord(q) - 0x4DC0 + 1)]
    if q in ALIASES:
        return [hexagram(ALIASES[q])]

    hexes = bundle()["hexagrams"]
    for h in hexes:
        if q in (h["name"]["zh_hant"], h["name"]["zh_hans"]):
            return [h]

    # Trigram pairs: 坎上震下 / 上坎下震
    m = re.fullmatch(r"(.)上(.)下", q) or re.fullmatch(r"上(.)下(.)", q)
    if m and (h := _from_trigrams(m.group(1), m.group(2))):
        return [h]
    # Full names: 水雷屯 (upper image, lower image, name), 乾為天 (doubled trigram)
    m = re.fullmatch(r"(.)[為为](.)", q)
    if m and _trigram_key(m.group(1)) and _trigram_key(m.group(1)) == IMAGES.get(m.group(2)):
        return [_from_trigrams(m.group(1), m.group(1))]
    if len(q) >= 3 and q[0] in IMAGES and q[1] in IMAGES:
        h = _from_trigrams(q[0], q[1])
        rest = q[2:]
        if h and (rest in (h["name"]["zh_hant"], h["name"]["zh_hans"]) or ALIASES.get(rest) == h["number"]):
            return [h]
    # English trigram pairs: "water over thunder"
    m = re.fullmatch(r"\s*(\w+)\s+over\s+(\w+)\s*", q, flags=re.I)
    if m and (h := _from_trigrams(m.group(1), m.group(2))):
        return [h]

    latin = normalize_latin(q)
    if not latin:
        return []
    toned = unicodedata.normalize("NFC", q.lower().replace(" ", ""))
    exact_tone = [h for h in hexes if h["name"]["pinyin"].replace(" ", "") == toned]
    if exact_tone:
        return exact_tone
    plain = [h for h in hexes if normalize_latin(h["name"]["pinyin"]) == latin]
    if plain:
        return plain
    loose = [h for h in hexes if normalize_latin(h["name"]["pinyin"]).replace("v", "u") == latin.replace("v", "u")]
    if loose:
        return loose
    en = [h for h in hexes if normalize_latin(h["name"]["en"]) == latin
          or normalize_latin(re.sub(r"^the\s+", "", h["name"]["en"], flags=re.I)) == latin]
    return en


def get(query) -> dict:
    """Exactly one hexagram, or ValueError if there is none or more than one."""
    found = find(query)
    if not found:
        raise ValueError(f"no hexagram matches {query!r}")
    if len(found) > 1:
        names = ", ".join(f"{h['number']} {h['name']['zh_hant']} {h['name']['pinyin']}" for h in found)
        raise ValueError(f"{query!r} is ambiguous: {names}")
    return found[0]

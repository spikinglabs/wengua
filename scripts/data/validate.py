"""Validate the Wengua dataset. Exits non-zero on any problem.

Usage: python scripts/data/validate.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "data"
LABELS_YANG = ["初九", "九二", "九三", "九四", "九五", "上九"]
LABELS_YIN = ["初六", "六二", "六三", "六四", "六五", "上六"]
TEXT_KEYS = ("zh_hant", "zh_hans")

errors: list[str] = []


def err(where: str, msg: str) -> None:
    errors.append(f"{where}: {msg}")


def check_text(where: str, value, required=True) -> None:
    if value is None:
        if required:
            err(where, "missing")
        return
    for k in TEXT_KEYS:
        if not isinstance(value.get(k), str) or not value[k].strip():
            err(where, f"empty {k}")
    for k in TEXT_KEYS:
        if any(c in (value.get(k) or "") for c in "（）()[]〔〕【】"):
            err(where, f"editorial brackets left in {k}")
    if value.get("zh_hans") and "干" in value["zh_hans"] and "乾" in value.get("zh_hant", ""):
        err(where, "乾 was converted to 干 in simplified text")


def check_en(where: str, value) -> None:
    """Legge's English: present, plain ASCII prose (Legge's em dash allowed), no OCR leftovers."""
    en = value.get("en_legge")
    if not isinstance(en, str) or len(en) < 10:
        err(where, "missing en_legge")
        return
    if any(ord(c) > 127 and c != "\u2014" for c in en):
        err(where, "non-ASCII character in en_legge")
    if any(s in en for s in ("  ", " ,", " .", " ;")):
        err(where, "spacing problem in en_legge")


def main() -> int:
    trigrams = json.loads((DATA / "trigrams.json").read_text())
    by_key = {t["key"]: t for t in trigrams}
    if len(trigrams) != 8 or len({t["binary"] for t in trigrams}) != 8:
        err("trigrams.json", "expected 8 distinct trigrams")

    seen_binary = set()
    files = sorted((DATA / "hexagrams").glob("*.json"))
    if len(files) != 64:
        err("hexagrams", f"expected 64 files, found {len(files)}")
    for f in files:
        h = json.loads(f.read_text())
        n = h["number"]
        w = f"hexagram {n}"
        if f.stem != f"{n:02d}":
            err(w, f"file name {f.name} does not match number")
        if h["unicode"] != chr(0x4DC0 + n - 1):
            err(w, "unicode symbol does not match King Wen number")
        b = h["binary"]
        if len(b) != 6 or set(b) - {"0", "1"}:
            err(w, f"bad binary {b}")
        if b in seen_binary:
            err(w, f"duplicate binary {b}")
        seen_binary.add(b)
        lower, upper = by_key[h["trigrams"]["lower"]], by_key[h["trigrams"]["upper"]]
        if lower["binary"] + upper["binary"] != b:
            err(w, "binary does not match its trigrams")
        for k in ("judgment", "tuan", "image"):
            check_text(f"{w} {k}", h.get(k))
        for k in ("judgment", "tuan", "image"):
            check_en(f"{w} {k}", h[k])
        check_text(f"{w} name", h["name"])
        if not h["name"].get("pinyin") or not h["name"].get("en"):
            err(w, "name needs pinyin and en")
        if len(h["lines"]) != 6:
            err(w, f"expected 6 lines, found {len(h['lines'])}")
        for i, line in enumerate(h["lines"]):
            lw = f"{w} line {i + 1}"
            if line["position"] != i + 1:
                err(lw, "position out of order")
            expected = LABELS_YANG[i] if b[i] == "1" else LABELS_YIN[i]
            if line["label"]["zh_hant"] != expected:
                err(lw, f"label {line['label']['zh_hant']} does not match bit {b[i]} (expected {expected})")
            check_text(f"{lw} text", line["text"])
            check_text(f"{lw} xiao_xiang", line["xiao_xiang"])
            check_en(f"{lw} text", line["text"])
            check_en(f"{lw} xiao_xiang", line["xiao_xiang"])
        if n in (1, 2):
            use = h.get("use_line")
            want = "用九" if n == 1 else "用六"
            if not use or use["label"]["zh_hant"] != want:
                err(w, f"missing {want}")
            else:
                check_text(f"{w} {want}", use["text"])
                check_en(f"{w} {want}", use["text"])
                check_en(f"{w} {want} xiao_xiang", use["xiao_xiang"])
                check_text(f"{w} {want} xiao_xiang", use["xiao_xiang"])
            if not h.get("wenyan"):
                err(w, "missing 文言")
            for i, para in enumerate(h.get("wenyan") or []):
                check_en(f"{w} 文言 {i + 1}", para)
        elif "use_line" in h or "wenyan" in h:
            err(w, "only 乾 and 坤 have 用九/用六 and 文言")
        src = h.get("source", {})
        if not src.get("text", {}).get("url") or not src.get("cross_check", {}).get("url"):
            err(w, "missing source urls")
    if len(seen_binary) != 64:
        err("hexagrams", "the 64 binaries are not all distinct")

    if errors:
        print("\n".join(errors))
        print(f"\n{len(errors)} problem(s) found")
        return 1
    print("Dataset OK: 64 hexagrams, 384 lines plus 用九 and 用六, 8 trigrams")
    return 0


if __name__ == "__main__":
    sys.exit(main())

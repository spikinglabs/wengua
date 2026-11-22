"""Build the Wengua dataset from the cached source snapshots.

Primary source: Kanseki Repository KR1a0001 周易 (base edition: TLS), the
one page per hexagram, snapshotted in data/sources/wikisource/NN.wikitext.
Cross-check source: Kanseki Repository KR1a0001 (base edition: TLS), in
data/sources/kanripo/NN.txt. Every 卦辞 and 爻辞 is compared character by
character (punctuation ignored); differences are written to
data/cross-check.json for human review.

Usage: python scripts/data/build.py
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import opencc

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
DATASET_VERSION = "0.3.0"  # SemVer: bump on any text change
SRC = DATA / "sources"

# King Wen order. pinyin and Wengua's own short English glosses (CC BY 4.0).
HEXAGRAMS = [
    ("乾", "qián", "Heaven"), ("坤", "kūn", "Earth"), ("屯", "zhūn", "Sprouting"),
    ("蒙", "méng", "Youthful Ignorance"), ("需", "xū", "Waiting"), ("訟", "sòng", "Dispute"),
    ("師", "shī", "The Army"), ("比", "bǐ", "Union"), ("小畜", "xiǎo chù", "Small Restraint"),
    ("履", "lǚ", "Treading"), ("泰", "tài", "Peace"), ("否", "pǐ", "Standstill"),
    ("同人", "tóng rén", "Fellowship"), ("大有", "dà yǒu", "Great Possession"),
    ("謙", "qiān", "Modesty"), ("豫", "yù", "Enthusiasm"), ("隨", "suí", "Following"),
    ("蠱", "gǔ", "Remedying Decay"), ("臨", "lín", "Approach"), ("觀", "guān", "Contemplation"),
    ("噬嗑", "shì kè", "Biting Through"), ("賁", "bì", "Adornment"), ("剝", "bō", "Stripping Away"),
    ("復", "fù", "Return"), ("无妄", "wú wàng", "Innocence"), ("大畜", "dà chù", "Great Restraint"),
    ("頤", "yí", "Nourishment"), ("大過", "dà guò", "Great Excess"), ("坎", "kǎn", "The Abyss"),
    ("離", "lí", "Radiance"), ("咸", "xián", "Influence"), ("恒", "héng", "Duration"),
    ("遯", "dùn", "Retreat"), ("大壯", "dà zhuàng", "Great Strength"), ("晉", "jìn", "Advance"),
    ("明夷", "míng yí", "Darkening of the Light"), ("家人", "jiā rén", "The Family"),
    ("睽", "kuí", "Opposition"), ("蹇", "jiǎn", "Obstruction"), ("解", "xiè", "Release"),
    ("損", "sǔn", "Decrease"), ("益", "yì", "Increase"), ("夬", "guài", "Breakthrough"),
    ("姤", "gòu", "Encounter"), ("萃", "cuì", "Gathering"), ("升", "shēng", "Ascending"),
    ("困", "kùn", "Exhaustion"), ("井", "jǐng", "The Well"), ("革", "gé", "Revolution"),
    ("鼎", "dǐng", "The Cauldron"), ("震", "zhèn", "Thunder"), ("艮", "gèn", "Stillness"),
    ("漸", "jiàn", "Gradual Progress"), ("歸妹", "guī mèi", "The Marrying Maiden"),
    ("豐", "fēng", "Abundance"), ("旅", "lǚ", "The Wanderer"), ("巽", "xùn", "Wind"),
    ("兌", "duì", "Joy"), ("渙", "huàn", "Dispersion"), ("節", "jié", "Limitation"),
    ("中孚", "zhōng fú", "Inner Truth"), ("小過", "xiǎo guò", "Small Excess"),
    ("既濟", "jì jì", "After Completion"), ("未濟", "wèi jì", "Before Completion"),
]

# Lines are listed bottom to top; "1" is a solid (yang) line.
TRIGRAMS = [
    ("qian", "乾", "qián", "☰", "111", "Heaven"),
    ("dui", "兌", "duì", "☱", "110", "Lake"),
    ("li", "離", "lí", "☲", "101", "Fire"),
    ("zhen", "震", "zhèn", "☳", "100", "Thunder"),
    ("xun", "巽", "xùn", "☴", "011", "Wind"),
    ("kan", "坎", "kǎn", "☵", "010", "Water"),
    ("gen", "艮", "gèn", "☶", "001", "Mountain"),
    ("kun", "坤", "kūn", "☷", "000", "Earth"),
]
TRIGRAM_BY_ZH = {t[1]: t for t in TRIGRAMS}

# OpenCC maps 乾 to 干 ("dry"); in the Yijing it is always qián.
PROTECT = ["乾"]
_t2s = opencc.OpenCC("t2s")


def to_hans(text: str) -> str:
    marks = {ch: f"{i}" for i, ch in enumerate(PROTECT)}
    for ch, m in marks.items():
        text = text.replace(ch, m)
    text = _t2s.convert(text)
    for ch, m in marks.items():
        text = text.replace(m, ch)
    return text


def bilingual(hant: str) -> dict:
    return {"zh_hant": hant, "zh_hans": to_hans(hant)}


def clean(raw: str, notes: list) -> str:
    """Strip wiki markup, recording variants and editorial notes."""
    s = re.sub(r"-\{(?:[^|{}]*\|)?([^{}]*)\}-", r"\1", raw)

    def variant(m):
        notes.append({"type": "variant", "reading": m.group(1), "alternative": m.group(2)})
        return m.group(1)

    s = re.sub(r"\{\{另\|([^|}]*)\|([^}]*)\}\}", variant, s)

    def note(m):
        notes.append({"type": "note", "text": m.group(1)})
        return ""

    s = re.sub(r"\{\{\*\|([^}]*)\}\}", note, s)
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("'''", "")
    if "{{" in s or "}}" in s:
        raise ValueError(f"unhandled template in: {raw}")
    return s.strip()


LINE_RE = re.compile(r"^(初[九六]|[九六][二三四五]|上[九六]|用[九六])[：:，,、](.*)$")


def parse_wikisource(n: int) -> dict:
    text = (SRC / "wikisource" / f"{n:02d}.wikitext").read_text()
    revid = int(re.match(r"%%REVID (\d+)", text).group(1))
    rows = text.splitlines()
    section = None
    out = {"judgment": None, "lines": [], "tuan": [], "image": None, "xiao": [], "wenyan": [], "trigrams": None}
    notes: list = []
    for row in rows:
        m = re.search(r"^\[\[(?:File|Image):.*?\]\]\s*(\S+?)下(\S+?)上\s*$", row)
        if m and out["trigrams"] is None:
            out["trigrams"] = (clean(m.group(1), []), clean(m.group(2), []))
            continue
        head = re.match(r"^\*'''(彖曰|象曰|文言曰)：'''", row)
        if head:
            section = head.group(1)
            continue
        if "'''易經：'''" in row:
            section = "經"
            continue
        m = re.match(r"^([*#:;]+)(.*)$", row)
        if not m or section is None:
            continue
        marker, body = m.groups()
        local: list = []
        body = clean(body, local)
        if not body:
            continue
        if section == "經":
            if marker == "**":
                name, colon, judgment = body.partition("：")
                out["judgment"] = judgment.strip() if colon else body
                notes += [dict(x, field="judgment") for x in local]
            elif marker == "*#":
                lm = LINE_RE.match(body)
                if not lm:
                    raise ValueError(f"#{n}: bad line row {body}")
                out["lines"].append((lm.group(1), lm.group(2).strip()))
                notes += [dict(x, field=f"lines.{len(out['lines'])}.text") for x in local]
            elif marker == "***" and out["judgment"] is not None and not out["lines"]:
                out["judgment"] += body  # judgment continued on a second row
                notes += [dict(x, field="judgment") for x in local]
            else:
                raise ValueError(f"#{n}: unexpected row in 經: {row}")
        elif section == "彖曰":
            out["tuan"].append(body)
            notes += [dict(x, field="tuan") for x in local]
        elif section == "象曰":
            if marker == "**":
                out["image"] = body
                notes += [dict(x, field="image") for x in local]
            elif marker == "*#":
                out["xiao"].append(body)
                notes += [dict(x, field=f"lines.{len(out['xiao'])}.xiao_xiang") for x in local]
        elif section == "文言曰":
            out["wenyan"].append(body)
            notes += [dict(x, field="wenyan") for x in local]
    out["revid"] = revid
    out["notes"] = notes
    return out



NAME_IN_TEXT = {10, 12, 13, 52}  # 履虎尾, 否之匪人, 同人于野, 艮其背: the name opens the judgment


def bare(s: str) -> str:
    """Characters only, for comparing editions regardless of punctuation."""
    return "".join(ch for ch in s if unicodedata.category(ch).startswith("L"))


def diff(a: str, b: str) -> list:
    import difflib

    ops = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag != "equal":
            ops.append({"primary": a[i1:i2], "wikisource": b[j1:j2]})
    return ops


def load_emendations() -> dict:
    out = {}
    for line in (SRC / "emendations.tsv").read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        n, field, old, new, note = line.split("\t")
        out.setdefault(int(n), []).append((field, old, new, note))
    return out


def main() -> None:
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    import kanripo

    (DATA / "hexagrams").mkdir(parents=True, exist_ok=True)
    trigrams = [
        {"key": k, "name": {**bilingual(zh), "pinyin": py, "en": en}, "symbol": sym, "binary": b}
        for k, zh, py, sym, b, en in TRIGRAMS
    ]
    (DATA / "trigrams.json").write_text(json.dumps(trigrams, ensure_ascii=False, indent=2) + "\n")

    report = []
    emendations = load_emendations()
    legge = json.loads((SRC / "legge" / "text.json").read_text(encoding="utf-8"))
    for n, (name, pinyin, en) in enumerate(HEXAGRAMS, start=1):
        kr = kanripo.parse((SRC / "kanripo" / f"{n:02d}.txt").read_text())
        ws = parse_wikisource(n)
        if n == 1:
            kr["image"], qian_xiao = kanripo.split_qian_image(kr["image"])
            kr["xiao"], kr["use_xiao"] = qian_xiao[:6], qian_xiao[6]
        judgment = kr["judgment"]
        if n in NAME_IN_TEXT and not judgment.startswith(name):
            judgment = name + judgment
        if n == 29:  # the received text opens 坎 with 習坎
            judgment = "習坎，" + kr["judgment"]
        lower, upper = (TRIGRAM_BY_ZH[t] for t in kr["trigrams"])
        names = {h[0] for h in HEXAGRAMS} | {"習坎"}

        def unmark(t):
            """TLS wraps hexagram names in 《》; plain text reads better."""
            return re.sub(r"《([^》]+)》", lambda m: m.group(1) if m.group(1) in names else m.group(0), t) if t else t

        for key in ("judgment", "tuan", "image", "use_xiao"):
            kr[key] = unmark(kr[key])
        kr["xiao"] = [unmark(x) for x in kr["xiao"]]
        kr["wenyan"] = [re.sub(r"《([元亨利貞])》", r"「\1」", unmark(x)) for x in kr["wenyan"]]

        # Restore the received text where both witnesses agree against the base (emendations.tsv).
        fields = {"judgment": judgment, "tuan": kr["tuan"], "image": kr["image"]}
        for i, (label, text) in enumerate(kr["lines"]):
            fields[f"lines.{i + 1}.text"] = text
            fields[f"lines.{i + 1}.xiao_xiang"] = kr["xiao"][i]
        applied = []
        for field, old, new, note in emendations.get(n, []):
            if fields[field].count(old) != 1:
                raise ValueError(f"emendation {n} {field}: {old!r} must occur exactly once")
            fields[field] = fields[field].replace(old, new)
            applied.append({"field": field, "base": old, "adopted": new, "note": note})
        judgment, kr["tuan"], kr["image"] = fields["judgment"], fields["tuan"], fields["image"]
        kr["lines"] = [(label, fields[f"lines.{i + 1}.text"]) for i, (label, _) in enumerate(kr["lines"])]
        kr["xiao"] = [fields[f"lines.{i + 1}.xiao_xiang"] for i in range(len(kr["xiao"]))]

        def sep(label, text):
            return re.sub(r"^[、：:，,]", "", text)

        lines = [
            {
                "position": i + 1,
                "label": bilingual(label),
                "text": bilingual(sep(label, text)),
                "xiao_xiang": bilingual(kr["xiao"][i]),
            }
            for i, (label, text) in enumerate(kr["lines"])
        ]
        record = {
            "number": n,
            "unicode": chr(0x4DC0 + n - 1),
            "binary": lower[4] + upper[4],
            "trigrams": {"lower": lower[0], "upper": upper[0]},
            "name": {**bilingual(name), "pinyin": pinyin, "en": en},
            "judgment": bilingual(judgment),
            "tuan": bilingual(kr["tuan"]),
            "image": bilingual(kr["image"]),
            "lines": lines,
        }
        if kr["use_line"]:
            label, text = kr["use_line"]
            record["use_line"] = {"label": bilingual(label), "text": bilingual(text),
                                  "xiao_xiang": bilingual(kr["use_xiao"])}
        # English: James Legge's translation (1882), see data/sources/legge/README.md.
        en = legge[f"{n:02d}"]
        record["judgment"]["en_legge"] = en["judgment"]
        for line, text in zip(record["lines"], en["lines"], strict=True):
            line["text"]["en_legge"] = text
        if "use_line" in record:
            record["use_line"]["text"]["en_legge"] = en["use_line"]
        if kr["wenyan"]:
            record["wenyan"] = [bilingual(p) for p in kr["wenyan"]]

        # Cross-check against Wikisource, field by field, ignoring punctuation.
        pairs = [("judgment", judgment, ws["judgment"] if n not in NAME_IN_TEXT else ws["judgment"]),
                 ("tuan", kr["tuan"], "".join(ws["tuan"])),
                 ("image", kr["image"], ws["image"] or "")]
        ws_lines = [t for lab, t in ws["lines"] if not lab.startswith("用")]
        ws_use = [t for lab, t in ws["lines"] if lab.startswith("用")]
        for i, line in enumerate(lines):
            pairs.append((f"lines.{i + 1}.text", line["text"]["zh_hant"], ws_lines[i] if i < len(ws_lines) else ""))
            pairs.append((f"lines.{i + 1}.xiao_xiang", line["xiao_xiang"]["zh_hant"], ws["xiao"][i] if i < len(ws["xiao"]) else ""))
        if kr["use_line"]:
            pairs.append(("use_line.text", record["use_line"]["text"]["zh_hant"], ws_use[0] if ws_use else ""))
        variants = []
        for field, a, b in pairs:
            a_bare, b_bare = bare(a), bare(b)
            if field == "judgment" and n not in NAME_IN_TEXT and b_bare.startswith(name) is False:
                pass
            d = diff(a_bare, b_bare)
            if d:
                variants.append({"field": field, "differences": d})
                report.append({"hexagram": n, "name": name, "field": field, "differences": d})
        record["variants"] = variants
        record["emendations"] = applied
        record["source"] = {
            "text": {
                "work": "周易",
                "edition": "Kanseki Repository KR1a0001 (base edition: TLS)",
                "url": f"https://github.com/kanripo/KR1a0001/blob/master/KR1a0001_{n:03d}.txt",
            },
            "collated_with": {
                "edition": "四部叢刊本 王弼《周易注》 (Song edition), Kanseki Repository KR1a0006, branch SBCK",
                "url": "https://github.com/kanripo/KR1a0006/tree/SBCK",
            },
            "cross_check": {
                "edition": "Chinese Wikisource, 周易/" + name,
                "url": f"https://zh.wikisource.org/w/index.php?oldid={ws['revid']}",
            },
        }
        (DATA / "hexagrams" / f"{n:02d}.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")

    bundle = {
        "dataset": "wengua-data",
        "version": DATASET_VERSION,
        "license": "CC-BY-SA-4.0",
        "trigrams": trigrams,
        "hexagrams": [json.loads((DATA / "hexagrams" / f"{i:02d}.json").read_text()) for i in range(1, 65)],
    }
    (DATA / "iching.json").write_text(json.dumps(bundle, ensure_ascii=False, separators=(",", ":")) + "\n")
    (DATA / "cross-check.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote 64 hexagrams and 8 trigrams; {len(report)} fields differ from Wikisource (see data/cross-check.json)")


if __name__ == "__main__":
    main()

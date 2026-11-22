"""Parse a Kanseki Repository (KR1a0001) 周易 file into its parts."""

from __future__ import annotations

import re

LABEL = r"(?:初[九六]|[九六][二三四五]|上[九六]|用[九六])"
BREAK = "\uE010"  # marks a page break in the source (private use, so not whitespace)
SECTION = re.compile(rf"《(彖|象|文言)》曰[：:、，]?|(?:(?<=^)|(?<=[。？！」』\uE010]))({LABEL})[、：:，]")


def flatten(raw: str) -> tuple[str, str, str]:
    """Return (lower trigram, upper trigram, body text with paragraph marks)."""
    lines = [l for l in raw.splitlines() if not l.startswith("#")]
    text = "\n".join(lines)
    text = re.sub(r"<pb:[^>]+>", BREAK, text).replace("¶", "")
    text = re.sub(r"\s+", "", text)
    m = re.search(r"\*\*《[^》]+》(?:（[^）]*）)?" + BREAK + r"*[䷀-䷿]?(\S)下(\S)上", text)
    lower, upper = m.group(1), m.group(2)
    body = text[m.end():]
    body = re.sub(f"{BREAK}+", BREAK, body).strip(BREAK)
    return lower, upper, body


def strip_quotes(s: str) -> str:
    """TLS marks quotations of the classic with 「」 inside the commentaries."""
    return s.replace("「", "").replace("」", "")


def tidy(s: str) -> str:
    return s.replace(BREAK, "").strip()


def parse(raw: str) -> dict:
    lower, upper, body = flatten(raw)
    out = {"trigrams": (lower, upper), "judgment": None, "tuan": None, "image": None,
           "lines": [], "xiao": [], "use_line": None, "use_xiao": None, "wenyan": []}

    wenyan_at = body.find("《文言》曰")
    if wenyan_at >= 0:
        wen = body[wenyan_at:]
        wen = re.sub(r"^《文言》曰[：:、，]?", "", wen)
        out["wenyan"] = [p for p in (x.strip() for x in wen.split(BREAK)) if p]
        body = body[:wenyan_at]

    tokens = list(SECTION.finditer(body))
    head = body[: tokens[0].start()] if tokens else body
    out["judgment"] = tidy(re.sub(r"^《[^》]+》", "", tidy(head)))

    pending_image = True
    for i, t in enumerate(tokens):
        end = tokens[i + 1].start() if i + 1 < len(tokens) else len(body)
        content = tidy(body[t.end():end])
        kind, label = t.group(1), t.group(2)
        if kind == "彖":
            out["tuan"] = strip_quotes(content)
        elif kind == "象":
            if pending_image:
                out["image"] = strip_quotes(content)
                pending_image = False
            elif out["use_line"] and out["use_xiao"] is None and len(out["xiao"]) == len(out["lines"]):
                out["use_xiao"] = strip_quotes(content)
            else:
                out["xiao"].append(strip_quotes(content))
        elif label:
            if label.startswith("用"):
                out["use_line"] = (label, content)
            else:
                out["lines"].append((label, content))
    return out


def split_qian_image(image: str) -> tuple[str, list[str]]:
    """In 乾 the 大象 and all 小象 form one block: split it into its parts."""
    sentences = [s + "。" for s in image.split("。") if s]
    return sentences[0], sentences[1:]

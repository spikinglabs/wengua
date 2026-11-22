"""Which texts to read (取辭).

The default rule follows Zhu Xi, 《易學啓蒙·考變占》. The `all` rule simply
returns every text that could matter and leaves the weighing to the reader.
"""

from __future__ import annotations

ZHUXI_SOURCE = {"zh_hant": "朱熹《易學啓蒙·考變占》", "zh_hans": "朱熹《易学启蒙·考变占》",
                "en": "Zhu Xi, Yixue Qimeng, 'Examining the changes'"}

ZHUXI_EXPLANATIONS = {
    0: ("No changing lines: read the judgment of the primary hexagram.",
        "六爻皆不變：占本卦卦辭。", "六爻皆不变：占本卦卦辞。"),
    1: ("One changing line: read that line of the primary hexagram.",
        "一爻變：以本卦變爻之辭占。", "一爻变：以本卦变爻之辞占。"),
    2: ("Two changing lines: read both lines of the primary hexagram; the upper one leads.",
        "二爻變：以本卦二變爻之辭占，以上爻為主。", "二爻变：以本卦二变爻之辞占，以上爻为主。"),
    3: ("Three changing lines: read the judgments of the primary hexagram (貞, the base) "
        "and the relating hexagram (悔, the outcome).",
        "三爻變：占本卦及之卦之卦辭，以本卦為貞，之卦為悔。",
        "三爻变：占本卦及之卦之卦辞，以本卦为贞，之卦为悔。"),
    4: ("Four changing lines: read the two unchanging lines of the relating hexagram; the lower one leads.",
        "四爻變：以之卦二不變爻之辭占，以下爻為主。", "四爻变：以之卦二不变爻之辞占，以下爻为主。"),
    5: ("Five changing lines: read the one unchanging line of the relating hexagram.",
        "五爻變：以之卦不變爻之辭占。", "五爻变：以之卦不变爻之辞占。"),
    6: ("All six lines change: read the judgment of the relating hexagram.",
        "六爻皆變：占之卦卦辭。", "六爻皆变：占之卦卦辞。"),
    "use": ("All six lines change in Qian or Kun: read 用九 or 用六.",
            "六爻皆變，乾坤占二用：以用九、用六之辭占。", "六爻皆变，乾坤占二用：以用九、用六之辞占。"),
}

ALL_EXPLANATION = ("Every relevant text: the primary judgment, each changing line, and the relating judgment.",
                   "列出所有相關文辭：本卦卦辭、各變爻爻辭、之卦卦辭。",
                   "列出所有相关文辞：本卦卦辞、各变爻爻辞、之卦卦辞。")

RULES = ("zhuxi", "all")


def _judgment(hexagram: dict, role: str) -> dict:
    return {"hexagram": hexagram["number"], "kind": "judgment", "position": None,
            "label": None, "text": hexagram["judgment"], "role": role}


def _line(hexagram: dict, position: int, role: str) -> dict:
    line = hexagram["lines"][position - 1]
    return {"hexagram": hexagram["number"], "kind": "line", "position": position,
            "label": line["label"], "text": line["text"], "role": role}


def _use(hexagram: dict, role: str) -> dict:
    use = hexagram["use_line"]
    return {"hexagram": hexagram["number"], "kind": "use", "position": None,
            "label": use["label"], "text": use["text"], "role": role}


def _explain(t: tuple) -> dict:
    return {"en": t[0], "zh_hant": t[1], "zh_hans": t[2]}


def select(primary: dict, relating: dict, changing: list[int], rule: str = "zhuxi") -> dict:
    """Return {rule, changing_count, explanation, source, texts}."""
    k = len(changing)
    if rule == "all":
        texts = [_judgment(primary, "context")]
        texts += [_line(primary, p, "changing") for p in changing]
        if k == 6 and primary.get("use_line"):
            texts.append(_use(primary, "changing"))
        if k:
            texts.append(_judgment(relating, "outcome"))
        return {"rule": "all", "changing_count": k, "explanation": _explain(ALL_EXPLANATION),
                "source": None, "texts": texts}
    if rule != "zhuxi":
        raise ValueError(f"unknown rule {rule!r}; choose one of {', '.join(RULES)}")

    key = k
    unchanged = [p for p in range(1, 7) if p not in changing]
    if k == 0:
        texts = [_judgment(primary, "principal")]
    elif k == 1:
        texts = [_line(primary, changing[0], "principal")]
    elif k == 2:
        lo, hi = changing
        texts = [_line(primary, hi, "principal"), _line(primary, lo, "supporting")]
    elif k == 3:
        texts = [_judgment(primary, "zhen"), _judgment(relating, "hui")]
    elif k == 4:
        lo, hi = unchanged
        texts = [_line(relating, lo, "principal"), _line(relating, hi, "supporting")]
    elif k == 5:
        texts = [_line(relating, unchanged[0], "principal")]
    elif primary.get("use_line"):
        key = "use"
        texts = [_use(primary, "principal")]
    else:
        texts = [_judgment(relating, "principal")]
    return {"rule": "zhuxi", "changing_count": k, "explanation": _explain(ZHUXI_EXPLANATIONS[key]),
            "source": ZHUXI_SOURCE, "texts": texts}

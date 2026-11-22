import json
from pathlib import Path

import wengua
from wengua.rng import SeededRng, randbelow

VECTORS = json.loads((Path(__file__).resolve().parents[2] / "spec" / "vectors.json").read_text(encoding="utf-8"))


def test_rng():
    for v in VECTORS["rng"]:
        g = SeededRng(v["seed"])
        assert [g.next_u32() for _ in v["u32"]] == v["u32"]
    for v in VECTORS["randbelow"]:
        g = SeededRng(v["seed"])
        assert [randbelow(g, v["n"]) for _ in v["values"]] == v["values"]


def test_casts():
    for v in VECTORS["casts"]:
        r = wengua.cast(method=v["method"], seed=v["seed"], mode="test")
        assert r["values"] == v["values"]
        assert r["audit"]["record"] == v["record"]


def test_readings():
    for v in VECTORS["readings"]:
        r = wengua.read_cast(v["values"], rule=v["rule"])
        num = lambda h: h["number"] if h else None  # noqa: E731
        assert [num(r[k]) for k in ("primary", "relating", "nuclear", "opposite", "inverse")] == \
            [v[k] for k in ("primary", "relating", "nuclear", "opposite", "inverse")]
        assert r["changing_lines"] == v["changing_lines"]
        assert r["selection"]["explanation"]["en"] == v["selection"]["explanation"]
        got = [[t["hexagram"], t["kind"], t["position"], t["role"], t["text"]["zh_hant"]] for t in r["selection"]["texts"]]
        assert got == v["selection"]["texts"]


def test_lookups():
    for v in VECTORS["lookups"]:
        assert [h["number"] for h in wengua.find(v["query"])] == v["numbers"], v["query"]

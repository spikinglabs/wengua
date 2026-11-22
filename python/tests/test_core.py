import pytest

import wengua
from wengua.casting import cast_coins, cast_yarrow
from wengua.rng import SecureRng, SeededRng

CHI2_CRITICAL_DF3_P001 = 16.266


def chi2(counts, probs, n):
    return sum((counts[k] - n * p) ** 2 / (n * p) for k, p in probs.items())


@pytest.mark.parametrize("method,probs", [
    (cast_coins, {6: 1 / 8, 7: 3 / 8, 8: 3 / 8, 9: 1 / 8}),
    (cast_yarrow, {6: 1 / 16, 7: 5 / 16, 8: 7 / 16, 9: 3 / 16}),
])
@pytest.mark.parametrize("rng", [SeededRng(20261122), SecureRng()])
def test_distribution(method, probs, rng):
    counts = {6: 0, 7: 0, 8: 0, 9: 0}
    casts = 4000
    for _ in range(casts):
        values, _ = method(rng)
        for v in values:
            counts[v] += 1
    assert chi2(counts, probs, casts * 6) < CHI2_CRITICAL_DF3_P001


def test_yarrow_record_is_consistent():
    _, record = cast_yarrow(SeededRng(5))
    for line in record:
        stalks = 49
        for c in line["changes"]:
            assert c["stalks"] == stalks
            assert c["left"] >= 1 and c["right"] >= 2
            assert c["left"] + c["right"] == stalks
            stalks -= c["removed"]
        assert line["remaining"] == stalks == 4 * line["value"]


def test_known_relationships():
    zhun = wengua.get("屯")
    r = wengua.read_cast([7, 8, 8, 8, 7, 8])
    assert r["primary"]["number"] == zhun["number"] == 3
    assert r["nuclear"]["number"] == 23   # 剝
    assert r["opposite"]["number"] == 50  # 鼎
    assert r["inverse"]["number"] == 4    # 蒙
    assert r["relating"] is None
    assert wengua.read_cast([9] * 6)["relating"]["number"] == 2


def test_selection_rules():
    one = wengua.read_cast([7, 7, 9, 7, 7, 7])
    assert [(t["kind"], t["position"]) for t in one["selection"]["texts"]] == [("line", 3)]
    assert one["selection"]["texts"][0]["text"]["zh_hant"].startswith("君子終日乾乾")
    six = wengua.read_cast([9, 9, 6, 6, 9, 6])  # 未濟 to 既濟... all change outside 乾/坤
    assert [t["kind"] for t in six["selection"]["texts"]] == ["judgment"]
    assert six["selection"]["texts"][0]["hexagram"] == six["relating"]["number"]


def test_seed_needs_test_mode():
    with pytest.raises(ValueError):
        wengua.cast(seed=1)
    r = wengua.cast(seed=1, mode="test")
    assert r["audit"]["test"] is True and r["audit"]["rng"] == "seeded-test"
    assert wengua.cast()["audit"]["test"] is False


def test_manual_input():
    assert wengua.read_cast([["h", "h", "h"], [2, 2, 2], 7, 8, "7", (3, 2, 2)])["values"] == [9, 6, 7, 8, 7, 7]
    for bad in ([7] * 5, [5, 7, 7, 7, 7, 7], [["h", "h"], 7, 7, 7, 7, 7], [["x", "h", "h"], 7, 7, 7, 7, 7]):
        with pytest.raises(ValueError):
            wengua.read_cast(bad)


def test_get_ambiguous_and_missing():
    with pytest.raises(ValueError, match="ambiguous"):
        wengua.get("kun")
    with pytest.raises(ValueError, match="no hexagram"):
        wengua.get("nothing")


def test_every_hexagram_roundtrips():
    for n in range(1, 65):
        h = wengua.hexagram(n)
        for q in (h["unicode"], h["binary"], h["name"]["zh_hant"], h["name"]["zh_hans"]):
            assert wengua.get(q)["number"] == n

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { cast, find, readCast, SeededRng, randbelow, castCoins, castYarrow, get, hexagram, SecureRng } from "../src/index.js";

const here = fileURLToPath(new URL(".", import.meta.url));
const V = JSON.parse(readFileSync(`${here}/../../../spec/vectors.json`, "utf8"));

test("rng matches the Python implementation", () => {
  for (const v of V.rng) {
    const g = new SeededRng(v.seed);
    assert.deepEqual(v.u32.map(() => g.nextU32()), v.u32);
  }
  for (const v of V.randbelow) {
    const g = new SeededRng(v.seed);
    assert.deepEqual(v.values.map(() => randbelow(g, v.n)), v.values);
  }
});

test("seeded casts match", () => {
  for (const v of V.casts) {
    const r = cast({ method: v.method, seed: v.seed, mode: "test" });
    assert.deepEqual(r.values, v.values);
    assert.deepEqual(r.audit.record, v.record);
  }
});

test("readings match", () => {
  for (const v of V.readings) {
    const r = readCast(v.values, { rule: v.rule });
    const num = (h: { number: number } | null) => (h ? h.number : null);
    assert.deepEqual(
      [r.primary, r.relating, r.nuclear, r.opposite, r.inverse].map(num),
      [v.primary, v.relating, v.nuclear, v.opposite, v.inverse],
    );
    assert.deepEqual(r.changing_lines, v.changing_lines);
    assert.equal(r.selection.explanation.en, v.selection.explanation);
    assert.deepEqual(
      r.selection.texts.map((t) => [t.hexagram, t.kind, t.position, t.role, t.text.zh_hant]),
      v.selection.texts,
    );
  }
});

test("lookups match", () => {
  for (const v of V.lookups) assert.deepEqual(find(v.query).map((h) => h.number), v.numbers, v.query);
});

const CHI2 = 16.266; // df = 3, p = 0.001
for (const [name, fn, probs] of [
  ["coins", castCoins, { 6: 1 / 8, 7: 3 / 8, 8: 3 / 8, 9: 1 / 8 }],
  ["yarrow", castYarrow, { 6: 1 / 16, 7: 5 / 16, 8: 7 / 16, 9: 3 / 16 }],
] as const) {
  test(`${name} distribution`, () => {
    for (const rng of [new SeededRng(20261122), new SecureRng()]) {
      const counts: Record<number, number> = { 6: 0, 7: 0, 8: 0, 9: 0 };
      const n = 4000;
      for (let i = 0; i < n; i++) for (const v of fn(rng).values) counts[v]!++;
      const stat = Object.entries(probs).reduce((s, [k, p]) => s + (counts[+k]! - n * 6 * p) ** 2 / (n * 6 * p), 0);
      assert.ok(stat < CHI2, `chi2 ${stat}`);
    }
  });
}

test("seed needs test mode", () => {
  assert.throws(() => cast({ seed: 1 }));
  const r = cast({ seed: 1, mode: "test" });
  assert.equal(r.audit.test, true);
  assert.equal(cast().audit.test, false);
});

test("manual input and errors", () => {
  assert.deepEqual(readCast([["h", "h", "h"], [2, 2, 2], 7, 8, "7", [3, 2, 2]]).values, [9, 6, 7, 8, 7, 7]);
  for (const bad of [[7, 7, 7, 7, 7], [5, 7, 7, 7, 7, 7], [["h", "h"], 7, 7, 7, 7, 7]]) assert.throws(() => readCast(bad as never));
});

test("every hexagram round-trips", () => {
  for (let n = 1; n <= 64; n++) {
    const h = hexagram(n);
    for (const q of [h.unicode, h.binary, h.name.zh_hant, h.name.zh_hans]) assert.equal(get(q).number, n);
  }
  assert.throws(() => get("kun"), /ambiguous/);
});

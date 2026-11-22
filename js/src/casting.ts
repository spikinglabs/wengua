/**
 * Casting methods. Each returns six line values, bottom to top, and a record of
 * every coin or stalk. 6 old yin (changing), 7 young yang, 8 young yin, 9 old yang (changing).
 */
import { randbelow, type Rng } from "./rng.js";

export type LineValue = 6 | 7 | 8 | 9;
export interface CoinLine { coins: number[]; value: number }
export interface YarrowChange {
  stalks: number; left: number; right: number;
  left_remainder: number; right_remainder: number; removed: number;
}
export interface YarrowLine { changes: YarrowChange[]; remaining: number; value: number }
export type LineRecord = CoinLine | YarrowLine | { value: number };
export interface CastResult { values: number[]; record: LineRecord[] }

/** Three coins per line, heads 3 and tails 2. P(6,7,8,9) = 1/8, 3/8, 3/8, 1/8. */
export function castCoins(rng: Rng): CastResult {
  const values: number[] = [];
  const record: LineRecord[] = [];
  for (let i = 0; i < 6; i++) {
    const coins = [0, 0, 0].map(() => (randbelow(rng, 2) ? 3 : 2));
    const value = coins.reduce((a, b) => a + b, 0);
    values.push(value);
    record.push({ coins, value });
  }
  return { values, record };
}

const remainder = (n: number) => (n === 0 ? 0 : ((n - 1) % 4) + 1);

/**
 * The 大衍筮法 with 49 stalks and three changes per line. The left heap is drawn
 * uniformly from 1 to the largest multiple of four that leaves the right heap a
 * stalk after hanging one, which gives exactly P(6,7,8,9) = 1/16, 5/16, 7/16, 3/16.
 */
export function castYarrow(rng: Rng): CastResult {
  const values: number[] = [];
  const record: LineRecord[] = [];
  for (let i = 0; i < 6; i++) {
    let stalks = 49;
    const changes: YarrowChange[] = [];
    for (let c = 0; c < 3; c++) {
      const left = randbelow(rng, 4 * Math.floor((stalks - 2) / 4)) + 1;
      const right = stalks - left - 1;
      const rl = remainder(left), rr = remainder(right);
      const removed = 1 + rl + rr;
      changes.push({ stalks, left, right: right + 1, left_remainder: rl, right_remainder: rr, removed });
      stalks -= removed;
    }
    const value = stalks / 4;
    values.push(value);
    record.push({ changes, remaining: stalks, value });
  }
  return { values, record };
}

export type ManualLine = number | string | Array<number | string>;

function coin(c: number | string): number {
  if (typeof c === "string") {
    const s = c.trim().toLowerCase();
    if (s === "h" || s === "heads" || s === "3") return 3;
    if (s === "t" || s === "tails" || s === "2") return 2;
  } else if (c === 2 || c === 3) return c;
  throw new RangeError(`a coin is heads (3) or tails (2), got ${JSON.stringify(c)}`);
}

/** Six values from a physical cast, bottom to top: line values or three coin faces each. */
export function parseManual(lines: ManualLine[]): CastResult {
  if (!Array.isArray(lines) || lines.length !== 6) throw new RangeError("a cast has exactly six lines, bottom to top");
  const values: number[] = [];
  const record: LineRecord[] = [];
  for (const v of lines) {
    if (Array.isArray(v)) {
      const coins = v.map(coin);
      if (coins.length !== 3) throw new RangeError("each line needs three coins");
      const value = coins.reduce((a, b) => a + b, 0);
      values.push(value);
      record.push({ coins, value });
    } else {
      const n = typeof v === "string" ? Number(v.trim()) : v;
      if (![6, 7, 8, 9].includes(n)) throw new RangeError(`line value must be 6, 7, 8 or 9, got ${JSON.stringify(v)}`);
      values.push(n);
      record.push({ value: n });
    }
  }
  return { values, record };
}

/**
 * Random sources. Real readings use the platform's secure RNG
 * (crypto.getRandomValues). The seeded generator (Mulberry32) exists only for
 * tests and replays; it matches the Python package bit for bit.
 */

export interface Rng {
  readonly name: "secure" | "seeded-test";
  nextU32(): number;
}

export class SecureRng implements Rng {
  readonly name = "secure" as const;
  private buf = new Uint32Array(64);
  private i = 64;
  nextU32(): number {
    if (this.i >= this.buf.length) {
      globalThis.crypto.getRandomValues(this.buf);
      this.i = 0;
    }
    return this.buf[this.i++]!;
  }
}

/** Mulberry32. Not for real readings. */
export class SeededRng implements Rng {
  readonly name = "seeded-test" as const;
  readonly seed: number;
  private state: number;
  constructor(seed: number) {
    if (!Number.isInteger(seed)) throw new TypeError("seed must be an integer");
    this.seed = Number(BigInt(seed) & 0xffffffffn);
    this.state = this.seed;
  }
  nextU32(): number {
    const a = (this.state + 0x6d2b79f5) >>> 0;
    this.state = a;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = ((t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t) >>> 0;
    return (t ^ (t >>> 14)) >>> 0;
  }
}

/** A uniform integer in [0, n), by rejection sampling (no modulo bias). */
export function randbelow(rng: Rng, n: number): number {
  if (!(n > 0)) throw new RangeError("n must be positive");
  const limit = 2 ** 32 - (2 ** 32 % n);
  for (;;) {
    const x = rng.nextU32();
    if (x < limit) return x % n;
  }
}

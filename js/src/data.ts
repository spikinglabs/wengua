/** The bundled dataset (wengua-data): 64 hexagrams and 8 trigrams. */
import bundleJson from "./iching.json" with { type: "json" };

export interface Text { zh_hant: string; zh_hans: string }
export interface Name extends Text { pinyin: string; en: string }
export interface Line { position: number; label: Text; text: Text; xiao_xiang: Text }
export interface UseLine { label: Text; text: Text; xiao_xiang: Text }
export interface Hexagram {
  number: number; unicode: string; binary: string;
  trigrams: { lower: string; upper: string };
  name: Name; judgment: Text; tuan: Text; image: Text;
  lines: Line[]; use_line?: UseLine | null; wenyan?: Text[] | null;
  variants?: unknown[]; source: unknown;
}
export interface Trigram { key: string; name: Name; symbol: string; binary: string }
export interface Bundle { dataset: string; version: string; license: string; trigrams: Trigram[]; hexagrams: Hexagram[] }

export const bundle = bundleJson as unknown as Bundle;

const byBinary = new Map(bundle.hexagrams.map((h) => [h.binary, h]));
const byKey = new Map(bundle.trigrams.map((t) => [t.key, t]));

/** The full record of hexagram `n` (1 to 64, King Wen order). */
export function hexagram(n: number): Hexagram {
  if (!Number.isInteger(n) || n < 1 || n > 64) throw new RangeError("hexagram number must be 1 to 64");
  return bundle.hexagrams[n - 1]!;
}

/** Six bits, bottom to top, 1 = yang. */
export function hexagramByBinary(binary: string): Hexagram {
  const h = byBinary.get(binary);
  if (!h) throw new RangeError(`not a six-bit hexagram: ${JSON.stringify(binary)}`);
  return h;
}

export function trigram(key: string): Trigram {
  const t = byKey.get(key);
  if (!t) throw new RangeError(`unknown trigram ${JSON.stringify(key)}`);
  return t;
}

export function trigrams(): Trigram[] {
  return [...bundle.trigrams];
}

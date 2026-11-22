/** Build a Reading: the full, auditable result of a cast. */
import { castCoins, castYarrow, parseManual, type LineRecord, type ManualLine } from "./casting.js";
import { bundle, hexagramByBinary, type Hexagram, type Name } from "./data.js";
import { changingPositions, inverse, nuclear, opposite, primaryBits, relatingBits } from "./derive.js";
import { SecureRng, SeededRng } from "./rng.js";
import { select, type Selection } from "./selection.js";
import { VERSION } from "./version.js";

export const METHODS = ["coins", "yarrow"] as const;
export type Method = (typeof METHODS)[number];

export interface HexagramSummary {
  number: number; unicode: string; binary: string; name: Name; trigrams: { lower: string; upper: string };
}
export interface Reading {
  question: string | null;
  locale: string | null;
  method: Method | "manual";
  values: number[];
  lines: { position: number; value: number; yang: boolean; changing: boolean }[];
  primary: HexagramSummary;
  changing_lines: number[];
  relating: HexagramSummary | null;
  nuclear: HexagramSummary;
  opposite: HexagramSummary;
  inverse: HexagramSummary;
  selection: Selection;
  audit: {
    rng: "secure" | "seeded-test" | "none"; test: boolean; seed: number | null;
    record: LineRecord[] | null; timestamp: string; library: string; dataset: string;
  };
}

export const summary = (h: Hexagram): HexagramSummary =>
  ({ number: h.number, unicode: h.unicode, binary: h.binary, name: h.name, trigrams: h.trigrams });

export interface BuildOptions {
  method: Reading["method"]; record?: LineRecord[] | null; rng?: Reading["audit"]["rng"]; seed?: number | null;
  question?: string | null; rule?: string; locale?: string | null; timestamp?: string;
}

export function buildReading(values: number[], o: BuildOptions): Reading {
  const primary = hexagramByBinary(primaryBits(values));
  const changing = changingPositions(values);
  const relating = hexagramByBinary(relatingBits(values));
  const pb = primary.binary;
  const rng = o.rng ?? "none";
  return {
    question: o.question ?? null,
    locale: o.locale ?? null,
    method: o.method,
    values: [...values],
    lines: values.map((v, i) => ({ position: i + 1, value: v, yang: v === 7 || v === 9, changing: v === 6 || v === 9 })),
    primary: summary(primary),
    changing_lines: changing,
    relating: changing.length ? summary(relating) : null,
    nuclear: summary(hexagramByBinary(nuclear(pb))),
    opposite: summary(hexagramByBinary(opposite(pb))),
    inverse: summary(hexagramByBinary(inverse(pb))),
    selection: select(primary, relating, changing, o.rule ?? "zhuxi"),
    audit: {
      rng, test: rng === "seeded-test", seed: o.seed ?? null, record: o.record ?? null,
      timestamp: o.timestamp ?? new Date().toISOString().replace(/\.\d{3}Z$/, "+00:00"),
      library: `wengua-js ${VERSION}`,
      dataset: `${bundle.dataset} ${bundle.version}`,
    },
  };
}

export interface CastOptions {
  question?: string | null; method?: Method; rule?: string; locale?: string | null;
  /** Only allowed with mode "test"; the reading is then labelled as a test. */
  seed?: number; mode?: "test";
}

/** Cast a hexagram with a secure RNG and return a Reading. */
export function cast(o: CastOptions = {}): Reading {
  const method = o.method ?? "coins";
  if (!METHODS.includes(method)) throw new RangeError(`unknown method ${JSON.stringify(method)}; choose one of ${METHODS.join(", ")}`);
  if (o.seed !== undefined && o.mode !== "test") throw new RangeError('a seed is only allowed with mode "test"');
  const rng = o.seed !== undefined ? new SeededRng(o.seed) : new SecureRng();
  const { values, record } = (method === "coins" ? castCoins : castYarrow)(rng);
  return buildReading(values, {
    method, record, rng: rng.name, seed: rng instanceof SeededRng ? rng.seed : null,
    question: o.question, rule: o.rule, locale: o.locale,
  });
}

/** A Reading from a physical cast: six line values or coin faces, bottom to top. */
export function readCast(lines: ManualLine[], o: { question?: string | null; rule?: string; locale?: string | null } = {}): Reading {
  const { values, record } = parseManual(lines);
  return buildReading(values, { method: "manual", record, rng: "none", question: o.question, rule: o.rule, locale: o.locale });
}

/** Find hexagrams from whatever identifier a person or model has at hand. */
import { bundle, hexagram, hexagramByBinary, trigram, trigrams, type Hexagram } from "./data.js";

/** Nature images of the trigrams, as used in full names such as 水雷屯 and 乾為天. */
const IMAGES: Record<string, string> = {
  "天": "qian", "地": "kun", "雷": "zhen", "風": "xun", "风": "xun", "水": "kan",
  "火": "li", "山": "gen", "澤": "dui", "泽": "dui",
};
/** Common alternative characters for hexagram names. */
const ALIASES: Record<string, number> = { "恆": 32, "遁": 33, "豐": 55, "旣濟": 63 };

/** Lower case, no tone marks, no spaces or punctuation; ü becomes v. */
export function normalizeLatin(s: string): string {
  return s.trim().toLowerCase().normalize("NFD")
    .replace(/u\u0308/g, "v").replace(/u:/g, "v")
    .replace(/\p{Mn}/gu, "")
    .replace(/[\s\-'’_.]/g, "");
}

function trigramKey(token: string): string | null {
  if (token in IMAGES) return IMAGES[token]!;
  const t = normalizeLatin(token);
  for (const tri of trigrams()) {
    const n = tri.name;
    if ([n.zh_hant, n.zh_hans, tri.symbol].includes(token) || t === tri.key || t === normalizeLatin(n.en)) return tri.key;
  }
  return null;
}

function fromTrigrams(upper: string, lower: string): Hexagram | null {
  const u = trigramKey(upper), l = trigramKey(lower);
  if (!u || !l) return null;
  return hexagramByBinary(trigram(l).binary + trigram(u).binary);
}

const isName = (h: Hexagram, s: string) => s === h.name.zh_hant || s === h.name.zh_hans;

/**
 * All hexagrams matching `query`, best first. Accepts a number, a Chinese name
 * (繁 or 简), a full name (水雷屯, 乾為天), pinyin with or without tones, the English
 * name, the Unicode symbol, six bits bottom to top, or a trigram pair
 * (坎上震下, 上坎下震, water over thunder).
 */
export function find(query: number | string): Hexagram[] {
  if (typeof query === "number") return Number.isInteger(query) && query >= 1 && query <= 64 ? [hexagram(query)] : [];
  const q = String(query).trim();
  if (!q) return [];
  if (/^[01]{6}$/.test(q)) return [hexagramByBinary(q)];
  if (/^\d+$/.test(q)) {
    const n = Number(q);
    return n >= 1 && n <= 64 ? [hexagram(n)] : [];
  }
  if (q.length === 1 && q.charCodeAt(0) >= 0x4dc0 && q.charCodeAt(0) <= 0x4dff) return [hexagram(q.charCodeAt(0) - 0x4dc0 + 1)];
  if (q in ALIASES) return [hexagram(ALIASES[q]!)];

  const hexes = bundle.hexagrams;
  const named = hexes.find((h) => isName(h, q));
  if (named) return [named];

  let m = /^(.)上(.)下$/u.exec(q) ?? /^上(.)下(.)$/u.exec(q);
  if (m) { const h = fromTrigrams(m[1]!, m[2]!); if (h) return [h]; }
  m = /^(.)[為为](.)$/u.exec(q);
  if (m) {
    const k = trigramKey(m[1]!);
    if (k && k === IMAGES[m[2]!]) return [fromTrigrams(m[1]!, m[1]!)!];
  }
  const chars = [...q];
  if (chars.length >= 3 && chars[0]! in IMAGES && chars[1]! in IMAGES) {
    const h = fromTrigrams(chars[0]!, chars[1]!);
    const rest = chars.slice(2).join("");
    if (h && (isName(h, rest) || ALIASES[rest] === h.number)) return [h];
  }
  m = /^\s*(\w+)\s+over\s+(\w+)\s*$/i.exec(q);
  if (m) { const h = fromTrigrams(m[1]!, m[2]!); if (h) return [h]; }

  const latin = normalizeLatin(q);
  if (!latin) return [];
  const toned = q.toLowerCase().replace(/ /g, "").normalize("NFC");
  const exact = hexes.filter((h) => h.name.pinyin.replace(/ /g, "") === toned);
  if (exact.length) return exact;
  const plain = hexes.filter((h) => normalizeLatin(h.name.pinyin) === latin);
  if (plain.length) return plain;
  const loose = hexes.filter((h) => normalizeLatin(h.name.pinyin).replace(/v/g, "u") === latin.replace(/v/g, "u"));
  if (loose.length) return loose;
  return hexes.filter((h) => normalizeLatin(h.name.en) === latin || normalizeLatin(h.name.en.replace(/^the\s+/i, "")) === latin);
}

/** Exactly one hexagram; throws if there is none or more than one. */
export function get(query: number | string): Hexagram {
  const found = find(query);
  if (!found.length) throw new RangeError(`no hexagram matches ${JSON.stringify(query)}`);
  if (found.length > 1) {
    const names = found.map((h) => `${h.number} ${h.name.zh_hant} ${h.name.pinyin}`).join(", ");
    throw new RangeError(`${JSON.stringify(query)} is ambiguous: ${names}`);
  }
  return found[0]!;
}

/**
 * Which texts to read (取辭). The default rule follows Zhu Xi, 《易學啓蒙·考變占》.
 * The `all` rule returns every text that could matter.
 */
import type { Hexagram, Text } from "./data.js";

export const RULES = ["zhuxi", "all"] as const;
export type Rule = (typeof RULES)[number];
export type Role = "principal" | "supporting" | "zhen" | "hui" | "context" | "changing" | "outcome";
export interface SelectedText {
  hexagram: number; kind: "judgment" | "line" | "use"; position: number | null;
  label: Text | null; text: Text; role: Role;
}
export interface Explanation { en: string; zh_hant: string; zh_hans: string }
export interface Selection {
  rule: Rule; changing_count: number; explanation: Explanation;
  source: Explanation | null; texts: SelectedText[];
}

export const ZHUXI_SOURCE: Explanation = {
  zh_hant: "朱熹《易學啓蒙·考變占》", zh_hans: "朱熹《易学启蒙·考变占》",
  en: "Zhu Xi, Yixue Qimeng, 'Examining the changes'",
};

const ex = (en: string, zh_hant: string, zh_hans: string): Explanation => ({ en, zh_hant, zh_hans });

const ZHUXI: Record<string, Explanation> = {
  0: ex("No changing lines: read the judgment of the primary hexagram.",
    "六爻皆不變：占本卦卦辭。", "六爻皆不变：占本卦卦辞。"),
  1: ex("One changing line: read that line of the primary hexagram.",
    "一爻變：以本卦變爻之辭占。", "一爻变：以本卦变爻之辞占。"),
  2: ex("Two changing lines: read both lines of the primary hexagram; the upper one leads.",
    "二爻變：以本卦二變爻之辭占，以上爻為主。", "二爻变：以本卦二变爻之辞占，以上爻为主。"),
  3: ex("Three changing lines: read the judgments of the primary hexagram (貞, the base) " +
    "and the relating hexagram (悔, the outcome).",
    "三爻變：占本卦及之卦之卦辭，以本卦為貞，之卦為悔。",
    "三爻变：占本卦及之卦之卦辞，以本卦为贞，之卦为悔。"),
  4: ex("Four changing lines: read the two unchanging lines of the relating hexagram; the lower one leads.",
    "四爻變：以之卦二不變爻之辭占，以下爻為主。", "四爻变：以之卦二不变爻之辞占，以下爻为主。"),
  5: ex("Five changing lines: read the one unchanging line of the relating hexagram.",
    "五爻變：以之卦不變爻之辭占。", "五爻变：以之卦不变爻之辞占。"),
  6: ex("All six lines change: read the judgment of the relating hexagram.",
    "六爻皆變：占之卦卦辭。", "六爻皆变：占之卦卦辞。"),
  use: ex("All six lines change in Qian or Kun: read 用九 or 用六.",
    "六爻皆變，乾坤占二用：以用九、用六之辭占。", "六爻皆变，乾坤占二用：以用九、用六之辞占。"),
};

const ALL = ex("Every relevant text: the primary judgment, each changing line, and the relating judgment.",
  "列出所有相關文辭：本卦卦辭、各變爻爻辭、之卦卦辭。",
  "列出所有相关文辞：本卦卦辞、各变爻爻辞、之卦卦辞。");

const judgment = (h: Hexagram, role: Role): SelectedText =>
  ({ hexagram: h.number, kind: "judgment", position: null, label: null, text: h.judgment, role });
const line = (h: Hexagram, p: number, role: Role): SelectedText => {
  const l = h.lines[p - 1]!;
  return { hexagram: h.number, kind: "line", position: p, label: l.label, text: l.text, role };
};
const use = (h: Hexagram, role: Role): SelectedText =>
  ({ hexagram: h.number, kind: "use", position: null, label: h.use_line!.label, text: h.use_line!.text, role });

export function select(primary: Hexagram, relating: Hexagram, changing: number[], rule: string = "zhuxi"): Selection {
  const k = changing.length;
  if (rule === "all") {
    const texts = [judgment(primary, "context"), ...changing.map((p) => line(primary, p, "changing"))];
    if (k === 6 && primary.use_line) texts.push(use(primary, "changing"));
    if (k) texts.push(judgment(relating, "outcome"));
    return { rule: "all", changing_count: k, explanation: ALL, source: null, texts };
  }
  if (rule !== "zhuxi") throw new RangeError(`unknown rule ${JSON.stringify(rule)}; choose one of ${RULES.join(", ")}`);
  let key: string = String(k);
  const unchanged = [1, 2, 3, 4, 5, 6].filter((p) => !changing.includes(p));
  let texts: SelectedText[];
  if (k === 0) texts = [judgment(primary, "principal")];
  else if (k === 1) texts = [line(primary, changing[0]!, "principal")];
  else if (k === 2) texts = [line(primary, changing[1]!, "principal"), line(primary, changing[0]!, "supporting")];
  else if (k === 3) texts = [judgment(primary, "zhen"), judgment(relating, "hui")];
  else if (k === 4) texts = [line(relating, unchanged[0]!, "principal"), line(relating, unchanged[1]!, "supporting")];
  else if (k === 5) texts = [line(relating, unchanged[0]!, "principal")];
  else if (primary.use_line) { key = "use"; texts = [use(primary, "principal")]; }
  else texts = [judgment(relating, "principal")];
  return { rule: "zhuxi", changing_count: k, explanation: ZHUXI[key]!, source: ZHUXI_SOURCE, texts };
}

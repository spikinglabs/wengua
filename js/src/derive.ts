/** Hexagram relationships. Binary strings run bottom to top, 1 = yang. */
export const primaryBits = (v: number[]) => v.map((x) => (x === 7 || x === 9 ? "1" : "0")).join("");
/** 之卦: the changing lines (6 and 9) turn into their opposite. */
export const relatingBits = (v: number[]) => v.map((x) => (x === 6 || x === 7 ? "1" : "0")).join("");
export const changingPositions = (v: number[]) =>
  v.flatMap((x, i) => (x === 6 || x === 9 ? [i + 1] : []));
/** 互卦: lines 2-4 form the lower trigram, lines 3-5 the upper. */
export const nuclear = (b: string) => b.slice(1, 4) + b.slice(2, 5);
/** 錯卦: every line inverted. */
export const opposite = (b: string) => [...b].map((c) => (c === "1" ? "0" : "1")).join("");
/** 綜卦: the hexagram turned upside down. */
export const inverse = (b: string) => [...b].reverse().join("");

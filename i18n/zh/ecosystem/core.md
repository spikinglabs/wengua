---
description: "问卦 Wengua 的 TypeScript 与 Python 核心库：公平的三钱法与大衍筮法、变爻、相关卦、朱熹取辞规则和查卦。"
---

# 核心库

TypeScript（`npm install wengua`）和 Python（`pip install wengua`）实现同一套逻辑。两个包都必须通过同一份测试向量（`spec/vectors.json`），所以不会各走各的：同一个种子在两边得到同样的卦，连每枚铜钱都一样。

=== "Python"

    <!-- no-convert -->
    ```python
    import wengua

    r = wengua.cast("这次搬家我应当明白什么？", method="yarrow")
    r["primary"]["name"]          # {'zh_hant': '豐', 'zh_hans': '丰', 'pinyin': 'fēng', 'en': 'Abundance'}
    r["selection"]["texts"]       # 按朱熹规则选出的要读的文字，繁简俱全

    wengua.read_cast([9, 8, 7, 7, 8, 6])   # 实物起卦的结果，自下而上
    wengua.get("水雷屯")                     # 第三卦的完整记录
    ```

=== "TypeScript"

    <!-- no-convert -->
    ```ts
    import { cast, readCast, get } from "wengua";

    const r = cast({ question: "这次搬家我应当明白什么？", method: "yarrow" });
    r.primary.name;            // { zh_hant: "豐", zh_hans: "丰", pinyin: "fēng", en: "Abundance" }
    r.selection.texts;         // 要读的文字，繁简俱全

    readCast([9, 8, 7, 7, 8, 6]);
    get("水雷屯");
    ```

## 起卦方法

| 方法 | 6 老阴 | 7 少阳 | 8 少阴 | 9 老阳 |
|---|---|---|---|---|
| 三枚铜钱 | 1/8 | 3/8 | 3/8 | 1/8 |
| 蓍草（大衍筮法） | 1/16 | 5/16 | 7/16 | 3/16 |
| 手动 | 来自实物起卦 | | | |

- **铜钱：** 每爻掷三枚公平的铜钱，字为 3，背为 2，每枚都有记录。
- **蓍草：** 完整模拟大衍筮法，用四十九策，每爻三变：分二、挂一、揲四、归奇。每次分策都有记录。左堆的策数在 1 到“使右堆至少留一策的最大四的倍数”之间均匀抽取，因此每种余数机会均等，概率正好是 1/16、5/16、7/16、3/16。若简单地均匀分堆，老阴的概率会是约 4.8%，而不是 6.25%。
- **随机数**来自操作系统（Python 用 `secrets`，JavaScript 用 `crypto.getRandomValues`），并用拒绝采样避免取模偏差。只有在 `mode="test"` 时才接受 `seed`，这类结果会带有 `audit.test: true`。
- CI 对两种方法、两种随机源都做卡方检验。

## 推演

本卦、动爻、之卦、互卦、错卦（每爻阴阳互换）、综卦（上下颠倒）。

## 取辞

默认规则出自朱熹《易学启蒙·考变占》：

| 变爻数 | 读 |
|---|---|
| 0 | 本卦卦辞 |
| 1 | 本卦该变爻的爻辞 |
| 2 | 本卦两个变爻的爻辞，以上爻为主 |
| 3 | 本卦（贞）与之卦（悔）的卦辞 |
| 4 | 之卦两个不变爻的爻辞，以下爻为主 |
| 5 | 之卦唯一不变爻的爻辞 |
| 6 | 之卦卦辞；乾、坤则读用九、用六 |

每段选出的文字都有 `role`（`principal`、`supporting`、`zhen`、`hui`），结果里还附有该规则的繁体、简体和英文说明。设 `rule="all"` 则返回所有相关文字。

## 查卦

`find()` 返回所有匹配，`get()` 只返回一个。两者都接受：卦序、任一字体的卦名（訟或讼）、全名（水雷屯、乾为天）、带或不带声调的拼音（`xiǎo chù`、`xiaochu`）、英文名、卦符（䷂）、自下而上的六位二进制（`100010`），或上下卦组合（坎上震下、上坎下震、`water over thunder`）。像 `kun`（坤和困）这样有歧义的拼音会两个都返回。

## Reading 对象

`question`、`locale`、`method`、`values`（六个数，自下而上）、`lines`、`primary`、`changing_lines`、`relating`、`nuclear`、`opposite`、`inverse`、`selection`（`rule`、`explanation`、`source`、`texts`）和 `audit`（`rng`、`test`、`seed`、`record`、`timestamp`、`library`、`dataset`）。

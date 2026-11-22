---
description: "开放、有出处的六十四卦双语数据集：卦辞、爻辞、十翼，以及理雅各（James Legge）的英译。"
---

# 数据集

`wengua-data` 是一切的基础：每卦一条 JSON 记录，外加八卦，发布在 npm 和 PyPI 上。

## 每一卦包含

- 文王卦序、Unicode 卦符（䷀…䷿）、六位二进制（自下而上）、上下卦
- 繁体、简体、拼音和英文卦名
- 卦辞、彖传、大象、文言（仅乾、坤）
- 六爻，每爻有爻题（初九……上六）、爻辞和小象，另有用九、用六
- 每段文字都有 `zh_hant` 和 `zh_hans`，也都有 `en_legge`，即理雅各的英译。之后还会加上 `zh_plain` 和 `en_plain`
- `variants`（与对校本的差异）以及指向确切来源文件的 `source` 链接

## 来源

| 层次 | 来源 | 状态 |
|---|---|---|
| 中文（繁/简） | 汉籍リポジトリ（Kanseki Repository）KR1a0001《周易》，与宋本（四部丛刊本王弼《周易注》）逐字校勘，并与中文维基文库对校 | ✅ 完成 |
| 英文 | 理雅各 *The Yî King*（1882），公有领域，据三种扫描本和维基文库重建（[方法](https://github.com/spikinglabs/wengua/blob/main/data/sources/legge/README.md)） | ✅ 全部文字 |
| 白话注释 | 由问卦贡献者撰写 | 计划中 |

宋本和维基文库一致而与底本不同之处，恢复通行读法，并记入该卦的 `emendations` 字段（共 23 处）。其余差异列在 `data/collation-sbck.json` 和 `data/cross-check.json` 中。所用版本、快照和编辑取舍见 [`data/SOURCES.md`](https://github.com/spikinglabs/wengua/blob/main/data/SOURCES.md)。

数据集采用 **CC BY-SA 4.0** 许可。经文本身属于公有领域；许可涵盖所依据的数字转录，以及我们的结构和释义。

我们**不**使用任何仍受版权保护的现代译本或注释。

## 校验

CI 从仓库里的来源快照重新生成数据，结果与已提交的不同就报错。然后检查：共 64 卦、384 爻加用九、用六；二进制、卦序、Unicode 和上下卦相互一致；每个爻题（九/六）与其阴阳相符；没有空字段；简体中的“乾”不会变成 `干`；每段文字（包括文言）都有干净的 `en_legge`。

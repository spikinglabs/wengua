"""Build the whole website in three languages.

- English: `docs/`, configured by `zensical.toml`, built to `site/`.
- Simplified Chinese: `i18n/zh/`, built to `site/zh/`.
- Traditional Chinese: generated from `i18n/zh/` with OpenCC (s2twp: Taiwan
  standard with Taiwan wording) into `.i18n/zh-hant/`, built to `site/zh-hant/`.

The Chinese configs are derived from `zensical.toml`: same theme and Markdown
extensions, with the language, URLs, navigation titles and directories
replaced. Inline code is never converted; a fenced block is converted unless
the line before it is `<!-- no-convert -->`.

Usage: python scripts/build_site.py            (all three, from a clean site/)
       python scripts/build_site.py --check    (only check that every English page has a Chinese one)
"""

from __future__ import annotations

import copy
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import tomli_w

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
ZH = ROOT / "i18n" / "zh"
GEN = ROOT / ".i18n"
SITE_URL = "https://wengua.allo.land/"

# Navigation and site strings for Simplified Chinese, keyed by the English title.
NAV_ZH = {
    "Home": "首页",
    "Get started": "快速上手",
    "Other clients": "其他客户端",
    "APIs and libraries": "API 与程序库",
    "Ecosystem": "生态",
    "Dataset": "数据集",
    "Core library": "核心库",
    "MCP server": "MCP 服务",
    "Reading card (MCP App)": "卦象卡片（MCP App）",
    "CLI": "命令行",
    "Design": "设计",
    "Roadmap": "路线图",
    "Contributing": "参与贡献",
    "Privacy": "隐私",
}
SITE_ZH = {
    "site_name": "问卦 Wengua",
    "site_description": "为所有 AI 打造的准确、开放的《易经》工具",
    "copyright": "代码 MIT · 经文属公有领域 · 问卦注释 CC BY 4.0",
}

LANGS = [
    # code, theme language, URL prefix, source dir, OpenCC config (None = as written)
    ("zh", "zh", "zh/", ZH, None),
    ("zh-hant", "zh-Hant", "zh-hant/", GEN / "zh-hant", "s2twp"),
]

FENCE = re.compile(r"^(?P<indent>[ \t]*)(?P<fence>```+|~~~+)[^\n]*\n.*?^(?P=indent)(?P=fence)[ \t]*$", re.M | re.S)
INLINE = re.compile(r"`[^`\n]+`")
KEEP = "<!-- no-convert -->"
# Taiwan wording that OpenCC gets wrong in this context. 字体 here means a
# script (繁/简), not a typeface.
TW_FIXES = {"字型": "字體", "賬號": "帳號", "自定義": "自訂", "數字轉錄": "數位轉錄", "質量": "品質", "構建": "建置", "指令碼": "腳本", "倉庫": "儲存庫"}


class Converter:
    def __init__(self, name: str):
        import opencc

        self.cc = opencc.OpenCC(name)

    def convert(self, text: str) -> str:
        text = self.cc.convert(text)
        for wrong, right in TW_FIXES.items():
            text = text.replace(wrong, right)
        return text


def convert_markdown(text: str, conv) -> str:
    """Convert to traditional with OpenCC.

    Inline code is never converted (identifiers, and `干` where the page talks
    about simplified characters). Fenced blocks are converted, so comments and
    example questions read in traditional, unless the line before the fence is
    `<!-- no-convert -->` (blocks that show simplified data on purpose).
    """
    def prose(chunk: str) -> str:
        out, pos = [], 0
        for m in INLINE.finditer(chunk):
            out.append(conv.convert(chunk[pos : m.start()]))
            out.append(m.group(0))
            pos = m.end()
        out.append(conv.convert(chunk[pos:]))
        return "".join(out)

    out, pos = [], 0
    for m in FENCE.finditer(text):
        before = text[pos : m.start()]
        out.append(prose(before))
        keep = before.rstrip().endswith(KEEP)
        out.append(m.group(0) if keep else conv.convert(m.group(0)))
        pos = m.end()
    out.append(prose(text[pos:]))
    return "".join(out)


def nav_titles(nav, table):
    """Translate titles in a Zensical nav; drop entries whose page is missing is not allowed."""
    result = []
    for item in nav:
        if isinstance(item, str):
            result.append(item)
            continue
        new = {}
        for title, value in item.items():
            name = table.get(title, title)
            new[name] = nav_titles(value, table) if isinstance(value, list) else value
        result.append(new)
    return result


def nav_pages(nav):
    for item in nav:
        if isinstance(item, str):
            yield item
        else:
            for value in item.values():
                yield from (nav_pages(value) if isinstance(value, list) else [value])


def check(project: dict) -> list[str]:
    missing = []
    for page in nav_pages(project["nav"]):
        if not (ZH / page).exists():
            missing.append(page)
    for page in ZH.rglob("*.md"):
        rel = page.relative_to(ZH).as_posix()
        if not (DOCS / rel).exists():
            missing.append(f"{rel} (no English page)")
    return missing


def generate_hant(conv_name: str, dest: Path) -> None:
    conv = Converter(conv_name)
    if dest.exists():
        shutil.rmtree(dest)
    for src in ZH.rglob("*"):
        if src.is_dir():
            continue
        out = dest / src.relative_to(ZH)
        out.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix == ".md":
            out.write_text(convert_markdown(src.read_text(encoding="utf-8"), conv), encoding="utf-8")
        else:
            shutil.copy2(src, out)
    for key in ("site_name", "site_description", "copyright"):
        SITE_HANT[key] = conv.convert(SITE_ZH[key])
    for k, v in NAV_ZH.items():
        NAV_HANT[k] = conv.convert(v)


SITE_HANT: dict[str, str] = {}
NAV_HANT: dict[str, str] = {}


def config_for(base: dict, code: str, lang: str, prefix: str, src: Path) -> dict:
    cfg = copy.deepcopy(base)
    p = cfg["project"]
    strings, nav = (SITE_ZH, NAV_ZH) if code == "zh" else (SITE_HANT, NAV_HANT)
    p.update(strings)
    p["site_url"] = SITE_URL + prefix
    p["docs_dir"] = src.relative_to(ROOT).as_posix()
    p["site_dir"] = f"site/{prefix.rstrip('/')}"
    # Edit links always point at the Simplified source, which the traditional pages come from.
    p["edit_uri"] = "edit/main/i18n/zh/"
    p["nav"] = nav_titles(p["nav"], nav)
    p["theme"]["language"] = lang
    return cfg


def copy_shared(dest: Path) -> None:
    """Assets (cast box, icon, language links) are shared with the English docs."""
    target = dest / "assets"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(DOCS / "assets", target)


def build(config: Path, clean: bool) -> None:
    cmd = ["zensical", "build", "-f", str(config)] + (["--clean"] if clean else [])
    subprocess.run(cmd, check=True, cwd=ROOT)


def main() -> None:
    base = tomllib.loads((ROOT / "zensical.toml").read_text(encoding="utf-8"))
    missing = check(base["project"])
    if missing:
        sys.exit("Pages without a translation:\n  " + "\n  ".join(missing))
    if "--check" in sys.argv:
        print("Every page has English and Chinese versions.")
        return

    site = ROOT / "site"
    if site.exists():
        shutil.rmtree(site)
    build(ROOT / "zensical.toml", clean=True)

    GEN.mkdir(exist_ok=True)
    (GEN / ".gitignore").write_text("*\n", encoding="utf-8")
    for code, lang, prefix, src, conv in LANGS:
        if conv:
            generate_hant(conv, src)
        copy_shared(src)
        cfg_path = ROOT / f"zensical.{code}.toml"  # must sit in the project root
        cfg_path.write_text(tomli_w.dumps(config_for(base, code, lang, prefix, src)), encoding="utf-8")
        try:
            build(cfg_path, clean=True)
        finally:
            cfg_path.unlink()
        if src == ZH:
            shutil.rmtree(src / "assets")
    print("Built site/ (en), site/zh/ (简体) and site/zh-hant/ (繁體).")


if __name__ == "__main__":
    main()

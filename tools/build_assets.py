"""Готовит ресурсы сайта: шрифт приложения в WOFF (кириллица и латиница), скриншоты в webp, иконки.

Запуск: py -3.12 D:\\RuStore\\_site\\tools\\build_assets.py
Источники: шрифты серии в _shared\\fonts, скриншоты и иконка в uchim-vremya\\store.
"""
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SRC_FONTS = ROOT / "_shared" / "fonts"
STORE = ROOT / "uchim-vremya" / "store"
OUT = ROOT / "_site" / "assets"

UNICODES = ("U+0020-007E,U+00A0-00BF,U+0401,U+0410-044F,U+0451,U+2010-2014,"
            "U+2018-201E,U+2026,U+2116,U+20BD")
SCREENS = ["01_karta_urovnej", "02_polovina_chetvertogo", "03_postav_strelki"]


def fonts() -> None:
    (OUT / "fonts").mkdir(parents=True, exist_ok=True)
    for name in ["BalsamiqSans-Regular", "BalsamiqSans-Bold"]:
        opts = subset.Options()
        opts.flavor = "woff"
        opts.layout_features = ["*"]
        font = TTFont(SRC_FONTS / f"{name}.ttf")
        sub = subset.Subsetter(opts)
        sub.populate(unicodes=subset.parse_unicodes(UNICODES))
        sub.subset(font)
        font.flavor = "woff"
        dst = OUT / "fonts" / f"{name}.woff"
        font.save(dst)
        print(dst.name, dst.stat().st_size)


def images() -> None:
    (OUT / "img").mkdir(parents=True, exist_ok=True)
    for n in SCREENS:
        im = Image.open(STORE / "screenshots" / f"{n}.png").convert("RGB")
        im = im.resize((540, round(im.height * 540 / im.width)), Image.LANCZOS)
        dst = OUT / "img" / f"{n}.webp"
        im.save(dst, "WEBP", quality=86, method=6)
        print(dst.name, im.size, dst.stat().st_size)
    icon = Image.open(STORE / "icon_512.png").convert("RGBA")
    for size, name in [(240, "app-icon.png"), (180, "apple-touch-icon.png"), (32, "favicon-32.png")]:
        icon.resize((size, size), Image.LANCZOS).save(OUT / "img" / name, optimize=True)
        print(name)


if __name__ == "__main__":
    fonts()
    images()

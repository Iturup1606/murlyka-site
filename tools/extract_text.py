"""Выгружает видимый текст страниц сайта в .txt (UTF-8) для проверки humanizer-ru-check.

Запуск: py -3.12 D:\\RuStore\\_site\\tools\\extract_text.py <папка для txt>
"""
import html
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
BLOCK = {"p", "h1", "h2", "h3", "li", "figure"}


class Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "svg", "head", "nav", "header", "footer"):
            self.skip += 1
        if tag in BLOCK:
            self.out.append("\n")
        elif tag == "br":
            self.out.append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg", "head", "nav", "header", "footer"):
            self.skip -= 1
        if tag in ("p", "h1", "h2", "h3", "li"):
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def main() -> None:
    dst = Path(sys.argv[1])
    dst.mkdir(parents=True, exist_ok=True)
    for name, path in [("index", "index.html"), ("privacy", "privacy/index.html")]:
        t = Text()
        t.feed((SITE / path).read_text(encoding="utf-8"))
        text = html.unescape("".join(t.out)).replace("\u00a0", " ")
        lines = [re.sub(r"\s+", " ", l).strip() for l in text.splitlines()]
        body = "\n".join(l for l in lines if l)
        # заголовки без точки склеиваем с точкой, чтобы детектор видел предложения
        body = re.sub(r"([^.!?:;»])\n", r"\1.\n", body)
        (dst / f"murlyka_{name}.txt").write_text(body + "\n", encoding="utf-8")
        print(name, len(body.split()), "слов")


if __name__ == "__main__":
    main()

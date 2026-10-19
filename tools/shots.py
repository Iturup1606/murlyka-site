"""Скриншоты сайта на компьютере (1440) и телефоне (390), плотность 2, и простые проверки.

Запуск локально:   py -3.12 D:\\RuStore\\_site\\tools\\shots.py
Запуск по адресу:  py -3.12 D:\\RuStore\\_site\\tools\\shots.py --url https://iturup1606.github.io/murlyka-site --tag live
Снимки: D:\\RuStore\\_site\\shots\\<tag>_<страница>_<размер>.png
Проверки: горизонтальная прокрутка, ошибки консоли, загрузка шрифта, битые картинки.
"""
import argparse
import functools
import http.server
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

SITE = Path(__file__).resolve().parents[1]
OUT = SITE / "shots"
SIZES = {"desktop": (1440, 900), "tablet": (820, 1180), "phone": (390, 844)}


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args) -> None:
        pass


def serve() -> str:
    handler = functools.partial(QuietHandler, directory=str(SITE))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{httpd.server_address[1]}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", help="адрес сайта; без него поднимается локальный сервер")
    ap.add_argument("--tag", default="local")
    args = ap.parse_args()
    base = (args.url or serve()).rstrip("/")
    # privacy/index.html: и /privacy, и /privacy/ открывают политику (Pages перенаправляет без слэша)
    pages = {"index": "/", "privacy": "/privacy"}
    OUT.mkdir(exist_ok=True)
    problems = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for size, (w, h) in SIZES.items():
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=2,
                                      is_mobile=size == "phone", has_touch=size == "phone")
            page = ctx.new_page()
            errors = []
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: errors.append(str(e)))
            for name, path in pages.items():
                resp = page.goto(base + path, wait_until="networkidle")
                status = resp.status if resp else 0
                page.wait_for_timeout(2600)  # котик доигрывает взмах
                page.screenshot(path=str(OUT / f"{args.tag}_{name}_{size}_hero.png"))
                # прокрутка до конца, чтобы сработали появления, потом снимок всей страницы
                page.evaluate("""async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) {
                    window.scrollTo(0, y); await new Promise(r => setTimeout(r, 90)); } }""")
                page.wait_for_timeout(1400)
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(300)
                page.screenshot(path=str(OUT / f"{args.tag}_{name}_{size}_full.png"), full_page=True)
                info = page.evaluate("""() => ({
                    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                    font: document.fonts.check('700 20px "Balsamiq Sans"'),
                    broken: [...document.images].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src),
                    hidden: [...document.querySelectorAll('.reveal:not(.is-in)')].length })""")
                print(f"{size:7} {name:7} status={status} overflow={info['overflow']} font={info['font']} "
                      f"broken={info['broken']} not_revealed={info['hidden']}")
                if status != 200 or info["overflow"] > 0 or not info["font"] or info["broken"]:
                    problems.append(f"{size} {name}: {status} {info}")
            if errors:
                problems.append(f"{size}: ошибки консоли {errors}")
            ctx.close()
        browser.close()
    print("ПРОБЛЕМЫ:\n" + "\n".join(problems) if problems else "Проблем не найдено")


if __name__ == "__main__":
    main()

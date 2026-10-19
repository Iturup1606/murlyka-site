"""Ждёт, пока домен начнёт указывать на GitHub Pages (DNS по HTTPS: dns.google, при сбое cloudflare-dns.com).

Запуск: py -3.12 D:\\RuStore\\_site\\tools\\wait_dns.py [домен] [--hours 12]
Выход 0: у корня домена есть A-записи и все они - адреса GitHub Pages. Выход 1: не дождались.
Раз в минуту печатает, что видит DNS: A корня, AAAA корня, CNAME у www.
"""
import argparse
import json
import sys
import time
import urllib.request

GITHUB_A = {"185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153"}
RESOLVERS = ["https://dns.google/resolve?name={}&type={}",
             "https://cloudflare-dns.com/dns-query?name={}&type={}"]


def query(name: str, rtype: str) -> list[str] | None:
    for url in RESOLVERS:
        try:
            req = urllib.request.Request(url.format(name, rtype), headers={"accept": "application/dns-json"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.load(r)
            code = {"A": 1, "AAAA": 28, "CNAME": 5}[rtype]
            return [a["data"].rstrip(".") for a in data.get("Answer", []) if a.get("type") == code]
        except Exception:
            continue
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("domain", nargs="?", default="murlyka-kids.ru")
    ap.add_argument("--hours", type=float, default=12)
    args = ap.parse_args()
    deadline = time.time() + args.hours * 3600
    while time.time() < deadline:
        a = query(args.domain, "A")
        aaaa = query(args.domain, "AAAA")
        www = query("www." + args.domain, "CNAME")
        print(time.strftime("%H:%M:%S"), "A:", a, "AAAA:", aaaa, "www CNAME:", www, flush=True)
        if a and set(a) <= GITHUB_A:
            print("ГОТОВО: корень домена указывает на GitHub Pages", flush=True)
            sys.exit(0)
        time.sleep(60)
    print("НЕ ДОЖДАЛИСЬ: записи GitHub в DNS не появились", flush=True)
    sys.exit(1)


if __name__ == "__main__":
    main()

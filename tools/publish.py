"""Публикует сайт на GitHub Pages: копия _site -> D:\\RuStore\\_site_pages (отдельный git), коммит, push.

Запуск: py -3.12 D:\\RuStore\\_site\\tools\\publish.py "что изменилось"
Репозиторий: https://github.com/Iturup1606/murlyka-site (публичный, Pages из ветки main, корень).
Сайт:        https://iturup1606.github.io/murlyka-site/  и  .../privacy
Коммиты в публичном репозитории идут от адреса GitHub noreply: личная почта из git D:\\RuStore туда не попадает.
_site_pages - зеркало: всё, чего нет в _site (кроме .git), из него убирается при каждой публикации.
"""
import shutil
import subprocess
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parents[1]
PAGES = SITE.parent / "_site_pages"
REMOTE = "https://github.com/Iturup1606/murlyka-site.git"
AUTHOR = ("Iturup1606", "115628067+Iturup1606@users.noreply.github.com")
SKIP = {"shots", ".git", "__pycache__"}
# на случай если в _site когда-нибудь окажется лишнее: такие файлы не публикуем
FORBIDDEN = (".env", ".p12", ".jks", ".keystore", ".pem")


def git(*args: str) -> str:
    r = subprocess.run(["git", "-C", str(PAGES), *args], capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        sys.exit(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()


def sources() -> dict[Path, Path]:
    out = {}
    for p in SITE.rglob("*"):
        rel = p.relative_to(SITE)
        if p.is_file() and not (set(rel.parts) & SKIP):
            if p.name.lower().endswith(FORBIDDEN):
                sys.exit(f"в _site лежит {rel}: такие файлы не публикуются, уберите его")
            out[rel] = p
    return out


def main() -> None:
    message = sys.argv[1] if len(sys.argv) > 1 else "Обновление сайта"
    if not (PAGES / ".git").exists():
        PAGES.mkdir(exist_ok=True)
        subprocess.run(["git", "init", "-b", "main", str(PAGES)], check=True, capture_output=True)
        git("remote", "add", "origin", REMOTE)
    git("config", "user.name", AUTHOR[0])
    git("config", "user.email", AUTHOR[1])

    src = sources()
    for p in sorted(PAGES.rglob("*"), reverse=True):
        rel = p.relative_to(PAGES)
        if rel.parts[0] == ".git":
            continue
        if p.is_file() and rel not in src:
            p.unlink()
        elif p.is_dir() and not any(p.iterdir()):
            p.rmdir()
    for rel, p in src.items():
        dst = PAGES / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dst)

    git("add", "-A")
    if not git("status", "--porcelain"):
        print("Изменений нет, публиковать нечего")
        return
    git("commit", "-m", message)
    git("push", "-u", "origin", "main")
    print("Опубликовано:", git("log", "-1", "--format=%h %s"))


if __name__ == "__main__":
    main()

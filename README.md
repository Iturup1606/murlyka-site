# Сайт серии «Мурлыка»

Сайт серии детских обучающих приложений «Мурлыка» для Android: для регистрации компании в RuStore Консоли, поля
«Веб сайт» в карточке приложения и для родителей. Статика без сборки: HTML, CSS, немного JS. Хостинг - GitHub Pages.

| Адрес | Что | Файл |
|---|---|---|
| https://murlyka-kids.ru/ | главная: котик, первое приложение, родителям, контакты | `index.html` |
| https://murlyka-kids.ru/privacy | политика конфиденциальности приложений серии (адрес для RuStore) | `privacy/index.html` |

Разработчик: ООО «МК», ИНН 3808302760. Почта: tokoa436@gmail.com.

## Устройство
- Домен murlyka-kids.ru (регистратор и DNS - SpaceWeb): 4 записи A на `185.199.108.153`, `185.199.109.153`,
  `185.199.110.153`, `185.199.111.153` и CNAME `www` на `iturup1606.github.io`. Файл `CNAME` в корне сайта держит
  домен в Pages, его не удалять. HTTPS обязательный, сертификат выдан 19.10.2026, GitHub продлевает его сам.
- Пути относительные. `/privacy` открывается без `.html`, потому что это папка `privacy` с `index.html`
  (Pages перенаправляет `/privacy` на `/privacy/`).
- `assets/site.css` - все стили; цвета и шрифт из приложения (`uchim-vremya/app/lib/app_style.dart`):
  бирюзовый `#13A196`, малиновый `#D12E6A`, сливовый текст `#3A1830`, розовый фон `#FFF0F4`.
- `assets/site.js` - появление блоков при прокрутке и котик: машет лапкой при загрузке, по нажатию прыгает и говорит.
- Котик - SVG прямо в `index.html`, перенос `CatPainter` из `_shared/packages/kids_core/lib/src/characters.dart`
  (те же координаты 200 x 220 и цвета). Части и анимации: `assets/cat.svg.txt`.
- `assets/fonts` - Balsamiq Sans (шрифт приложения, лицензия OFL в `OFL.txt`), WOFF с кириллицей и латиницей.
- `assets/img` - три скриншота из `uchim-vremya/store/screenshots` (webp 540 px) и иконки из `icon_512.png`.
- `.nojekyll` - Pages отдаёт файлы как есть, без обработки Jekyll.

## Как обновить (на компьютере владельца, папка D:\RuStore\_site)
1. Ресурсы из приложения (после новых скриншотов или иконки): `py -3.12 D:\RuStore\_site\tools\build_assets.py`
2. Скриншоты 1440 / 820 / 390 и проверки (горизонтальный скролл, консоль, шрифт, картинки):
   `py -3.12 D:\RuStore\_site\tools\shots.py` -> `_site\shots` (в git и на сайт не попадает).
   По опубликованному адресу: `py -3.12 D:\RuStore\_site\tools\shots.py --url https://murlyka-kids.ru --tag live`
3. Тексты перед публикацией: `py -3.12 D:\RuStore\_site\tools\extract_text.py D:\Tools\ru-humanizer\work`, затем
   скилл `humanizer-ru-check` (19.10.2026: главная 76.3, политика 72.0, ПРОШЁЛ).
4. Публикация: `py -3.12 D:\RuStore\_site\tools\publish.py "что изменилось"`. Скрипт копирует `_site` в
   `D:\RuStore\_site_pages` (отдельный git) и отправляет в https://github.com/Iturup1606/murlyka-site, ветка `main`.
   Pages обновляется за 1-2 минуты.

## Ссылка из приложения
В приложении ссылки нет и не нужно: в карточке для малышей ссылки на внешние сайты в описании запрещены
(`_shared/RUSTORE.md`, п. 3.2, 9.7). Адрес сайта идёт только в поле контакта «Веб сайт» и в поле политики
конфиденциальности в Консоли RuStore.

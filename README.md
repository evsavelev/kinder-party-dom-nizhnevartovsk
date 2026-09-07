# Киндер Пати Дом — Нижневартовск

Отдельный статический коммерческий демонстрационный сайт.

- Сайт: https://evsavelev.github.io/kinder-party-dom-nizhnevartovsk/
- Репозиторий: https://github.com/evsavelev/kinder-party-dom-nizhnevartovsk

## Устройство

HTML, CSS и небольшой vanilla JS. Нет UI-фреймворков, базы данных, внешних шрифтов, трекеров и серверной формы. Содержание и ссылки доступны без JS; JS добавляет мобильное меню и просмотр фото. WhatsApp открывает подготовленное сообщение, которое посетитель сам отправляет.

`tools/build.mjs` — текст, программы, FAQ, schema и генерация `index.html`; `assets/styles.css` — оформление; `assets/app.js` — взаимодействие; `assets/images` — локальные фото. Для правки текста редактируйте build.mjs, затем запускайте сборку. Копия index.html в корне позволяет открыть статический сайт без Node.

## Локальная работа

```powershell
npm.cmd ci
npm.cmd run build
python -m http.server 4174 --bind 127.0.0.1
```

Откройте http://127.0.0.1:4174/. Только dev-зависимость `@playwright/test`. Для тестов нужен установленный Google Chrome (channel: chrome).

```powershell
npm.cmd test
npm.cmd run qa
```

QA снимки и машинный отчёт пишутся в игнорируемую `.research/qa`. Для проверки публикации задайте `$env:QA_URL = 'https://evsavelev.github.io/kinder-party-dom-nizhnevartovsk/'`. Production не содержит инструментов и документации: workflow публикует только `dist/`.

## Публикация

Push в main запускает `.github/workflows/pages.yml`: сборка → Pages artifact → deploy. История начата с checkpoint до реализации, работа велась в `feat/kinder-party-site`, затем сливается в main. Откат — обычный revert нужного коммита и push main, без удаления истории.

## Документы

- [DESIGN.md](DESIGN.md) — исследование, выбранная система и критерии визуальной проверки.
- [source-notes.md](source-notes.md) — источники, конфликты данных и ограничения.
- [TODO_DATA.md](TODO_DATA.md) — что подтвердить для официального запуска.
- [QA.md](QA.md) — воспроизводимые проверки и redteam.
- [assets/media-manifest.json](assets/media-manifest.json) — происхождение каждого фото.

Фотографии/название/логотип принадлежат соответствующим правообладателям; репозиторий не предоставляет свободную лицензию на их повторное использование. Лицензия шрифта находится рядом с ним.

## SEO

Одна содержательная посадочная страница без искусственных дублей по ключевым словам. Title/description, canonical, OG, sitemap, robots-файл, EntertainmentBusiness и FAQPage. Schema описывает только видимый контент; fake ratings отсутствуют. На GitHub Pages файл robots.txt проекта расположен в подпапке: корневой robots.txt домена github.io из этого репозитория не управляется. Индексация и позиции не гарантируются; в Search Console данные не проверялись.

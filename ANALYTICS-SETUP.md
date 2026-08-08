# Подключение аналитики и вебмастеров (бесплатно)

> Сайт сейчас живёт на GitHub Pages: `https://horelkinai.github.io/` (канонический домен `https://neoprosistem.by/` — подключится позже). Адрес для Метрики/вебмастеров можно указывать любой из них.

## 1. Яндекс.Метрика
1. Заведите счётчик: https://metrika.yandex.ru/ (нужен аккаунт Яндекса).
2. Вставьте сниппет ниже **перед закрывающим `</head>`** в `index.html` (и, при желании, во все страницы — тогда лучше через общий шаблон), заменив `XXXXXXXXXX` на номер счётчика:

```html
<!-- Yandex.Metrika counter -->
<script type="text/javascript">
   (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
   m[i].l=1*new Date();
   for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
   k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
   (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

   ym(XXXXXXXXXX, "init", {
        clickmap:true,
        trackLinks:true,
        accurateTrackBounce:true,
        webvisor:true
   });
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/XXXXXXXXXX" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->
```

## 2. Google Analytics 4
1. Создайте поток данных GA4: https://analytics.google.com/ (аккаунт Google) → Админ → Потоки данных → Добавить поток (Web, адрес `https://neoprosistem.by`).
2. Вставьте сниппет **перед `</head>`**, заменив `G-XXXXXXXXXX` на свой ID:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

## 3. Google Search Console
1. https://search.google.com/search-console → **Добавить ресурс** → тип **Префикс URL** → `https://horelkinai.github.io/` (сейчас сайт живёт там; когда подключите `neoprosistem.by` — добавьте и его как второй ресурс или тип «Домен»).
2. Подтверждение — проще всего **HTML-файл**: Google покажет файл вида `google1234567890.html` со строкой `google-site-verification: google1234567890.html`. Положите этот файл в корень репозитория (рядом с `index.html`) и запушите — он появится на сайте по адресу `https://horelkinai.github.io/google1234567890.html`. Кодекс может положить файл сам, если прислать токен.
   - Альтернатива для домена: DNS-запись TXT (когда появится доступ к DNS `neoprosistem.by`).
3. После подтверждения отправьте карту сайта: `https://horelkinai.github.io/sitemap.xml` (после подключения домена — `https://neoprosistem.by/sitemap.xml`).

## 4. Яндекс.Вебмастер
1. https://webmaster.yandex.ru/ → **Добавить сайт**: `https://horelkinai.github.io/` (пока нет своего домена; потом добавьте `https://neoprosistem.by/`).
2. Подтверждение: **HTML-файл** (Вебмастер выдаст `yandex_XXXXXXXX.html` — положить в корень репозитория и запушить) или **мета-тег** `<meta name="yandex-verification" content="XXXX" />` (вставить в `<head>` — можно попросить Кодекса).
3. Отправьте карту сайта `https://horelkinai.github.io/sitemap.xml`.
4. Раздел «Подбор запросов» → соберите семантику и добавьте в «Список запросов» для отслеживания.

## 5. Проверка скорости
- https://pagespeed.web.dev/ (укажите `https://neoprosistem.by/`).
- Основные требования уже выполнены в коде: прелоад LCP-фото, `fetchpriority=high`, `loading="lazy"` на второстепенных картинках, оптимизированные изображения (логотип 33 КБ, og-image.jpg 83 КБ), `display=swap` для шрифтов, один CSS и один JS.

## 6. Локальные карточки и каталоги (вручную, бесплатно)
- Яндекс.Бизнес: https://business.yandex.ru/ — заполнить карточку компании (Минск, телефоны, сайт).
- Google Business Profile: https://business.google.com/ — то же самое.
- Каталоги: 2GIS, Яндекс.Карты, Google Maps, региональные справочники (спрашивайте — подскажу список под вашу нишу).

## Важно
- НЕ использовать чёрные методы SEO (накрутка, массовый дешёвый ИИ-контент) — риск бана в 2026 году высокий.
- Первые результаты ожидайте через 6–12 месяцев при регулярной работе 10–15 часов в неделю.

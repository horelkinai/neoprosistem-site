# -*- coding: utf-8 -*-
import json, re
from pathlib import Path

root = Path('.')
index_path = root / 'index.html'
html = index_path.read_text(encoding='utf-8')

DOMAIN = 'https://neoprosistem.by'

faq = [
    ("Что такое бизнес-инженерия?",
     "Бизнес-инженерия — это когда мы разбираем ваш бизнес как сложный механизм: находим детали, которые тормозят движение, настраиваем или заменяем их, чтобы вся система заработала с новой мощностью. Мы не даём советы, мы строим систему и остаёмся, пока не будет результата."),
    ("Чем бизнес-инженер отличается от консультанта?",
     "Консультант даёт рекомендации, продаёт отчёты, берёт деньги за процесс и исчезает после сдачи проекта. Бизнес-инженер строит систему и остаётся до результата: отвечает за рост выручки и пропускную способность операционки, а не за красивую презентацию."),
    ("Сколько стоит первая диагностика?",
     "Бесплатно. За 48 часов мы находим три узких места, где ваш бизнес прямо сейчас теряет деньги и время, и отдаём план действий: отчёт по системным ошибкам, инструмент визуального контроля задач, сводную таблицу цен и пошаговые правки. Без доступа к вашим счетам."),
    ("За какое время бизнес начинает расти?",
     "В среднем выручка наших клиентов растёт в 2 раза за первые 90 дней (модель масштабирования ×2–×5). Это не магия и не везение, а результат выстроенной системы: маркетинг окупается, операционка работает без сбоев, команда растёт без микроменеджмента."),
    ("Что входит в цифровой рентген бизнеса?",
     "5 PDF-отчётов (разведка, техплан, смыслы, финансы, партнёры), информация «Матрица прорыва» — чертёж на А1, математика прибыли с реальной контент-экономикой и action-план на 7 дней. Стоимость — 1 000 BYN / 45 000 руб., окупается на первой неделе."),
    ("Сколько часов в неделю сэкономит система?",
     "Не менее 20 часов в неделю: целый рабочий день директора, который раньше уходил в рутину и микроменеджмент. Система ведёт показатели, задачи и маркетинг без вашего круглосуточного присутствия."),
    ("С какими бизнесами и в каких регионах вы работаете?",
     "Мы работаем с владельцами производственного и операционного бизнеса в Беларуси и ближних регионах России. У нас 30 лет производственной практики — мы знаем, сколько стоит час простоя станка. Контакты: +375 29 108-88-90 (BY), +7 910 334-78-51 (RU)."),
    ("Что значит «управление без вашего присутствия»?",
     "Это подключённое управление в абонентском режиме: LIGHT «Смотритель» (контроль показателей, задач, SMM), СТАНДАРТ «Директор» (отдел внешнего маркетинга, трафика, юридическое сопровождение, P&L) и ПРЕМИУМ «Империя» (полный контур — финансы, найм, регламенты, стратегия)."),
]

title = "Бизнес-инженерия — NEO PRO SISTEM | Беларусь, Россия"
description = ("Строим бизнес-системы, а не продаём советы. Бесплатная диагностика за 48 часов, "
               "рост выручки ×2–×5 и бизнес на автопилоте. Беларусь и Россия.")
og_title = "Бизнес-инженерия для предпринимателей — NEO PRO SISTEM | Беларусь, Россия"


def contact(tel, area):
    return {"@type": "ContactPoint", "telephone": tel, "contactType": "sales",
            "areaServed": area, "availableLanguage": "Russian"}


ld_graph = [
    {"@type": "Organization", "@id": DOMAIN + "/#organization",
     "name": "NEO PRO SISTEM", "url": DOMAIN + "/", "logo": DOMAIN + "/favicon.svg",
     "description": "Бизнес-инженерия для предпринимателей Беларуси и России: строим бизнес-системы, а не продаём советы.",
     "address": {"@type": "PostalAddress", "addressCountry": "BY"},
     "areaServed": ["BY", "RU"],
     "telephone": ["+375 29 108-88-90", "+7 910 334-78-51"],
     "sameAs": ["https://t.me/ukol_off", "https://www.instagram.com/neoprosistem/", "https://neoteh.by/"],
     "contactPoint": [contact("+375 29 108-88-90", "BY"), contact("+7 910 334-78-51", "RU")]},
    {"@type": "WebSite", "@id": DOMAIN + "/#website", "url": DOMAIN + "/",
     "name": "NEO PRO SISTEM — бизнес-инженерия", "inLanguage": "ru",
     "publisher": {"@id": DOMAIN + "/#organization"}},
    {"@type": "ProfessionalService", "@id": DOMAIN + "/#service",
     "name": "NEO PRO SISTEM — бизнес-инженерия",
     "url": DOMAIN + "/", "image": DOMAIN + "/og-image.jpg",
     "description": description, "priceRange": "0–450 000 руб/мес",
     "areaServed": ["BY", "RU"], "telephone": "+375 29 108-88-90",
     "parentOrganization": {"@id": DOMAIN + "/#organization"},
     "makesOffer": [
         {"@type": "Offer", "name": "Бесплатная диагностика за 48 часов", "price": "0", "priceCurrency": "BYN"},
         {"@type": "Offer", "name": "Цифровой рентген бизнеса", "price": "1000", "priceCurrency": "BYN"},
         {"@type": "Offer", "name": "Инженерия роста", "price": "4200", "priceCurrency": "BYN"}]},
    {"@type": "FAQPage", "@id": DOMAIN + "/#faq", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faq]},
]
head_ld = json.dumps({"@context": "https://schema.org", "@graph": ld_graph},
                     ensure_ascii=False, indent=2)

head = """<!DOCTYPE html>
<html lang="ru">
<head>
\t<meta charset="UTF-8">
\t<meta name="viewport" content="width=device-width, initial-scale=1">
\t<title>{title}</title>
\t<meta name="description" content="{description}">
\t<meta name="robots" content="index, follow, max-image-preview:large">
\t<meta name="author" content="NEO PRO SISTEM">
\t<link rel="canonical" href="{domain}/">
\t<meta name="geo.region" content="BY-MI">
\t<meta name="geo.placename" content="Минск">
\t<meta name="theme-color" content="#009D9E">
\t<meta name="format-detection" content="telephone=yes">

\t<meta property="og:type" content="website">
\t<meta property="og:site_name" content="NEO PRO SISTEM">
\t<meta property="og:locale" content="ru_RU">
\t<meta property="og:title" content="{og_title}">
\t<meta property="og:description" content="{description}">
\t<meta property="og:url" content="{domain}/">
\t<meta property="og:image" content="{domain}/og-image.jpg">
\t<meta property="og:image:width" content="1200">
\t<meta property="og:image:height" content="630">
\t<meta property="og:image:alt" content="NEO PRO SISTEM — бизнес-инженерия для предпринимателей">

\t<meta name="twitter:card" content="summary_large_image">
\t<meta name="twitter:site" content="@neoprosistem">
\t<meta name="twitter:title" content="{og_title}">
\t<meta name="twitter:description" content="{description}">
\t<meta name="twitter:image" content="{domain}/og-image.jpg">

\t<link rel="icon" href="favicon.svg" type="image/svg+xml">

\t<link rel="preconnect" href="https://fonts.googleapis.com">
\t<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
\t<link href="https://fonts.googleapis.com/css2?family=Titillium+Web:wght@400;600;700;900&family=Roboto:wght@300;400;500;700&family=Oswald:wght@500;700&display=swap" rel="stylesheet">
\t<link rel="stylesheet" href="css/styles.css">

\t<script type="application/ld+json">
{head_ld}
\t</script>
</head>""".format(title=title, description=description, og_title=og_title,
                 domain=DOMAIN, head_ld=head_ld)

html = re.sub(r'<head>.*?</head>', head, html, count=1, flags=re.DOTALL)

faq_items = "\n".join(
    '\t\t\t\t<details class="faq-item"{open}>\n'
    '\t\t\t\t\t<summary><span>{q}</span><span class="faq-icon"></span></summary>\n'
    '\t\t\t\t\t<p>{a}</p>\n'
    '\t\t\t\t</details>'.format(open=' open' if i == 0 else '', q=q, a=a)
    for i, (q, a) in enumerate(faq))

faq_section = """\t<!-- ======= FAQ ======= -->
\t<section class="section section-faq" id="faq">
\t\t<div class="container">
\t\t\t<div class="section-title">
\t\t\t\t<span class="section-kicker">Частые вопросы</span>
\t\t\t\t<h2>Вопросы и ответы</h2>
\t\t\t\t<p>Всё, что вы хотели знать о бизнес-инженерии — коротко и по делу.</p>
\t\t\t</div>
\t\t\t<div class="faq-list">
{faq_items}
\t\t\t</div>
\t\t\t<div class="faq-cta">
\t\t\t\t<p>Не нашли ответ? Напишите нам — подскажем, с чего начать именно вам.</p>
\t\t\t\t<a href="#contacts" class="button button-primary">Задать вопрос</a>
\t\t\t</div>
\t\t</div>
\t</section>

""".format(faq_items=faq_items)

anchor = "\t<!-- ======= CONTACTS ======= -->"
assert anchor in html, "CONTACTS anchor not found"
html = html.replace(anchor, faq_section + anchor, 1)

index_path.write_text(html, encoding='utf-8')

(root / 'robots.txt').write_text(
    "User-agent: *\nAllow: /\n\nSitemap: {0}/sitemap.xml\n".format(DOMAIN),
    encoding='utf-8')

(root / 'sitemap.xml').write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    '  <url>\n'
    '    <loc>{0}/</loc>\n'
    '    <lastmod>2026-08-07</lastmod>\n'
    '    <changefreq>monthly</changefreq>\n'
    '    <priority>1.0</priority>\n'
    '  </url>\n'
    '</urlset>\n'.format(DOMAIN),
    encoding='utf-8')

(root / 'favicon.svg').write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">\n'
    '  <rect width="64" height="64" rx="14" fill="#009D9E"/>\n'
    '  <text x="32" y="42" font-family="Arial, sans-serif" font-size="26" '
    'font-weight="700" fill="#ffffff" text-anchor="middle">NEO</text>\n'
    '</svg>\n',
    encoding='utf-8')

print("OK applied. FAQ items:", len(faq))
print("index.html size:", len(html))

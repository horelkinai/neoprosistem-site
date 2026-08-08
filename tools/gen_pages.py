# -*- coding: utf-8 -*-
"""
Генератор подстраниц из секций index.html.
Запуск: python3 tools/gen_pages.py  (из корня проекта)
"""
import re
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'index.html')

BASE = 'https://neoprosistem.by'

s = open(SRC, encoding='utf-8').read()

# --- разбор index.html ---
head, rest = s.split('</head>', 1)
head += '</head>'
topbar, rest = rest.split('<!-- ======= HEADER ======= -->', 1)
topbar = topbar.replace('<body>', '', 1)
header, rest = rest.split('<main>', 1)
main_inner, rest = rest.split('</main>', 1)
footer_part = rest

sections = {}
for m in re.finditer(r'<!-- ======= ([A-Z0-9 ]+) ======= -->(.*?)(?=<!-- ======= |\n\t*</main>|\Z)', main_inner, re.S):
    sections[m.group(1).strip()] = m.group(0)

NAV = [
    ('index.html', 'Главная'),
    ('method.html', 'Метод'),
    ('services.html', 'Направления'),
    ('stages.html', 'Этапы и цены'),
    ('contacts.html', 'Контакты'),
]

def build_nav(active_file):
    links = []
    for href, label in NAV:
        cls = ' class="active" aria-current="page"' if href == active_file else ''
        links.append(f'\t\t\t<a href="{href}"{cls}>{label}</a>')
    return ('\t\t<nav class="main-nav" id="mainNav">\n'
            + '\n'.join(links)
            + '\n\t\t</nav>')

def patch_head(active_file, title, desc):
    h = head
    h = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', h, count=1, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', h, count=1)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{BASE}/{active_file}">', h, count=1)
    h = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{BASE}/{active_file}">', h, count=1)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', h, count=1)
    h = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title}">', h, count=1)
    h = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{desc}">', h, count=1)

    jsonld = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "Organization",
      "@id": "{BASE}/#organization",
      "name": "NEO PRO SISTEM",
      "url": "{BASE}/",
      "logo": "{BASE}/favicon.svg",
      "description": "Бизнес-инженерия для предпринимателей Беларуси и России: строим бизнес-системы, а не продаём советы.",
      "telephone": ["+375 29 108-88-90", "+7 910 334-78-51"],
      "sameAs": ["https://t.me/ukol_off", "https://www.instagram.com/neoprosistem/", "https://neoteh.by/"]
    }},
    {{
      "@type": "WebPage",
      "@id": "{BASE}/{active_file}#webpage",
      "url": "{BASE}/{active_file}",
      "name": "{title}",
      "description": "{desc}",
      "inLanguage": "ru",
      "isPartOf": {{ "@id": "{BASE}/#website" }}
    }},
    {{
      "@type": "WebSite",
      "@id": "{BASE}/#website",
      "url": "{BASE}/",
      "name": "NEO PRO SISTEM — бизнес-инженерия",
      "inLanguage": "ru",
      "publisher": {{ "@id": "{BASE}/#organization" }}
    }}
  ]
}}
</script>'''
    h = re.sub(r'<script type="application/ld\+json">.*?</script>', jsonld, h, count=1, flags=re.S)
    return h

def page_hero(crumb, title_html, lead):
    return f'''	<!-- ======= PAGE HERO ======= -->
	<section class="page-hero" id="top">
		<div class="container">
			<div class="breadcrumbs"><a href="index.html">Главная</a><span>→</span><span>{crumb}</span></div>
			<h1>{title_html}</h1>
			<p class="lead">{lead}</p>
			<div class="page-hero-cta">
				<a href="#diagnostics" class="button button-accent">Бесплатная диагностика за 48 часов</a>
			</div>
		</div>
	</section>
'''

PAGES = [
    {
        'file': 'method.html',
        'crumb': 'Метод',
        'title': 'Метод бизнес-инженерии — NEO PRO SISTEM',
        'desc': 'Как мы разбираем бизнес как систему: разбор, настройка, рост ×2–×5 и автопилот. 4 этапа, бесплатная диагностика за 48 часов.',
        'hero': page_hero('Метод',
            'Разбираем бизнес, <em>как сложный механизм</em>',
            'Не консалтинг и не советы — инженерный подход: находим детали, которые тормозят движение, настраиваем или заменяем их, чтобы вся система заработала с новой мощностью.'),
        'sections': ['METHOD', 'VS', 'STAGES', 'TARIFFS', 'DIAGNOSTICS'],
    },
    {
        'file': 'services.html',
        'crumb': 'Направления',
        'title': 'Направления работы — NEO PRO SISTEM | 6 блоков бизнес-системы',
        'desc': 'Бренд-магнит, маркетинг, контент, операционка, команда и масштабирование ×2–×5. Полный контур бизнес-системы под ключ.',
        'hero': page_hero('Направления',
            '6 направлений, <em>полный контур системы</em>',
            'От бренда и маркетинга до операционки и масштабирования. Каждое направление настраивается как часть единой бизнес-машины — без разрозненных «фиксеров».'),
        'sections': ['DIRECTIONS', 'RESULTS', 'DIAGNOSTICS'],
    },
    {
        'file': 'stages.html',
        'crumb': 'Этапы и цены',
        'title': 'Этапы и тарифы — NEO PRO SISTEM | Цены в BYN и рублях',
        'desc': 'Путь из точки А в точку Б: бесплатная диагностика за 48 часов, цифровой рентген от 1 000 BYN, инженерия роста от 4 200 BYN и тарифы управления от 1 800 BYN/мес.',
        'hero': page_hero('Этапы и цены',
            'Путь из точки А <em>в точку Б</em>',
            'Четыре понятных этапа — от бесплатной диагностики до бизнеса на автопилоте. Цены в BYN и рублях, переключатель валют прямо на странице.'),
        'sections': ['STAGES', 'TARIFFS', 'DIAGNOSTICS'],
    },
    {
        'file': 'contacts.html',
        'crumb': 'Контакты',
        'title': 'Контакты — NEO PRO SISTEM | Беларусь, Россия',
        'desc': 'Свяжитесь с нами: Telegram @ukol_off, +375 29 108-88-90 (BY), +7 910 334-78-51 (RU), Instagram @neoprosistem. Бесплатная диагностика за 48 часов.',
        'hero': page_hero('Контакты',
            'Начните <em>с бесплатной диагностики</em>',
            'За 48 часов вы получите план действий: три узких места, которые тормозят рост, отчёт по системным ошибкам и пошаговые правки. 0 руб.'),
        'sections': ['CONTACTS', 'FAQ', 'DIAGNOSTICS'],
    },
]

for page in PAGES:
    h = patch_head(page['file'], page['title'], page['desc'])
    nav = build_nav(page['file'])
    header_patched = re.sub(r'\t\t<nav class="main-nav" id="mainNav">.*?</nav>', nav, header, count=1, flags=re.S)

    body = (topbar + header_patched + '\n<main>\n'
            + page['hero'] + '\n'
            + '\n'.join(sections[k] for k in page['sections'])
            + '\n</main>\n\n' + footer_part)

    out = h + '\n<body>\n\n' + body
    outpath = os.path.join(ROOT, page['file'])
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(out)
    print('written:', page['file'], len(out), 'bytes')

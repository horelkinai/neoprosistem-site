(function () {
	'use strict';

	/* ---------- Мобильное меню (выезжающая панель) ---------- */
	var burger = document.getElementById('burger');
	var mainNav = document.getElementById('mainNav');

	var navOverlay = document.createElement('div');
	navOverlay.className = 'nav-overlay';
	navOverlay.id = 'navOverlay';
	navOverlay.setAttribute('aria-hidden', 'true');
	document.body.appendChild(navOverlay);

	function setMenu(open) {
		if (!mainNav) return;
		mainNav.classList.toggle('open', open);
		if (burger) {
			burger.classList.toggle('open', open);
			burger.setAttribute('aria-expanded', open ? 'true' : 'false');
		}
		navOverlay.classList.toggle('show', open);
		document.body.classList.toggle('menu-open', open);
	}

	/*
	 * На мобильных панель должна жить в <body>, а не внутри шапки:
	 * backdrop-filter на шапке превращает её в containing block для
	 * position:fixed, из-за чего координаты панели «плывут».
	 */
	function moveNavForMobile() {
		if (!mainNav) return;
		var isMobile = window.innerWidth <= 1024;
		var inBody = mainNav.parentNode === document.body;
		if (isMobile && !inBody) {
			document.body.appendChild(mainNav);
		} else if (!isMobile && inBody) {
			var headerInner = document.querySelector('.header-inner');
			var cta = document.querySelector('.header-cta');
			if (headerInner) {
				if (cta) {
					headerInner.insertBefore(mainNav, cta);
				} else {
					headerInner.appendChild(mainNav);
				}
			}
		}
	}

	/* Панель должна начинаться ровно под фактическим положением шапки */
	function syncDrawer() {
		if (!mainNav) return;
		if (window.innerWidth <= 1024) {
			var header = document.getElementById('siteHeader');
			if (header) {
				var top = header.getBoundingClientRect().top + header.offsetHeight;
				mainNav.style.top = top + 'px';
				mainNav.style.height = 'calc(100dvh - ' + top + 'px)';
			}
		} else {
			mainNav.style.top = '';
			mainNav.style.height = '';
		}
	}

	if (burger && mainNav) {
		burger.addEventListener('click', function () {
			setMenu(!mainNav.classList.contains('open'));
		});

		navOverlay.addEventListener('click', function () {
			setMenu(false);
		});

		document.addEventListener('keydown', function (e) {
			if (e.key === 'Escape' || e.keyCode === 27) {
				setMenu(false);
			}
		});

		mainNav.addEventListener('click', function (e) {
			if (e.target.closest('a')) {
				setMenu(false);
			}
		});

		window.addEventListener('resize', function () {
			if (window.innerWidth > 1024) {
				setMenu(false);
			}
			moveNavForMobile();
			syncDrawer();
		});

		window.addEventListener('scroll', syncDrawer, { passive: true });
		window.addEventListener('load', function () {
			moveNavForMobile();
			syncDrawer();
		});
		moveNavForMobile();
		syncDrawer();
	}

	/* ---------- Переключатель валют ---------- */
	var currencySwitch = document.getElementById('currencySwitch');
	var currencyBtns = currencySwitch ? currencySwitch.querySelectorAll('.cs-btn') : [];
	var prices = document.querySelectorAll('[data-byn][data-rub]');
	var currentCurrency = 'byn';

	function applyCurrency(currency) {
		currentCurrency = currency;
		prices.forEach(function (el) {
			var byn = el.getAttribute('data-byn');
			var rub = el.getAttribute('data-rub');
			el.textContent = currency === 'byn' ? byn : rub;
			el.style.opacity = '0.25';
			setTimeout(function () { el.style.opacity = '1'; }, 150);
		});
		currencyBtns.forEach(function (btn) {
			btn.classList.toggle('active', btn.getAttribute('data-currency') === currency);
		});
	}

	if (currencySwitch) {
		currencyBtns.forEach(function (btn) {
			btn.addEventListener('click', function () {
				applyCurrency(btn.getAttribute('data-currency'));
			});
		});
	}

	/* ---------- Счётчики ---------- */
	function animateCounter(el) {
		var target = parseFloat(el.getAttribute('data-count'));
		if (isNaN(target)) return;
		var suffix = el.getAttribute('data-suffix') || '';
		var duration = 1400;
		var start = null;

		function step(ts) {
			if (!start) start = ts;
			var progress = Math.min((ts - start) / duration, 1);
			var eased = 1 - Math.pow(1 - progress, 3);
			el.textContent = Math.round(target * eased) + suffix;
			if (progress < 1) requestAnimationFrame(step);
		}
		requestAnimationFrame(step);
	}

	/* ---------- Появление при скролле ---------- */
	var revealEls = document.querySelectorAll('.card, .achievement-card, .tariff-card, .stage-card, .contact-card, .method-item, .dir-card');

	if ('IntersectionObserver' in window) {
		var io = new IntersectionObserver(function (entries) {
			entries.forEach(function (entry) {
				if (!entry.isIntersecting) return;
				entry.target.classList.add('in-view');
				io.unobserve(entry.target);
			});
		}, { threshold: 0.12 });

		revealEls.forEach(function (el) {
			el.classList.add('reveal');
			io.observe(el);
		});

		var counterIo = new IntersectionObserver(function (entries) {
			entries.forEach(function (entry) {
				if (!entry.isIntersecting) return;
				var counters = entry.target.querySelectorAll('[data-count]');
				counters.forEach(animateCounter);
				counterIo.unobserve(entry.target);
			});
		}, { threshold: 0.4 });

		var statBlocks = document.querySelectorAll('.hero-stats-inner, .achievements');
		statBlocks.forEach(function (block) { counterIo.observe(block); });
	} else {
		revealEls.forEach(function (el) { el.classList.add('in-view'); });
		document.querySelectorAll('[data-count]').forEach(animateCounter);
	}

	/* ---------- Кнопка «наверх» ---------- */
	var backToTop = document.getElementById('backToTop');

	if (backToTop) {
		window.addEventListener('scroll', function () {
			var show = window.scrollY > 500;
			backToTop.classList.toggle('visible', show);
		}, { passive: true });

		backToTop.addEventListener('click', function () {
			window.scrollTo({ top: 0, behavior: 'smooth' });
		});
	}

	/* ---------- Форма заявки ---------- */
	var form = document.getElementById('diagForm');

	if (form) {
		form.addEventListener('submit', function (e) {
			e.preventDefault();

			var name = form.querySelector('[name="name"]');
			var contact = form.querySelector('[name="contact"]');
			var valid = true;

			[name, contact].forEach(function (input) {
				input.style.borderColor = '';
				if (!input.value.trim()) {
					input.style.borderColor = '#EB4545';
					valid = false;
				}
			});

			if (!valid) {
				var firstInvalid = [name, contact].find(function (i) { return !i.value.trim(); });
				if (firstInvalid) firstInvalid.focus();
				return;
			}

			var data = {
				name: name.value.trim(),
				contact: contact.value.trim(),
				sphere: form.querySelector('[name="sphere"]').value.trim()
			};

			var success = document.getElementById('formSuccess');
			success.hidden = false;
			form.querySelector('button[type="submit"]').disabled = true;
			form.querySelector('button[type="submit"]').textContent = 'Заявка отправлена ✓';

			console.log('Заявка NEO PRO SISTEM:', data);
		});
	}

	/* ---------- Лайтбокс: сертификат ---------- */
	var certLightbox = document.getElementById('certLightbox');
	var openCertBtns = document.querySelectorAll('[data-open-cert]');

	function openLightbox() {
		if (!certLightbox) return;
		certLightbox.hidden = false;
		document.body.classList.add('lightbox-open');
		var closeBtn = certLightbox.querySelector('.lightbox-close');
		if (closeBtn) closeBtn.focus();
	}

	function closeLightbox() {
		if (!certLightbox) return;
		certLightbox.hidden = true;
		document.body.classList.remove('lightbox-open');
	}

	openCertBtns.forEach(function (btn) {
		btn.addEventListener('click', function (e) {
			e.preventDefault();
			openLightbox();
		});
	});

	if (certLightbox) {
		certLightbox.querySelectorAll('[data-cert-close]').forEach(function (el) {
			el.addEventListener('click', closeLightbox);
		});

		document.addEventListener('keydown', function (e) {
			if (e.key === 'Escape' && !certLightbox.hidden) closeLightbox();
		});
	}

	/* ---------- ИИ-ассистент ---------- */
	var aiChat = document.getElementById('aiChat');
	var aiLauncher = document.getElementById('aiChatLauncher');
	var aiWindow = document.getElementById('aiChatWindow');
	var aiBody = document.getElementById('aiChatBody');
	var aiForm = document.getElementById('aiChatForm');
	var aiInput = document.getElementById('aiChatInput');
	var aiClose = document.getElementById('aiChatClose');

	var AI_KB = [
		{
			keys: ['здравств', 'привет', 'добрый день', 'добрый вечер', 'хай', 'hello'],
			answer: 'Здравствуйте! Рад помочь 😊 Спросите про метод, направления, этапы и цены — или нажмите один из вопросов ниже.'
		},
		{
			keys: ['цена', 'цен', 'стоимост', 'стоит', 'тариф', 'сколько', 'бюджет', 'прайс'],
			answer: 'Работаем по прозрачным ценам:<br>• Диагностика за 48 часов — <b>0 руб.</b><br>• Цифровой рентген бизнеса — от <b>1 000 BYN</b><br>• Инженерия роста ×2–×5 — от <b>4 200 BYN</b><br>• Тарифы управления — от <b>1 800 BYN/мес</b><br><br>Подробнее: <a href="stages.html">Этапы и цены</a>.'
		},
		{
			keys: ['бизнес-инженери', 'бизнес инженери', 'бизнес-инженер', 'метод', 'подход', 'что вы делаете', 'в чём суть', 'суть'],
			answer: 'Мы строим бизнес-системы, а не продаём советы. Инженерный подход: разбираем бизнес как механизм, находим детали, которые тормозят движение, и настраиваем их.<br><br>4 этапа: <b>разбор</b> → <b>настройка</b> → <b>рост ×2–×5</b> → <b>автопилот</b>. Подробнее: <a href="method.html">Метод</a>.'
		},
		{
			keys: ['направлен', 'услуг', 'что входит', 'блок', 'бренд', 'маркетинг', 'контент', 'операционк', 'команд', 'масштабир'],
			answer: 'Работаем по 6 блокам бизнес-системы: <b>бренд-магнит, маркетинг, контент, операционка, команда, масштабирование</b>. Каждое направление настраивается как часть единой машины. Подробнее: <a href="services.html">Направления</a>.'
		},
		{
			keys: ['диагностик', 'начать', 'первый шаг', 'как начать', 'с чего начать', 'заявк', 'бесплатн'],
			answer: 'Первый шаг — <b>бесплатная диагностика за 48 часов</b>: найдём три узких места, которые тормозят рост, и дадим план правок за 0 руб. Оставьте заявку: <a href="#diagnostics">Бесплатная диагностика</a>.'
		},
		{
			keys: ['этап', 'срок', 'сколько времени', 'долго', 'график', 'поэтап'],
			answer: 'Идём по 4 этапам: диагностика (48 ч) → цифровой рентген → инженерия роста → управление на автопилоте. Первые результаты обычно видны уже в первые 90 дней — целевой ориентир ×2 к выручке. Подробнее: <a href="stages.html">Этапы и цены</a>.'
		},
		{
			keys: ['контакт', 'связаться', 'телефон', 'позвонить', 'telegram', 'телеграм', 'instagram', 'инстаграм', 'написать', 'мессенджер', 'почта'],
			answer: 'Связаться можно так:<br>• Telegram: <a href="https://t.me/ukol_off" target="_blank" rel="noopener">@ukol_off</a><br>• Instagram: <a href="https://www.instagram.com/neoprosistem/" target="_blank" rel="noopener">@neoprosistem</a><br>• BY: <a href="tel:+375291088890">+375 29 108-88-90</a><br>• RU: <a href="tel:+79103347851">+7 910 334-78-51</a>'
		},
		{
			keys: ['основател', 'василий', 'уколов', 'кто вы', 'эксперт', 'опыт', '30 лет', 'сертификат'],
			answer: 'Основатель — <b>Василий Уколов</b>, бизнес-инженер: 30 лет производственной практики + технологии управления 2026 года, сертифицированный участник конференции «Цифровые решения для бизнеса» • 2026.'
		},
		{
			keys: ['результат', 'выручк', 'рост', 'прибыл', 'эффект', 'сколько заработаю', 'гарант'],
			answer: 'Ориентиры по системе: <b>×2 к выручке за 90 дней</b>, +20 часов директору в неделю, бизнес работает без вашего круглосуточного участия. Результаты зависят от состояния системы — диагностика покажет узкие места.'
		},
		{
			keys: ['спасибо', 'благодар', 'отлично', 'понятно', 'пока', 'до свидания'],
			answer: 'Всегда пожалуйста! 😊 Если появятся вопросы — напишите в Telegram <a href="https://t.me/ukol_off" target="_blank" rel="noopener">@ukol_off</a> или оставьте заявку на <a href="#diagnostics">диагностику</a>.'
		}
	];

	var AI_FALLBACK = 'Не нашёл точного ответа на этот вопрос 🤔 Лучше всего уточнить напрямую: Telegram <a href="https://t.me/ukol_off" target="_blank" rel="noopener">@ukol_off</a> или <a href="tel:+375291088890">+375 29 108-88-90</a>. А я могу рассказать о методе, направлениях и ценах!';

	function normalize(q) {
		return q.toLowerCase().replace(/ё/g, 'е').replace(/[^а-яёa-z0-9\s\-+@]/gi, ' ').replace(/\s+/g, ' ').trim();
	}

	function findAnswer(q) {
		var nq = normalize(q);
		for (var i = 0; i < AI_KB.length; i++) {
			for (var k = 0; k < AI_KB[i].keys.length; k++) {
				if (nq.indexOf(normalize(AI_KB[i].keys[k])) !== -1) {
					return AI_KB[i].answer;
				}
			}
		}
		return AI_FALLBACK;
	}

	function aiScrollBottom() {
		if (aiBody) aiBody.scrollTop = aiBody.scrollHeight;
	}

	function aiAddMsg(text, who) {
		if (!aiBody) return;
		var msg = document.createElement('div');
		msg.className = 'ai-msg ai-msg-' + who;
		msg.innerHTML = text;
		aiBody.appendChild(msg);
		aiScrollBottom();
	}

	function aiShowTyping() {
		var el = document.createElement('div');
		el.className = 'ai-msg ai-msg-bot ai-typing';
		el.innerHTML = '<span></span><span></span><span></span>';
		if (aiBody) aiBody.appendChild(el);
		aiScrollBottom();
		return el;
	}

	function aiSend(text) {
		if (!text.trim()) return;
		aiAddMsg(text, 'user');
		var chips = aiBody ? aiBody.querySelector('.ai-chips') : null;
		if (chips) chips.remove();
		var typing = aiShowTyping();
		setTimeout(function () {
			if (typing && typing.parentNode) typing.parentNode.removeChild(typing);
			aiAddMsg(findAnswer(text), 'bot');
		}, 650 + Math.random() * 500);
	}

	function aiSetOpen(open) {
		if (aiLauncher) {
			aiLauncher.classList.toggle('open', open);
			aiLauncher.setAttribute('aria-expanded', open ? 'true' : 'false');
			aiLauncher.setAttribute('aria-label', open ? 'Закрыть чат с ИИ-ассистентом' : 'Открыть чат с ИИ-ассистентом');
		}
		if (aiWindow) {
			aiWindow.classList.toggle('open', open);
			aiWindow.setAttribute('aria-hidden', open ? 'false' : 'true');
		}
		if (open && aiInput) {
			setTimeout(function () { aiInput.focus(); }, 120);
		}
	}

	if (aiLauncher) {
		aiLauncher.addEventListener('click', function () {
			aiSetOpen(!(aiWindow && aiWindow.classList.contains('open')));
		});
	}

	if (aiClose) {
		aiClose.addEventListener('click', function () {
			aiSetOpen(false);
		});
	}

	if (aiForm) {
		aiForm.addEventListener('submit', function (e) {
			e.preventDefault();
			if (!aiInput) return;
			var q = aiInput.value;
			aiInput.value = '';
			aiSend(q);
		});
	}

	if (aiBody) {
		aiBody.addEventListener('click', function (e) {
			var chip = e.target.closest('.ai-chip');
			if (chip) {
				aiSend(chip.getAttribute('data-q'));
			}
		});
	}

	document.addEventListener('keydown', function (e) {
		if ((e.key === 'Escape' || e.keyCode === 27) && aiWindow && aiWindow.classList.contains('open')) {
			aiSetOpen(false);
		}
	});
})();

/* Слайд-шоу фото основателя: показываем по очереди, останавливаемся на последнем */
(function () {
	var slides = document.querySelectorAll('.hero-slide');
	if (slides.length < 2) return;

	var index = 0;
	var timer = setInterval(function () {
		if (index >= slides.length - 1) {
			clearInterval(timer);
			return;
		}
		slides[index].classList.remove('is-active');
		index += 1;
		slides[index].classList.add('is-active');
	}, 3000);
})();

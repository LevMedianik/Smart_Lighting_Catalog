document.addEventListener("DOMContentLoaded", () => {
  console.log("script.js запущен");

  const categoryContainer = document.getElementById("categoryContainer");
  const subcategoryContainer = document.getElementById("subcategoryContainer");
  const fixtureContainer = document.getElementById("fixtureContainer");

  if (!window.fixturesData) {
    console.error("❌ fixturesData не найден");
    return;
  }

  // Маппинг категорий → иконки
  const categoryIcons = {
    "Потолочные": "./assets/lamp.png",
    "Настенные": "./assets/wall-lamp.png",
    "Напольные": "./assets/floor-lamp.png"
  };

  // Рендер категорий
  const renderCategories = () => {
    categoryContainer.innerHTML = "";

    Object.keys(fixturesData).forEach(categoryName => {
      const card = document.createElement("div");
      card.className =
        "relative bg-[#23282b]/90 rounded-3xl p-8 w-72 shadow-xl hover:shadow-2xl transition transform hover:scale-105 cursor-pointer overflow-hidden backdrop-blur-sm text-center category-btn";


      // Эффект глянца
      const gloss = document.createElement("div");
      gloss.className =
        "absolute inset-0 bg-gradient-to-t from-transparent via-white/10 to-transparent opacity-30 rounded-3xl pointer-events-none";
      card.appendChild(gloss);

      // Иконка
      const img = document.createElement("img");
      img.src = categoryIcons[categoryName] || "./assets/img_placeholder.png";
      img.alt = categoryName;
      img.className = "w-16 mx-auto mb-4 opacity-90 relative z-10";
      card.appendChild(img);

      // Название
      const title = document.createElement("h3");
      title.textContent = categoryName;
      title.className = "text-xl font-semibold mb-2 relative z-10";
      card.appendChild(title);

      // Описание
      const desc = document.createElement("p");
      desc.className = "text-sm text-gray-300 relative z-10";
      if (categoryName === "Потолочные")
        desc.textContent = "Панели, линейные и магистральные модели для офисов, залов и коридоров.";
      else if (categoryName === "Настенные")
        desc.textContent = "Компактные решения для акцентного освещения и комфортных интерьеров.";
      else if (categoryName === "Напольные")
        desc.textContent = "Светильники для жилых и общественных пространств, создающие уют и стиль.";
      card.appendChild(desc);

      // Обработчик клика
      card.addEventListener("click", () => {
        // снять подсветку со всех карточек категорий
        document.querySelectorAll(".category-btn").forEach(btn => btn.classList.remove("active-btn"));
        // подсветить текущую
        card.classList.add("active-btn");
        // отрисовать подкатегории выбранной категории
        renderSubcategories(categoryName);
      });


      categoryContainer.appendChild(card);
    });
  };

  // Рендер подкатегорий
  const renderSubcategories = (categoryName) => {
    subcategoryContainer.innerHTML = "";
    fixtureContainer.innerHTML = "";

    const subcategories = Object.keys(fixturesData[categoryName] || {});
    subcategories.forEach(sub => {
      const btn = document.createElement("button");
      btn.className =
        "bg-[#3a3a3a] hover:bg-[#4a4a4a] text-white px-5 py-2 rounded-xl transition subcategory-btn";

      btn.textContent = sub;
      btn.addEventListener("click", () => {
      // снять подсветку со всех подкатегорий
      document.querySelectorAll(".subcategory-btn").forEach(b => b.classList.remove("active-btn"));
      // подсветить выбранную
      btn.classList.add("active-btn");
      // показать светильники
      renderFixtures(categoryName, sub);
    });

      subcategoryContainer.appendChild(btn);
    });
  };

  // Рендер карточек светильников
  const renderFixtures = (categoryName, subcategoryName) => {
    fixtureContainer.innerHTML = "";

    const fixtures = fixturesData[categoryName]?.[subcategoryName] || [];
    fixtures.forEach(item => {
      const card = document.createElement("div");
      card.className =
        "bg-[#2b2b2b] rounded-2xl p-6 shadow-md hover:shadow-lg transition";
      card.innerHTML = `
        <div class="flex items-center gap-4">
          <img src="./assets/img_placeholder.png" alt="fixture" class="w-16 h-16 rounded-lg object-cover">
          <div>
            <h4 class="text-lg font-semibold">${item.бренд}</h4>
            <p class="text-sm text-gray-400">Серия: ${item.серия}</p>
            <p class="text-sm">Мощность: ${item.мощность_вт} Вт
            <p class="text-sm">Световой поток: ${item.световой_поток_лм} лм</p>
            <p class="text-green-400 font-medium">Цена: ${item["цена_₽"]} ₽</p>
          </div>
        </div>
      `;
      fixtureContainer.appendChild(card);
    });
  };

  // Инициализация
  renderCategories();
});

/* ======================= AI-Advisor ======================= */

// открытие/скрытие панели
document.getElementById('openChatBtn')?.addEventListener('click', () => {
  document.getElementById('chatPanel')?.classList.toggle('hidden');
});

document.getElementById('clearChatBtn')?.addEventListener('click', () => clearChatKeepGreeting());

// отправка сообщения
document.getElementById('chatForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();

  const input = document.getElementById('chatInput');
  const text = (input.value || '').trim();
  if (!text) return;

  appendMsg('user', text);
  input.value = '';

  // 1) Парсим текст на параметры RoomInput
  const payload = parseRoomMessage(text);

  // Проверяем наличие ключевых параметров
  const missing = [];
  if (!payload['тип_помещения']) missing.push('тип помещения');
  if (!isFinite(payload['площадь_м2'])) missing.push('площадь (м²)');
  if (!isFinite(payload['высота_м'])) missing.push('высота (м)');
  if (!isFinite(payload['бюджет_₽'])) missing.push('бюджет (₽)');

  if (missing.length) {
    appendMsg(
      'bot',
      `Не хватает данных: <b>${missing.join(', ')}</b>.<br>
      Например: <span class="tip">«офис 45 м², высота 3.2 м, бюджет 20000»</span>.`
    );
    return;
  }

  // 2) POST /chat
  try {
    const res = await fetch('http://127.0.0.1:8000/chat/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }) // ✅ теперь передаём JSON
    });

    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    const data = await res.json();

    // 3) Обрабатываем ответ
    let out = '';
    if (data.summary) out += data.summary.replace(/\n/g, '<br>') + '<br><br>';

    const items = (data.recommendations || []).slice(0, 3);
    if (!items.length) {
      appendMsg('bot', data.advice || 'Рекомендации не найдены. Попробуйте другой запрос.');
      return;
    }

    out += items.map((r, i) => {
      const price =
        typeof r['цена_₽'] !== 'undefined'
          ? formatRub(r['цена_₽'])
          : typeof r['цена_руб'] !== 'undefined'
          ? formatRub(r['цена_руб'])
          : '—';

      return `#${i + 1}. <b>${r['бренд']}</b> ${r['серия'] || ''} — <i>${r['тип_светильника']}</i>, 
              ${(r['мощность_вт'] ?? '—')} Вт, ${(r['световой_поток_лм'] ?? '—')} лм, ≈ ${price}`;
    }).join('<br>');

    if (data.advice) out += `<br><br>${data.advice.replace(/\n/g, '<br>')}`;
    appendMsg('bot', out);

  } catch (err) {
    console.error('Ошибка при запросе к /chat:', err);
    appendMsg('bot', `Ошибка при запросе к <code>/chat</code>: ${err.message}`);
  }
});


// helpers
function appendMsg(side, html){
  const box = document.getElementById('chatMessages');
  const row = document.createElement('div');
  row.className = `chat-msg ${side}`;
  row.innerHTML = `<div class="bubble">${html}</div>`;
  box.appendChild(row);
  box.scrollTop = box.scrollHeight;
}

function clearChatKeepGreeting(){
  const box = document.getElementById('chatMessages');
  const first = box.firstElementChild?.outerHTML || '';
  box.innerHTML = first; // оставляем только приветствие
}

// формат ₽ без поломки кодировки
function formatRub(v){
  const n = Number(v);
  if (!isFinite(n)) return '—';
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 2 }).format(n);
}

/* -------- парсер пользовательского текста (легковесный) --------
   Выцепляем: тип помещения, площадь, высоту, бюджет.
   Остальные поля — дефолты (как в RoomInput / твоём пайплайне).
*/
function parseRoomMessage(text){
  const s = ' ' + (text || '').toLowerCase() + ' ';

  // алиасы типов помещений -> твои ключи в ROOM_RULES
  const ROOM_ALIASES = [
    ['офис', 'офисное помещение'],
    ['торговый зал', 'торговый зал'],
    ['гостиная', 'гостиная'],
    ['кухня', 'кухня домашняя'],
    ['коридор', 'коридор'],
    ['склад', 'склад'],
    ['класс', 'школьный класс'],
    ['аудитория', 'лекционная аудитория'],
    ['санузел', 'санузел'],
    ['серверная', 'серверная'],
    ['конференц', 'конференц зал'],
    ['больница', 'палата больницы'],
  ];
  let room = '';
  for (const [needle, canon] of ROOM_ALIASES) {
    if (s.includes(' ' + needle + ' ')) { room = canon; break; }
  }
  if (!room) {
    // ещё попытка — искать “для офиса/гостиной/…”
    for (const [needle, canon] of ROOM_ALIASES) {
      if (s.includes('для ' + needle + ' ')) { room = canon; break; }
    }
  }

  // площадь (м2, м², “квадратных” и т.п.)
  const areaRe = /(?:\b| )(?:площад[ьи]\s*|квадратн\w*\s*)?(\d+(?:[.,]\d+)?)(?=\s*(?:м2|м²|метр(?:а|ов)?(?:\s*в\s*квадрате)?|кв\.?))?/i;
  const areaM = s.match(areaRe);
  let area = areaM ? parseFloat(areaM[1].replace(',', '.')) : NaN;

  // высота
  const hRe = /(?:высот\w*|потол(?:ок|ки)\s*)(\d+(?:[.,]\d+)?)/i;
  const hM  = s.match(hRe);
  let height = hM ? parseFloat(hM[1].replace(',', '.')) : NaN;

  // бюджет
  const moneyRe = /(?:бюджет\w*|за\s*)(\d[\d\s]*(?:[.,]\d+)?)/i;
  const moneyM  = s.match(moneyRe);
  let budget = NaN;
  if (moneyM) {
    budget = parseFloat(moneyM[1].replace(/\s/g,'').replace(',', '.'));
    // если пользователь написал “20к/20k”
    const kRe = /(\d+(?:[.,]\d+)?)\s*[кk]\b/;
    const kM = s.match(kRe);
    if (!isFinite(budget) && kM) budget = parseFloat(kM[1].replace(',', '.')) * 1000;
  }

  // дефолты (мягкие)
  const payload = {
    'тип_помещения': room || 'офисное помещение',
    'площадь_м2': isFinite(area) ? area : 20,
    'высота_м': isFinite(height) ? height : 3,
    'целевой_люкс': 400,
    'cri_min': 80,
    'cct_предпочтение_k': 4000,
    'ip_min': 40,
    'бюджет_₽': isFinite(budget) ? budget : 100000
  };
  return payload;
}

/* -------- кнопки открытия из шапки/hero -------- */
document.querySelectorAll('[data-open-advisor]').forEach(el=>{
  el.addEventListener('click', (e)=>{
    e.preventDefault();
    document.getElementById('advisor')?.scrollIntoView({behavior:'smooth'});
    const panel = document.getElementById('chatPanel');
    if (panel?.classList.contains('hidden')) panel.classList.remove('hidden');
    document.getElementById('chatInput')?.focus();
  });
});
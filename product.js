(() => {
  const state = { products: [], byId: new Map() };
  const $ = (selector) => document.querySelector(selector);
  const laptopSvg = '<svg viewBox="0 0 120 82" role="img" aria-label="Иконка ноутбука" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="8" width="80" height="53" rx="5" fill="#eef1f7" stroke="#657086" stroke-width="3"/><path d="M14 67h92l8 7H6l8-7Z" fill="#d7dce6" stroke="#657086" stroke-width="3" stroke-linejoin="round"/><path d="M33 22h54v28H33z" fill="#fff" opacity=".8"/><path d="M47 36h26" stroke="#635bff" stroke-width="3" stroke-linecap="round"/></svg>';
  const monoSvg = '<svg viewBox="0 0 120 86" role="img" aria-label="Иконка моноблока" xmlns="http://www.w3.org/2000/svg"><rect x="18" y="7" width="84" height="55" rx="5" fill="#eef1f7" stroke="#657086" stroke-width="3"/><path d="M42 70h36l4 8H38l4-8Z" fill="#d7dce6" stroke="#657086" stroke-width="3" stroke-linejoin="round"/><path d="M31 22h58v28H31z" fill="#fff" opacity=".82"/><circle cx="60" cy="15" r="2" fill="#657086"/><path d="M48 36h24" stroke="#635bff" stroke-width="3" stroke-linecap="round"/></svg>';

  const gpuSvg = '<svg viewBox="0 0 120 86" role="img" aria-label="Иконка видеокарты" xmlns="http://www.w3.org/2000/svg"><rect x="13" y="18" width="94" height="50" rx="5" fill="#eef1f7" stroke="#657086" stroke-width="3"/><circle cx="48" cy="43" r="13" fill="#fff" stroke="#635bff" stroke-width="3"/><circle cx="80" cy="43" r="13" fill="#fff" stroke="#635bff" stroke-width="3"/><path d="M20 29h-8v28h8M99 29h9v28h-9" stroke="#657086" stroke-width="3"/></svg>';
  const cpuSvg = '<svg viewBox="0 0 120 86" role="img" aria-label="Иконка процессора" xmlns="http://www.w3.org/2000/svg"><rect x="29" y="15" width="62" height="56" rx="5" fill="#eef1f7" stroke="#657086" stroke-width="3"/><rect x="43" y="29" width="34" height="28" rx="3" fill="#fff" stroke="#635bff" stroke-width="3"/><path d="M39 8v7M51 8v7M63 8v7M75 8v7M87 8v7M39 71v7M51 71v7M63 71v7M75 71v7M87 71v7M22 25h7M22 37h7M22 49h7M22 61h7M91 25h7M91 37h7M91 49h7M91 61h7" stroke="#657086" stroke-width="3" stroke-linecap="round"/></svg>';
  const ssdSvg = '<svg viewBox="0 0 120 86" role="img" aria-label="Иконка SSD" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="25" width="80" height="36" rx="5" fill="#eef1f7" stroke="#657086" stroke-width="3"/><circle cx="35" cy="43" r="5" fill="#635bff"/><path d="M52 36h35M52 43h24M52 50h29" stroke="#657086" stroke-width="3" stroke-linecap="round"/><path d="M28 18h64" stroke="#635bff" stroke-width="3" stroke-linecap="round"/></svg>';
  const genericSvg = '<svg viewBox="0 0 120 86" role="img" aria-label="Иконка товара" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="16" width="80" height="54" rx="7" fill="#eef1f7" stroke="#657086" stroke-width="3"/><path d="M41 78h38" stroke="#635bff" stroke-width="4" stroke-linecap="round"/></svg>';
  const caseSvg = '<svg viewBox="0 0 120 86" role="img" aria-label="Иконка корпуса" xmlns="http://www.w3.org/2000/svg"><rect x="31" y="8" width="58" height="70" rx="5" fill="#eef1f7" stroke="#657086" stroke-width="3"/><rect x="42" y="19" width="36" height="31" rx="3" fill="#fff" stroke="#635bff" stroke-width="3"/><circle cx="49" cy="61" r="3" fill="#635bff"/><path d="M60 61h17M60 68h17" stroke="#657086" stroke-width="3" stroke-linecap="round"/></svg>';
  const psuSvg = '<svg viewBox="0 0 120 86" role="img" aria-label="Иконка блока питания" xmlns="http://www.w3.org/2000/svg"><rect x="17" y="20" width="86" height="48" rx="6" fill="#eef1f7" stroke="#657086" stroke-width="3"/><circle cx="48" cy="44" r="15" fill="#fff" stroke="#635bff" stroke-width="3"/><path d="M48 29v30M33 44h30M77 34h16M77 44h16M77 54h10" stroke="#657086" stroke-width="3" stroke-linecap="round"/></svg>';
  const coolingSvg = '<svg viewBox="0 0 120 86" role="img" aria-label="Иконка охлаждения" xmlns="http://www.w3.org/2000/svg"><circle cx="41" cy="43" r="23" fill="#eef1f7" stroke="#657086" stroke-width="3"/><circle cx="41" cy="43" r="6" fill="#fff" stroke="#635bff" stroke-width="3"/><path d="M41 20v17M41 49v17M18 43h17M49 43h17" stroke="#657086" stroke-width="3" stroke-linecap="round"/><rect x="72" y="25" width="26" height="36" rx="3" fill="#fff" stroke="#635bff" stroke-width="3"/><path d="M78 33h14M78 42h14M78 51h14" stroke="#657086" stroke-width="3" stroke-linecap="round"/></svg>';
  const motherboardSvg = '<svg viewBox="0 0 120 86" role="img" aria-label="Иконка материнской платы" xmlns="http://www.w3.org/2000/svg"><rect x="16" y="10" width="88" height="66" rx="5" fill="#eef1f7" stroke="#657086" stroke-width="3"/><rect x="28" y="23" width="24" height="24" rx="3" fill="#fff" stroke="#635bff" stroke-width="3"/><path d="M63 20h27M63 30h27M63 40h18M28 56h62M24 17v7M24 50v12M57 56v15M91 50v12" stroke="#657086" stroke-width="3" stroke-linecap="round"/></svg>';
  const ramSvg = '<svg viewBox="0 0 120 86" role="img" aria-label="Иконка оперативной памяти" xmlns="http://www.w3.org/2000/svg"><rect x="16" y="28" width="88" height="28" rx="4" fill="#eef1f7" stroke="#657086" stroke-width="3"/><path d="M28 28v-9M40 28v-9M52 28v-9M64 28v-9M76 28v-9M88 28v-9M28 56v9M40 56v9M52 56v9M64 56v9M76 56v9M88 56v9" stroke="#657086" stroke-width="3" stroke-linecap="round"/><path d="M29 40h62M29 48h35" stroke="#635bff" stroke-width="3" stroke-linecap="round"/></svg>';
  const hddSvg = '<svg viewBox="0 0 120 86" role="img" aria-label="Иконка жёсткого диска" xmlns="http://www.w3.org/2000/svg"><rect x="19" y="13" width="82" height="60" rx="7" fill="#eef1f7" stroke="#657086" stroke-width="3"/><circle cx="60" cy="43" r="20" fill="#fff" stroke="#635bff" stroke-width="3"/><circle cx="60" cy="43" r="5" fill="#657086"/><path d="M60 23v40M40 43h40" stroke="#657086" stroke-width="2" opacity=".6"/></svg>';

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (char) => ({
      "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"
    }[char]));
  }

  function setError(message) {
    const status = $("#productStatus");
    status.classList.add("error");
    status.textContent = message;
  }

  const laptopUserValueTranslations = [
    [/\bPure Silver\b/gi, "Серебристый"],
    [/\bCool Silver\b/gi, "Серебристый"],
    [/\bLuna Grey\b/gi, "Серый"],
    [/\bMidnight Black\b/gi, "Чёрный"],
    [/\bCarbo Black\b/gi, "Чёрный"],
    [/\bMixed Black\b/gi, "Чёрный"],
    [/\bBlack\b/gi, "Чёрный"],
    [/\bWhite\b/gi, "Белый"],
    [/\bSilver\b/gi, "Серебристый"],
    [/\bGray\b/gi, "Серый"],
    [/\bGrey\b/gi, "Серый"],
    [/\bBlue\b/gi, "Синий"],
    [/\bGold\b/gi, "Золотистый"]
  ];

  const laptopScreenTermsToHide = new Set(["tn", "comfyview", "без сенсора"]);
  const laptopScreenValueTranslations = [
    [/\bTouchscreen\b/gi, "Сенсорный экран"],
    [/\bTouch\s+screen\b/gi, "Сенсорный экран"],
    [/\bTouch\b/gi, "Сенсорный экран"]
  ];

  function normalizeLaptopScreenValue(value) {
    const translated = laptopScreenValueTranslations.reduce(
      (result, [pattern, replacement]) => result.replace(pattern, replacement),
      value
    );
    return translated
      .split(",")
      .map((part) => part.trim())
      .filter((part) => !laptopScreenTermsToHide.has(part.toLowerCase()))
      .join(", ");
  }

  function normalizeLaptopUserValue(product, item) {
    const category = product.categoryName || product.category || "";
    if (category !== "Ноутбуки" || !item || typeof item.value !== "string") return item;

    const label = String(item.label || "").trim().toLowerCase();
    const isScreen = label === "экран";
    const userFacingCharacteristic = /цвет|покрыти|материал|особенност|клавиатур|раскладк|состояни|тип/.test(label);
    if (!userFacingCharacteristic && !isScreen) return item;

    let value = item.value;
    if (isScreen) value = normalizeLaptopScreenValue(value);
    if (userFacingCharacteristic) {
      value = laptopUserValueTranslations.reduce(
        (result, [pattern, replacement]) => result.replace(pattern, replacement),
        value
      );
    }

    return {
      ...item,
      value
    };
  }

  function mergeSpecs(product) {
    const merged = [];
    const labels = new Set();
    [...(product.verifiedSpecs || []), ...(product.catalogFacts || [])].forEach((item) => {
      if (!item || !item.label) return;
      const displayItem = normalizeLaptopUserValue(product, item);
      if (!String(displayItem.value ?? "").trim()) return;
      const key = item.label.trim().toLowerCase();
      if (labels.has(key)) return;
      labels.add(key);
      merged.push({...displayItem});
    });
    return merged;
  }

  function mainSpecs(product) {
    const specs = mergeSpecs(product);
    const category = product.categoryName || product.category || "";
    const find = (tests) => specs.find((item) => tests.some((test) => test(item.label.toLowerCase())));
    const wantedByCategory = {
      "Видеокарты":[["графика","модель"],["видеопамять","память"],["тип памяти"],["шина памяти"],["интерфейс"],["видеовыходы"]],
      "Процессоры":[["процессор"],["ядра/потоки"],["частота"],["кэш"],["сокет"],["графика"],["память"]],
      "SSD":[["накопитель"],["ёмкость","объём"],["интерфейс"],["форм-фактор"],["скорость чтения"],["скорость записи"]],
      "Материнские платы":[["модель"],["чипсет"],["сокет"],["тип памяти"],["форм-фактор"],["беспроводная сеть"]],
      "Оперативная память":[["модель"],["тип памяти"],["объём","ёмкость"],["частота"],["форм-фактор"],["задержка"]],
      "HDD":[["накопитель","модель"],["серия"],["ёмкость","объём"],["форм-фактор"],["интерфейс"],["назначение"]],
      "Корпуса":[["модель"],["форм-фактор"],["цвет"],["вентиляторы"],["поддержка радиатора"]],
      "Блоки питания":[["модель"],["мощность"],["стандарт"],["сертификат"],["модульность"]],
      "Охлаждение":[["модель","серия"],["тип охлаждения"],["размер радиатора"],["подсветка"]]
    };
    const tests = wantedByCategory[category] || [["процессор"],["оперативная память","память"],["накопител"],["экран"],["график"],["ос"]];
    const wanted = tests.map(labels => find(labels.map(label => value => value === label || value.includes(label)))).filter(Boolean);
    const uniqueWanted = wanted.filter((item,index,array) => array.findIndex(candidate => candidate.label === item.label) === index);
    if (uniqueWanted.length) return uniqueWanted;
    return specs.filter(item => !["Бренд","Категория"].includes(String(item.label || "").trim())).slice(0, 6);
  }

  function renderMainSpecs(product) {
    const mainSpecsNode = $("#mainSpecs");
    if (!mainSpecsNode) return;
    mainSpecsNode.innerHTML = mainSpecs(product).map((item) =>
      '<div class="main-spec-row"><dt>' + escapeHtml(item.label) + "</dt><dd>" +
      escapeHtml(item.value) + "</dd></div>"
    ).join("");
  }

  function renderFullSpecs(product) {
    const groups = new Map();
    const order = ["Общие параметры","Экран","Процессор","Оперативная память","Память","Графика","Накопители","Интерфейсы","Питание","Клавиатура","Габариты","Дополнительно"];
    mergeSpecs(product).forEach((item) => {
      const group = item.group || "Дополнительно";
      if (!groups.has(group)) groups.set(group, []);
      groups.get(group).push(item);
    });
    const orderedGroups = [
      ...order.filter(group => groups.has(group)),
      ...[...groups.keys()].filter(group => !order.includes(group))
    ];
    const specGroupsNode = $("#specGroups");
    if (!specGroupsNode) return;
    specGroupsNode.innerHTML = orderedGroups.map((group) =>
      '<section class="spec-group"><h3>' + escapeHtml(group) + '</h3><dl class="full-spec-list">' +
      groups.get(group).map((item) =>
        '<div class="full-spec-row"><dt>' + escapeHtml(item.label) + "</dt><dd>" +
        escapeHtml(item.value) +
        "</dd></div>"
      ).join("") + "</dl></section>"
    ).join("");
  }

  function activateTab(name) {
    document.querySelectorAll(".product-tab").forEach((button) => {
      const active = button.dataset.tab === name;
      button.classList.toggle("active", active);
      button.setAttribut  const categoryCopies = {
    "Моноблоки":{label:"Моноблоки",noun:"моноблок",genitive:"моноблока",url:"rgw_page_monoblocks.html"},
    "Ноутбуки":{label:"Ноутбуки",noun:"ноутбук",genitive:"ноутбука",url:"rgw_page_laptops.html"},
    "Мониторы":{label:"Мониторы",noun:"монитор",genitive:"монитора",url:"rgw_page_monitors.html"},
    "Видеокарты":{label:"Видеокарты",noun:"видеокарту",genitive:"видеокарты",url:"rgw_page_gpus.html"},
    "Процессоры":{label:"Процессоры",noun:"процессор",genitive:"процессора",url:"rgw_page_processors.html"},
    "SSD":{label:"SSD",noun:"накопитель SSD",genitive:"SSD",url:"rgw_page_ssd.html"},
    "Материнские платы":{label:"Материнские платы",noun:"материнскую плату",genitive:"материнской платы",url:"rgw_page_motherboards.html"},
    "Оперативная память":{label:"Оперативная память",noun:"оперативную память",genitive:"оперативной памяти",url:"rgw_page_ram.html"},
    "HDD":{label:"HDD",noun:"жёсткий диск",genitive:"жёсткого диска",url:"rgw_page_hdd.html"},
    "Корпуса":{label:"Корпуса",noun:"корпус",genitive:"корпуса",url:"rgw_page_cases.html"},
    "Блоки питания":{label:"Блоки питания",noun:"блок питания",genitive:"блока питания",url:"rgw_page_power_supplies.html"},
    "Охлаждение":{label:"Охлаждение",noun:"систему охлаждения",genitive:"системы охлаждения",url:"rgw_page_cooling.html"},
    "Точки доступа":{label:"Точки доступа",noun:"точку доступа",genitive:"точки доступа",url:"rgw_page_access_points.html"},
    "Переходники":{label:"Переходники",noun:"переходник",genitive:"переходника",url:"rgw_page_adapters.html"},
    "Аналоговые камеры":{label:"Аналоговые камеры",noun:"аналоговую камеру",genitive:"аналоговой камеры",url:"rgw_page_analog_cameras.html"},
    "Сумки и рюкзаки":{label:"Сумки и рюкзаки",noun:"сумку или рюкзак",genitive:"сумки или рюкзака",url:"rgw_page_bags.html"},
    "Кабели":{label:"Кабели",noun:"кабель",genitive:"кабеля",url:"rgw_page_cables.html"},
    "Картриджи":{label:"Картриджи",noun:"картридж",genitive:"картриджа",url:"rgw_page_cartridges.html"},
    "Коннекторы и розетки":{label:"Коннекторы и розетки",noun:"коннектор или розетку",genitive:"коннектора или розетки",url:"rgw_page_connectors_outlets.html"},
    "DVD-приводы":{label:"DVD-приводы",noun:"DVD-привод",genitive:"DVD-привода",url:"rgw_page_dvd_drives.html"},
    "Внешние HDD/SSD":{label:"Внешние HDD/SSD",noun:"внешний накопитель",genitive:"внешнего накопителя",url:"rgw_page_external_storage.html"},
    "Флешки":{label:"Флешки",noun:"флешку",genitive:"флешки",url:"rgw_page_flash_drives.html"},
    "Наушники":{label:"Наушники",noun:"наушники",genitive:"наушников",url:"rgw_page_headphones.html"},
    "Домофоны":{label:"Домофоны",noun:"домофон",genitive:"домофона",url:"rgw_page_intercoms.html"},
    "Инверторы":{label:"Инверторы",noun:"инвертор",genitive:"инвертора",url:"rgw_page_inverters.html"},
    "IP-камеры":{label:"IP-камеры",noun:"IP-камеру",genitive:"IP-камеры",url:"rgw_page_ip_cameras.html"},
    "IP-телефония":{label:"IP-телефония",noun:"IP-телефон",genitive:"IP-телефонии",url:"rgw_page_ip_telephony.html"},
    "Клавиатуры":{label:"Клавиатуры",noun:"клавиатуру",genitive:"клавиатуры",url:"rgw_page_keyboards.html"},
    "Карты памяти":{label:"Карты памяти",noun:"карту памяти",genitive:"карты памяти",url:"rgw_page_memory_cards.html"},
    "Mesh-системы":{label:"Mesh-системы",noun:"Mesh-систему",genitive:"Mesh-системы",url:"rgw_page_mesh.html"},
    "Мыши":{label:"Мыши",noun:"мышь",genitive:"мыши",url:"rgw_page_mice.html"},
    "Мини-АТС":{label:"Мини-АТС",noun:"мини-АТС",genitive:"мини-АТС",url:"rgw_page_mini_pbx.html"},
    "Сетевые аксессуары":{label:"Сетевые аксессуары",noun:"сетевой аксессуар",genitive:"сетевого аксессуара",url:"rgw_page_network_accessories.html"},
    "Сетевые кабели":{label:"Сетевые кабели",noun:"сетевой кабель",genitive:"сетевого кабеля",url:"rgw_page_network_cables.html"},
    "Сетевые карты":{label:"Сетевые карты",noun:"сетевую карту",genitive:"сетевой карты",url:"rgw_page_network_cards.html"},
    "Прочие аксессуары":{label:"Прочие аксессуары",noun:"аксессуар",genitive:"аксессуара",url:"rgw_page_other_accessories.html"},
    "Патч-панели":{label:"Патч-панели",noun:"патч-панель",genitive:"патч-панели",url:"rgw_page_patch_panels.html"},
    "Сетевые фильтры / пилоты":{label:"Сетевые фильтры / пилоты",noun:"сетевой фильтр",genitive:"сетевого фильтра",url:"rgw_page_power_strips.html"},
    "Расходные материалы":{label:"Расходные материалы",noun:"расходный материал",genitive:"расходного материала",url:"rgw_page_print_consumables.html"},
    "Принтеры и МФУ":{label:"Принтеры и МФУ",noun:"принтер или МФУ",genitive:"принтера или МФУ",url:"rgw_page_printers.html"},
    "Проекторы и экраны":{label:"Проекторы и экраны",noun:"проектор или экран",genitive:"проектора или экрана",url:"rgw_page_projectors_screens.html"},
    "Роутеры":{label:"Роутеры",noun:"роутер",genitive:"роутера",url:"rgw_page_routers.html"},
    "Серверные шкафы":{label:"Серверные шкафы",noun:"серверный шкаф",genitive:"серверного шкафа",url:"rgw_page_server_racks.html"},
    "Колонки":{label:"Колонки",noun:"колонку",genitive:"колонки",url:"rgw_page_speakers.html"},
    "Стабилизаторы":{label:"Стабилизаторы",noun:"стабилизатор",genitive:"стабилизатора",url:"rgw_page_stabilizers.html"},
    "Коммутаторы":{label:"Коммутаторы",noun:"коммутатор",genitive:"коммутатора",url:"rgw_page_switches.html"},
    "Системные блоки":{label:"Системные блоки",noun:"системный блок",genitive:"системного блока",url:"rgw_page_system_units.html"},
    "UPS":{label:"UPS",noun:"ИБП",genitive:"ИБП",url:"rgw_page_ups.html"},
    "Батареи для UPS":{label:"Батареи для UPS",noun:"батарею для UPS",genitive:"батареи для UPS",url:"rgw_page_ups_batteries.html"},
    "USB-хабы":{label:"USB-хабы",noun:"USB-хаб",genitive:"USB-хаба",url:"rgw_page_usb_hubs.html"},
    "Видеорегистраторы":{label:"Видеорегистраторы",noun:"видеорегистратор",genitive:"видеорегистратора",url:"rgw_page_video_recorders.html"},
    "Веб-камеры":{label:"Веб-камеры",noun:"веб-камеру",genitive:"веб-камеры",url:"rgw_page_webcams.html"},
    "Wi-Fi адаптеры":{label:"Wi-Fi адаптеры",noun:"Wi-Fi адаптер",genitive:"Wi-Fi адаптера",url:"rgw_page_wifi_adapters.html"},
    "Радиомосты":{label:"Радиомосты",noun:"радиомост",genitive:"радиомоста",url:"rgw_page_wireless_bridges.html"}
  };

  function categoryCopy(product) {
    const category = product.categoryName || product.category || "";
    return categoryCopies[category] || {label:category || "Каталог",noun:"товар",genitive:"товара",url:product.categoryUrl || "index.html"};
  }
  function emojiPlaceholder(product, copy) {
    const glyph = String(product.placeholder || "").trim();
    if (!glyph) return genericSvg;
    return '<svg viewBox="0 0 120 86" role="img" aria-label="Иконка ' + escapeHtml(copy.label) + '" xmlns="http://www.w3.org/2000/svg"><text x="60" y="59" text-anchor="middle" font-size="48">' + escapeHtml(glyph) + '</text></svg>';
  }

  function placeholderFor(product, copy) {
    if (copy.label === "Моноблоки") return monoSvg;
    if (copy.label === "Ноутбуки") return laptopSvg;
    if (copy.label === "Видеокарты") return gpuSvg;
    if (copy.label === "Процессоры") return cpuSvg;
    if (copy.label === "SSD") return ssdSvg;
    if (copy.label === "Материнские платы") return motherboardSvg;
    if (copy.label === "Оперативная память") return ramSvg;
    if (copy.label === "HDD") return hddSvg;
    if (copy.label === "Корпуса" || copy.label === "Системные блоки") return caseSvg;
    if (copy.label === "Блоки питания") return psuSvg;
    if (copy.label === "Охлаждение") return coolingSvg;
    return emojiPlaceholder(product, copy);
  }

  function render(product) {
    document.title = product.name + " — АКС";
    const setText = (selector, value) => {
      const node = $(selector);
      if (node) node.textContent = value;
    };
    const copy = categoryCopy(product);
    setText("#productBreadcrumb", product.name);
    setText("#productBrand", product.brand);
    setText("#productBrandMark", product.brand);
    setText("#productName", product.name);
    const categoryLink = $("#productCategoryLink");
    if (categoryLink) {
      categoryLink.textContent = copy.label;
      categoryLink.href = product.categoryUrl || copy.url;
    }
    const buildDescription = $("#productBuildDescription");
    if (buildDescription) buildDescription.textContent = "Сохраните " + copy.noun + " для будущего подбора комплектующих и сравнения конфигураций.";
    const descriptionText = $("#productDescriptionText");
    if (descriptionText) descriptionText.textContent = "Здесь собраны основные характеристики конкретной конфигурации " + copy.genitive + ".";

    const identifiers = product.identifiers || {};
    const modelParts = [identifiers.modelNumber, identifiers.machineType, identifiers.partNumber, identifiers.family].filter(Boolean);
    setText("#productSku", "Код товара: " + product.sku +
      (modelParts.length ? " · Модель/платформа: " + modelParts.join(" · ") : ""));

    const visual = $("#productVisual");
    if (visual && product.image) {
      visual.innerHTML = '<img src="' + escapeHtml(product.image) + '" alt="' + escapeHtml(product.name) + '">';
    } else if (visual) {
      const placeholderSvg = placeholderFor(product, copy);
      visual.innerHTML = '<div class="product-placeholder"><div class="product-placeholder-icon" aria-hidden="true">' +
        placeholderSvg + '</div><div class="product-placeholder-caption">Изображение товара</div></div>';
    }

    renderMainSpecs(product);
    renderFullSpecs(product);

    const productStatus = $("#productStatus");
    const productContent = $("#productContent");
    if (productStatus) productStatus.hidden = true;
    if (productContent) productContent.hidden = false;
  }

  function initInteractions() {
    document.querySelectorAll(".product-tab").forEach((button) => {
      button.addEventListener("click", () => activateTab(button.dataset.tab));
    });
    const allSpecsLink = $("#allSpecsLink");
    if (allSpecsLink) allSpecsLink.addEventListener("click", () => {
      activateTab("specs");
      const fullSpecs = $("#fullSpecs");
      if (fullSpecs) fullSpecs.scrollIntoView({behavior:"smooth", block:"start"});
    });
    const buildButton = $("#buildButton");
    if (buildButton) buildButton.addEventListener("click", (event) => {
      const button = event.currentTarget;
      const added = button.getAttribute("aria-pressed") === "true";
      button.setAttribute("aria-pressed", String(!added));
      button.textContent = added ? "Добавить" : "Добавлено";
    });
    document.querySelectorAll(".product-thumb").forEach((thumb) => {
      thumb.addEventListener("click", () => {
        document.querySelectorAll(".product-thumb").forEach((item) => item.classList.remove("active"));
        thumb.classList.add("active");
      });
    });
  }

  async function init() {
    const id = new URLSearchParams(window.location.search).get("id");
    if (!id) {
      setError("Товар не найден. Откройте карточку из каталога.");
      return;
    }
    try {
      const response = await fetch("products.json", {cache:"no-store"});
      if (!response.ok) throw new Error("products.json: " + response.status);
      state.products = await response.json();
      state.byId = new Map(state.products.map((product) => [product.id, product]));
      const product = state.byId.get(id);
      if (!product) {
        setError("Товар не найден.");
        return;
      }
      render(product);
      try {
        initInteractions();
      } catch (interactionError) {
        console.warn("Product interactions unavailable:", interactionError);
      }
    } catch (error) {
      console.error(error);
      setError("Не удалось загрузить карточку товара: " + (error && error.message ? error.message : String(error)));
    }
  }

  init();
})();

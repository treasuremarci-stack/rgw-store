(() => {
  const state = { products: [], byId: new Map() };
  const $ = (selector) => document.querySelector(selector);
  const laptopSvg = '<svg viewBox="0 0 120 82" role="img" aria-label="Иконка ноутбука" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="8" width="80" height="53" rx="5" fill="#eef1f7" stroke="#657086" stroke-width="3"/><path d="M14 67h92l8 7H6l8-7Z" fill="#d7dce6" stroke="#657086" stroke-width="3" stroke-linejoin="round"/><path d="M33 22h54v28H33z" fill="#fff" opacity=".8"/><path d="M47 36h26" stroke="#635bff" stroke-width="3" stroke-linecap="round"/></svg>';
  const monoSvg = '<svg viewBox="0 0 120 86" role="img" aria-label="Иконка моноблока" xmlns="http://www.w3.org/2000/svg"><rect x="18" y="7" width="84" height="55" rx="5" fill="#eef1f7" stroke="#657086" stroke-width="3"/><path d="M42 70h36l4 8H38l4-8Z" fill="#d7dce6" stroke="#657086" stroke-width="3" stroke-linejoin="round"/><path d="M31 22h58v28H31z" fill="#fff" opacity=".82"/><circle cx="60" cy="15" r="2" fill="#657086"/><path d="M48 36h24" stroke="#635bff" stroke-width="3" stroke-linecap="round"/></svg>';

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

  function mergeSpecs(product) {
    const merged = [];
    const labels = new Set();
    [...(product.verifiedSpecs || []), ...(product.catalogFacts || [])].forEach((item) => {
      if (!item || !item.label) return;
      const key = item.label.trim().toLowerCase();
      if (labels.has(key)) return;
      labels.add(key);
      merged.push({...item});
    });
    return merged;
  }

  function mainSpecs(product) {
    const specs = mergeSpecs(product);
    const find = (test) => specs.find((item) => test(item.label.toLowerCase()));
    const wanted = [
      find(label => label === "процессор"),
      find(label => label.includes("оперативная память") || label === "память"),
      find(label => label.includes("накопител")),
      find(label => label === "экран"),
      find(label => label.includes("график")),
      find(label => label === "ос")
    ].filter(Boolean);
    return wanted.filter((item,index,array) =>
      array.findIndex(candidate => candidate.label === item.label) === index
    );
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
    const order = ["Общие параметры","Экран","Процессор","Оперативная память","Графика","Накопители","Интерфейсы","Питание","Клавиатура","Габариты","Дополнительно"];
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
      button.setAttribute("aria-selected", String(active));
    });
    document.querySelectorAll("[data-panel]").forEach((panel) => {
      panel.hidden = panel.dataset.panel !== name;
    });
  }

  function categoryCopy(product) {
    const category = product.categoryName || product.category || "";
    if (category === "Моноблоки") {
      return {label:"Моноблоки", noun:"моноблок", genitive:"моноблока"};
    }
    if (category === "Ноутбуки") {
      return {label:"Ноутбуки", noun:"ноутбук", genitive:"ноутбука"};
    }
    return {label:category || "Каталог", noun:"товар", genitive:"товара"};
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
      categoryLink.href = product.categoryUrl || (copy.label === "Моноблоки" ? "rgw_page_monoblocks.html" : "rgw_page_laptops.html");
    }
    const buildDescription = $("#productBuildDescription");
    if (buildDescription) buildDescription.textContent = "Сохраните " + copy.noun + " для будущего подбора комплектующих и сравнения конфигураций.";
    const descriptionText = $("#productDescriptionText");
    if (descriptionText) descriptionText.textContent = "Карточка показывает характеристики конкретной конфигурации " + copy.genitive + ". Параметры без надёжного подтверждения намеренно не добавляются.";

    const identifiers = product.identifiers || {};
    const modelParts = [identifiers.modelNumber, identifiers.machineType, identifiers.partNumber, identifiers.family].filter(Boolean);
    setText("#productSku", "Код товара: " + product.sku +
      (modelParts.length ? " · Модель/платформа: " + modelParts.join(" · ") : ""));

    const visual = $("#productVisual");
    if (visual && product.image) {
      visual.innerHTML = '<img src="' + escapeHtml(product.image) + '" alt="' + escapeHtml(product.name) + '">';
    } else if (visual) {
      const placeholderSvg = copy.label === "Моноблоки" ? monoSvg : laptopSvg;
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

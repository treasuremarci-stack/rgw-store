(() => {
  const state = { products: [], byId: new Map() };
  const $ = (selector) => document.querySelector(selector);

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
      merged.push({...item, verified:Boolean(item.sourceName)});
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

  function sourceNote(item) {
    return item.verified && item.sourceName
      ? '<span class="main-spec-source">Источник: ' + escapeHtml(item.sourceName) + "</span>"
      : "";
  }

  function renderMainSpecs(product) {
    $("#mainSpecs").innerHTML = mainSpecs(product).map((item) =>
      '<div class="main-spec-row"><dt>' + escapeHtml(item.label) + "</dt><dd>" +
      escapeHtml(item.value) + sourceNote(item) + "</dd></div>"
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
    $("#specGroups").innerHTML = orderedGroups.map((group) =>
      '<section class="spec-group"><h3>' + escapeHtml(group) + '</h3><dl class="full-spec-list">' +
      groups.get(group).map((item) =>
        '<div class="full-spec-row"><dt>' + escapeHtml(item.label) + "</dt><dd>" +
        escapeHtml(item.value) +
        (item.verified && item.sourceName ? '<span class="spec-source">Источник: ' + escapeHtml(item.sourceName) + "</span>" : "") +
        "</dd></div>"
      ).join("") + "</dl></section>"
    ).join("");
  }

  function renderVerification(product) {
    const verification = product.verification || {};
    const notes = verification.notes || [];
    const note = notes.length
      ? '<p class="verification-note">' + notes.map(escapeHtml).join("<br>") + "</p>"
      : "";
    const sources = (product.sources || []).map((item) => {
      const name = escapeHtml(item.name);
      const scope = item.scope ? " · " + escapeHtml(item.scope) : "";
      const link = item.url
        ? '<a href="' + escapeHtml(item.url) + '" target="_blank" rel="noopener noreferrer">' + name + "</a>"
        : name;
      return "<li>" + link + ' <small>(' + escapeHtml(item.type || "source") + scope + ")</small></li>";
    }).join("");
    $("#productVerification").innerHTML =
      "<h3>Проверка данных</h3>" + note +
      "<div>Статус: <strong>" + escapeHtml(verification.status || "не указан") +
      "</strong>. Параметры без однозначного подтверждения не добавлялись.</div>" +
      '<ul class="source-list">' + sources + "</ul>";
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

  function render(product) {
    document.title = product.name + " — АКС";
    $("#productBreadcrumb").textContent = product.name;
    $("#productBrand").textContent = product.brand;
    $("#productName").textContent = product.name;

    const identifiers = product.identifiers || {};
    const modelParts = [identifiers.modelNumber, identifiers.machineType, identifiers.partNumber, identifiers.family].filter(Boolean);
    $("#productSku").textContent = "Код товара: " + product.sku +
      (modelParts.length ? " · Модель/платформа: " + modelParts.join(" · ") : "");

    const visual = $("#productVisual");
    if (product.image) {
      visual.innerHTML = '<img src="' + escapeHtml(product.image) + '" alt="' + escapeHtml(product.name) + '">';
    } else {
      visual.innerHTML = '<div class="product-placeholder"><div class="product-placeholder-icon" aria-hidden="true">' +
        escapeHtml(product.placeholder || "💻") + '</div><div class="product-placeholder-caption">Изображение товара</div></div>';
    }

    renderMainSpecs(product);
    renderFullSpecs(product);
    renderVerification(product);

    $("#productStatus").hidden = true;
    $("#productContent").hidden = false;
  }

  function initInteractions() {
    document.querySelectorAll(".product-tab").forEach((button) => {
      button.addEventListener("click", () => activateTab(button.dataset.tab));
    });
    $("#allSpecsLink").addEventListener("click", () => {
      activateTab("specs");
      $("#fullSpecs").scrollIntoView({behavior:"smooth", block:"start"});
    });
    $("#buildButton").addEventListener("click", (event) => {
      const button = event.currentTarget;
      const added = button.getAttribute("aria-pressed") === "true";
      button.setAttribute("aria-pressed", String(!added));
      button.textContent = added ? "Добавить" : "Добавлено";
    });
  }

  async function init() {
    const id = new URLSearchParams(window.location.search).get("id");
    if (!id) {
      setError("Товар не найден. Откройте карточку из каталога ноутбуков.");
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
      initInteractions();
    } catch (error) {
      console.error(error);
      setError("Не удалось загрузить карточку товара. Повторите попытку позже.");
    }
  }

  init();
})();

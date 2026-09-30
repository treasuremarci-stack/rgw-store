(() => {
  const state = {
    products: [],
    byId: new Map()
  };

  const $ = (selector) => document.querySelector(selector);

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (char) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;"
    }[char]));
  }

  function setError(message) {
    const status = $("#productStatus");
    status.classList.add("error");
    status.textContent = message;
  }

  function renderSources(product) {
    const list = $("#productSources");
    list.innerHTML = (product.sources || []).map((item) => {
      const label = escapeHtml(item.name);
      const scope = item.scope ? " · " + escapeHtml(item.scope) : "";
      const link = item.url
        ? '<a href="' + escapeHtml(item.url) + '" target="_blank" rel="noreferrer noopener">' + label + "</a>"
        : label;
      return "<li>" + link + ' <small>(' + escapeHtml(item.type || "source") + scope + ")</small></li>";
    }).join("");
  }

  function mergeSpecs(product) {
    const merged = [];
    const labels = new Set();
    (product.verifiedSpecs || []).forEach((item) => {
      if (!item || !item.label || labels.has(item.label)) return;
      labels.add(item.label);
      merged.push({...item, verified:true});
    });
    (product.catalogFacts || []).forEach((item) => {
      if (!item || !item.label || labels.has(item.label)) return;
      labels.add(item.label);
      merged.push({...item, verified:false});
    });
    return merged;
  }

  function render(product) {
    document.title = product.name + " — АКС";
    $("#productBreadcrumb").textContent = product.name;
    $("#productBrand").textContent = product.brand;
    $("#productName").textContent = product.name;
    const identifiers = product.identifiers || {};
    const modelParts = [identifiers.modelNumber, identifiers.machineType, identifiers.partNumber, identifiers.family].filter(Boolean);
    $("#productSku").textContent = "SKU проекта: " + product.sku + (modelParts.length ? " · Модель/платформа: " + modelParts.join(" · ") : "");
    if (product.price) {
      $("#productPrice").textContent = product.price + " ₽";
      $("#productPriceNote").textContent = "Цена взята из price.csv";
    } else {
      $("#productPrice").textContent = "Цена уточняется";
      $("#productPriceNote").textContent = "В price.csv нет однозначного совпадения";
    }

    const visual = $("#productVisual");
    if (product.image) {
      visual.innerHTML = '<img src="' + escapeHtml(product.image) + '" alt="' + escapeHtml(product.name) + '">';
    } else {
      visual.innerHTML = '<span aria-hidden="true">' + escapeHtml(product.placeholder || "💻") + "</span>";
    }

    $("#productSpecs").innerHTML = mergeSpecs(product).map((item) => {
      const source = item.verified && item.sourceName
        ? '<span class="spec-source">Источник: ' + escapeHtml(item.sourceName) + "</span>"
        : "";
      return '<div class="spec-row"><dt>' + escapeHtml(item.label) + "</dt><dd>" + escapeHtml(item.value) + source + "</dd></div>";
    }).join("");

    const verification = product.verification || {};
    const notes = verification.notes || [];
    const noteMarkup = notes.length
      ? '<p class="verification-note">' + notes.map(escapeHtml).join("<br>") + "</p>"
      : "";
    $("#productVerification").innerHTML = noteMarkup + "<p>Статус: <strong>" +
      escapeHtml(verification.status || "не указан") + "</strong>. Интернет-источники использованы только для технических характеристик.</p>";
    renderSources(product);

    $("#productStatus").hidden = true;
    $("#productContent").hidden = false;
  }

  async function init() {
    const id = new URLSearchParams(window.location.search).get("id");
    if (!id) {
      setError("Не указан идентификатор товара. Откройте карточку из каталога ноутбуков.");
      return;
    }
    try {
      const response = await fetch("products.json", {cache:"no-store"});
      if (!response.ok) throw new Error("products.json: " + response.status);
      state.products = await response.json();
      state.byId = new Map(state.products.map((product) => [product.id, product]));
      const product = state.byId.get(id);
      if (!product) {
        setError("Товар с идентификатором «" + id + "» не найден.");
        return;
      }
      render(product);
    } catch (error) {
      console.error(error);
      setError("Не удалось загрузить данные карточки товара. Повторите попытку позже.");
    }
  }

  init();
})();

(function () {
  "use strict";

  var $ = function (id) { return document.getElementById(id); };
  var state = {
    client: null,
    session: null,
    products: [],
    categories: [],
    images: [],
    editingProductId: null,
    categoryEditId: null,
    toastTimer: null
  };

  var config = window.AKS_SUPABASE_CONFIG || {};
  var configReady = Boolean(
    window.supabase &&
    typeof window.supabase.createClient === "function" &&
    /^https?:\/\//.test(config.url || "") &&
    config.anonKey &&
    !/service_role/i.test(config.anonKey)
  );

  function toggle(id, visible) {
    var node = $(id);
    if (node) node.classList.toggle("hidden", !visible);
  }

  function setText(id, value) {
    var node = $(id);
    if (node) node.textContent = value == null ? "" : String(value);
  }

  function showToast(message, isError) {
    var node = $("toast");
    if (!node) return;
    node.textContent = message;
    node.classList.toggle("toast-error", Boolean(isError));
    node.classList.remove("hidden");
    clearTimeout(state.toastTimer);
    state.toastTimer = setTimeout(function () { node.classList.add("hidden"); }, 4200);
  }

  function errorText(error) {
    if (!error) return "Неизвестная ошибка.";
    return error.message || error.details || error.hint || String(error);
  }

  function setFormError(id, message) {
    setText(id, message || "");
  }

  function formatPrice(value) {
    if (value === null || value === undefined || value === "") return "—";
    var number = Number(value);
    if (!Number.isFinite(number)) return "—";
    return new Intl.NumberFormat("ru-RU", { maximumFractionDigits: 2 }).format(number) + " сомони";
  }

  function normalize(value) {
    return String(value || "").trim().toLocaleLowerCase("ru-RU");
  }

  function categoryById(id) {
    return state.categories.find(function (item) { return item.id === id; });
  }

  function categoryLabel(id) {
    var category = categoryById(id);
    return category ? category.name : "Без категории";
  }

  function imagesForProduct(id) {
    return state.images
      .filter(function (item) { return item.product_id === id; })
      .sort(function (a, b) { return (a.sort_order || 0) - (b.sort_order || 0); });
  }

  function renderAuth() {
    var signedIn = Boolean(state.session && state.session.user);
    toggle("loginPanel", configReady && !signedIn);
    toggle("appPanel", configReady && signedIn);
    if (!configReady) {
      setText("authState", "Ожидает настройки");
    } else if (signedIn) {
      setText("authState", "Вход: " + (state.session.user.email || "администратор"));
    } else {
      setText("authState", "Вход не выполнен");
    }
  }

  function renderStats() {
    setText("statProducts", state.products.length);
    setText("statPublished", state.products.filter(function (item) { return item.is_published; }).length);
    setText("statCategories", state.categories.length);
    setText("statImages", state.products.filter(function (item) { return Boolean(item.main_image); }).length);
  }

  function appendOption(select, value, label, selected) {
    var option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    option.selected = Boolean(selected);
    select.appendChild(option);
  }

  function categorySort(a, b) {
    return (a.sort_order || 0) - (b.sort_order || 0) || a.name.localeCompare(b.name, "ru");
  }

  function renderCategoryOptions() {
    var filter = $("categoryFilter");
    var productCategory = $("productCategory");
    var subcategory = $("productSubcategory");
    var parent = $("categoryParent");
    var oldFilter = filter.value;
    var oldCategory = productCategory.value;
    var oldSubcategory = subcategory.value;
    var oldParent = parent.value;

    filter.innerHTML = "";
    appendOption(filter, "", "Все категории", oldFilter === "");
    state.categories.slice().sort(categorySort).forEach(function (category) {
      appendOption(filter, category.id, category.name, category.id === oldFilter);
    });

    productCategory.innerHTML = "";
    appendOption(productCategory, "", "Выберите категорию", oldCategory === "");
    state.categories.filter(function (item) { return item.is_active; }).sort(categorySort).forEach(function (category) {
      appendOption(productCategory, category.id, category.name, category.id === oldCategory);
    });

    subcategory.innerHTML = "";
    appendOption(subcategory, "", "Нет подкатегории", oldSubcategory === "");
    state.categories.filter(function (item) { return item.is_active; }).sort(categorySort).forEach(function (category) {
      appendOption(subcategory, category.id, category.name, category.id === oldSubcategory);
    });

    parent.innerHTML = "";
    appendOption(parent, "", "Нет родительской", oldParent === "");
    state.categories.filter(function (item) {
      return item.id !== state.categoryEditId;
    }).sort(categorySort).forEach(function (category) {
      appendOption(parent, category.id, category.name, category.id === oldParent);
    });
  }

  function renderProducts() {
    var body = $("productsBody");
    var query = normalize($("searchInput").value);
    var categoryId = $("categoryFilter").value;
    var status = $("statusFilter").value;
    body.replaceChildren();

    var filtered = state.products.filter(function (product) {
      var haystack = normalize([product.id, product.name, product.brand, product.model, product.sku].join(" "));
      var matchesSearch = !query || haystack.indexOf(query) !== -1;
      var matchesCategory = !categoryId || product.category_id === categoryId || product.subcategory_id === categoryId;
      var matchesStatus = !status ||
        (status === "published" && product.is_published) ||
        (status === "hidden" && !product.is_published);
      return matchesSearch && matchesCategory && matchesStatus;
    });

    filtered.sort(function (a, b) {
      return String(b.updated_at || "").localeCompare(String(a.updated_at || ""));
    });

    filtered.forEach(function (product) {
      var row = document.createElement("tr");
      var idCell = document.createElement("td");
      idCell.className = "table-id";
      idCell.textContent = product.id;
      row.appendChild(idCell);

      var nameCell = document.createElement("td");
      var name = document.createElement("strong");
      name.textContent = product.name;
      nameCell.appendChild(name);
      var sku = document.createElement("div");
      sku.className = "table-sub";
      sku.textContent = product.sku ? "SKU: " + product.sku : (product.main_image ? "Есть основное фото" : "Без фото");
      nameCell.appendChild(sku);
      row.appendChild(nameCell);

      var modelCell = document.createElement("td");
      modelCell.textContent = [product.model, product.brand].filter(Boolean).join(" · ") || "—";
      row.appendChild(modelCell);

      var categoryCell = document.createElement("td");
      categoryCell.textContent = categoryLabel(product.subcategory_id || product.category_id);
      row.appendChild(categoryCell);

      var priceCell = document.createElement("td");
      priceCell.textContent = formatPrice(product.price_tjs);
      row.appendChild(priceCell);

      var statusCell = document.createElement("td");
      var statusPill = document.createElement("span");
      statusPill.className = "status-pill " + (product.is_published ? "status-published" : "status-hidden");
      statusPill.textContent = product.is_published ? "Опубликован" : "Скрыт";
      statusCell.appendChild(statusPill);
      row.appendChild(statusCell);

      var actionsCell = document.createElement("td");
      actionsCell.className = "row-actions";
      var editButton = document.createElement("button");
      editButton.type = "button";
      editButton.className = "button button-light";
      editButton.textContent = "Изменить";
      editButton.dataset.editProduct = product.id;
      actionsCell.appendChild(editButton);
      var deleteButton = document.createElement("button");
      deleteButton.type = "button";
      deleteButton.className = "button button-danger";
      deleteButton.textContent = "Удалить";
      deleteButton.dataset.deleteProduct = product.id;
      actionsCell.appendChild(deleteButton);
      row.appendChild(actionsCell);
      body.appendChild(row);
    });

    toggle("emptyState", filtered.length === 0);
    setText("tableSummary", filtered.length + " из " + state.products.length);
  }

  function renderCategories() {
    var list = $("categoriesList");
    list.replaceChildren();
    state.categories.slice().sort(categorySort).forEach(function (category) {
      var item = document.createElement("li");
      var info = document.createElement("div");
      info.className = "category-info";
      var title = document.createElement("strong");
      title.textContent = category.name + (category.is_active ? "" : " (скрыта)");
      info.appendChild(title);
      var meta = document.createElement("small");
      meta.textContent = category.slug + (category.parent_id ? " · дочерняя" : "");
      info.appendChild(meta);
      item.appendChild(info);

      var actions = document.createElement("div");
      actions.className = "category-actions-inline";
      var edit = document.createElement("button");
      edit.type = "button";
      edit.className = "button button-light";
      edit.textContent = "Изменить";
      edit.dataset.editCategory = category.id;
      actions.appendChild(edit);
      var remove = document.createElement("button");
      remove.type = "button";
      remove.className = "button button-danger";
      remove.textContent = "Удалить";
      remove.dataset.deleteCategory = category.id;
      actions.appendChild(remove);
      item.appendChild(actions);
      list.appendChild(item);
    });
  }

  function renderAll() {
    renderStats();
    renderCategoryOptions();
    renderProducts();
    renderCategories();
  }

  async function loadData() {
    if (!state.client || !state.session) return;
    setText("tableSummary", "Загрузка…");
    var results = await Promise.all([
      state.client.from("catalog_products").select("*"),
      state.client.from("catalog_categories").select("*"),
      state.client.from("catalog_product_images").select("*")
    ]);
    var failure = results.find(function (result) { return result.error; });
    if (failure) throw failure.error;
    state.products = results[0].data || [];
    state.categories = results[1].data || [];
    state.images = results[2].data || [];
    renderAll();
  }


  function chunkItems(items, size) {
    var chunks = [];
    for (var index = 0; index < items.length; index += size) {
      chunks.push(items.slice(index, index + size));
    }
    return chunks;
  }

  function importCategoryRows(names) {
    var used = {};
    return names.map(function (name, index) {
      var base = transliterate(name) || ("category-" + (index + 1));
      var slug = base;
      var suffix = 2;
      while (used[slug]) {
        slug = base + "-" + suffix;
        suffix += 1;
      }
      used[slug] = true;
      return {
        name: name,
        slug: slug,
        sort_order: index,
        is_active: true
      };
    });
  }

  function catalogImagePaths(product) {
    return uniquePaths([product.image].concat(Array.isArray(product.images) ? product.images : []));
  }

  function catalogSpecifications(product) {
    return {
      catalogFacts: Array.isArray(product.catalogFacts) ? product.catalogFacts : [],
      verifiedSpecs: Array.isArray(product.verifiedSpecs) ? product.verifiedSpecs : [],
      identifiers: product.identifiers && typeof product.identifiers === "object" ? product.identifiers : {},
      placeholder: product.placeholder || null,
      categoryUrl: product.categoryUrl || null
    };
  }

  async function importExistingCatalog() {
    if (!state.client || !state.session) {
      showToast("Сначала войдите в админку.", true);
      return;
    }
    if (!window.confirm(
      "Импортировать существующие товары без цен?\\n\\n" +
      "Будут добавлены категории и товары из products.json. Цены останутся пустыми. " +
      "Уже существующие ID будут пропущены, чтобы не стереть будущие цены."
    )) return;

    var button = $("importCatalogButton");
    button.disabled = true;
    button.textContent = "Подготовка импорта…";
    try {
      var response = await fetch("../products.json", { cache: "no-store" });
      if (!response.ok) throw new Error("Не удалось загрузить products.json: HTTP " + response.status);
      var source = await response.json();
      if (!Array.isArray(source) || !source.length) throw new Error("products.json не содержит товаров.");

      var categoryNames = Array.from(new Set(source.map(function (product) {
        return String(product.categoryName || product.category || "").trim();
      }).filter(Boolean))).sort(function (a, b) {
        return a.localeCompare(b, "ru");
      });
      if (!categoryNames.length) throw new Error("В товарах не найдены категории.");

      var categoryRows = importCategoryRows(categoryNames);
      var categoryInsert = await state.client
        .from("catalog_categories")
        .upsert(categoryRows, { onConflict: "slug" });
      if (categoryInsert.error) throw categoryInsert.error;

      var categoryResult = await state.client
        .from("catalog_categories")
        .select("id,name,slug");
      if (categoryResult.error) throw categoryResult.error;
      var categoryByName = {};
      (categoryResult.data || []).forEach(function (category) {
        categoryByName[category.name] = category;
      });

      var productRows = source.map(function (product) {
        var categoryName = String(product.categoryName || product.category || "").trim();
        var category = categoryByName[categoryName];
        if (!category) throw new Error("Не найдена категория: " + categoryName);
        var identifiers = product.identifiers && typeof product.identifiers === "object" ? product.identifiers : {};
        var imagePaths = catalogImagePaths(product);
        return {
          id: product.id,
          sku: product.sku || null,
          name: product.name,
          brand: product.brand || null,
          model: identifiers.modelNumber || identifiers.partNumber || null,
          category_id: category.id,
          subcategory_id: null,
          price_tjs: null,
          specifications: catalogSpecifications(product),
          main_image: product.image || imagePaths[0] || null,
          is_published: true
        };
      });

      var productChunks = chunkItems(productRows, 40);
      for (var productIndex = 0; productIndex < productChunks.length; productIndex += 1) {
        var productInsert = await state.client
          .from("catalog_products")
          .upsert(productChunks[productIndex], { onConflict: "id", ignoreDuplicates: true });
        if (productInsert.error) throw productInsert.error;
        button.textContent = "Товары " + Math.min((productIndex + 1) * 40, productRows.length) + "/" + productRows.length;
      }

      var imageRows = [];
      source.forEach(function (product) {
        var paths = catalogImagePaths(product);
        var mainPath = product.image || paths[0] || null;
        paths.forEach(function (path, pathIndex) {
          imageRows.push({
            product_id: product.id,
            storage_path: path,
            alt_text: product.name || null,
            sort_order: pathIndex,
            is_primary: path === mainPath
          });
        });
      });

      var imageChunks = chunkItems(imageRows, 40);
      for (var imageIndex = 0; imageIndex < imageChunks.length; imageIndex += 1) {
        var imageInsert = await state.client
          .from("catalog_product_images")
          .upsert(imageChunks[imageIndex], { onConflict: "product_id,storage_path", ignoreDuplicates: true });
        if (imageInsert.error) throw imageInsert.error;
      }

      await loadData();
      showToast("Импорт завершен: " + productRows.length + " товаров, " + categoryRows.length + " категорий. Цены оставлены пустыми.");
    } catch (error) {
      showToast("Импорт не завершен: " + errorText(error), true);
    } finally {
      button.disabled = false;
      button.textContent = "Импорт каталога без цен";
    }
  }

  function openModal(product) {
    state.editingProductId = product ? product.id : null;
    $("productModalTitle").textContent = product ? "Редактировать товар" : "Добавить товар";
    $("productId").value = product ? product.id : "";
    $("productId").readOnly = Boolean(product);
    $("productSku").value = product && product.sku ? product.sku : "";
    $("productName").value = product ? product.name : "";
    $("productBrand").value = product && product.brand ? product.brand : "";
    $("productModel").value = product && product.model ? product.model : "";
    $("productCategory").value = product ? product.category_id : "";
    $("productSubcategory").value = product ? (product.subcategory_id || "") : "";
    $("productPrice").value = product && product.price_tjs !== null && product.price_tjs !== undefined ? product.price_tjs : "";
    $("productPublished").checked = Boolean(product && product.is_published);
    $("productMainImage").value = product && product.main_image ? product.main_image : "";
    $("productGallery").value = product ? imagesForProduct(product.id).map(function (image) { return image.storage_path; }).join("\n") : "";
    $("productFiles").value = "";
    $("productSpecifications").value = JSON.stringify(product && product.specifications ? product.specifications : {}, null, 2);
    setFormError("productError", "");
    $("productModal").classList.remove("hidden");
    $("productName").focus();
  }

  function closeModal() {
    $("productModal").classList.add("hidden");
    state.editingProductId = null;
  }

  function parseSpecifications() {
    var raw = $("productSpecifications").value.trim();
    if (!raw) return {};
    var parsed = JSON.parse(raw);
    if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") {
      throw new Error("Характеристики должны быть JSON-объектом.");
    }
    return parsed;
  }

  function uniquePaths(values) {
    var seen = new Set();
    return values.map(function (value) { return String(value || "").trim(); })
      .filter(function (value) {
        if (!value || seen.has(value)) return false;
        seen.add(value);
        return true;
      });
  }

  function uploadPath(productId, file, index) {
    var safeName = file.name.toLowerCase().replace(/[^a-z0-9._-]+/g, "-").replace(/^-+|-+$/g, "");
    var nonce = window.crypto && typeof window.crypto.randomUUID === "function" ? window.crypto.randomUUID() : String(Date.now());
    return productId + "/" + nonce + "-" + index + "-" + (safeName || "image");
  }

  async function uploadSelectedFiles(productId) {
    var files = Array.prototype.slice.call($("productFiles").files || []);
    if (!files.length) return [];
    var uploaded = [];
    var bucket = state.client.storage.from("catalog-images");
    for (var index = 0; index < files.length; index += 1) {
      var file = files[index];
      var path = uploadPath(productId, file, index);
      var result = await bucket.upload(path, file, {
        cacheControl: "3600",
        upsert: false,
        contentType: file.type || "application/octet-stream"
      });
      if (result.error) throw result.error;
      uploaded.push(path);
    }
    return uploaded;
  }

  async function saveProduct(event) {
    event.preventDefault();
    setFormError("productError", "");
    var button = $("productSaveButton");
    button.disabled = true;
    button.textContent = "Сохранение…";
    try {
      var id = $("productId").value.trim();
      if (!/^[A-Za-z0-9][A-Za-z0-9._-]{1,127}$/.test(id)) {
        throw new Error("ID: латинские буквы, цифры, точка, дефис или подчеркивание; минимум 2 символа.");
      }
      var priceRaw = $("productPrice").value.trim();
      var price = priceRaw === "" ? null : Number(priceRaw);
      if (price !== null && (!Number.isFinite(price) || price < 0 || price > 100000000)) {
        throw new Error("Цена должна быть числом от 0 до 100 000 000 сомони.");
      }
      var categoryId = $("productCategory").value;
      if (!categoryId) throw new Error("Выберите категорию.");
      var payload = {
        id: id,
        sku: $("productSku").value.trim() || null,
        name: $("productName").value.trim(),
        brand: $("productBrand").value.trim() || null,
        model: $("productModel").value.trim() || null,
        category_id: categoryId,
        subcategory_id: $("productSubcategory").value || null,
        price_tjs: price,
        specifications: parseSpecifications(),
        main_image: $("productMainImage").value.trim() || null,
        is_published: $("productPublished").checked
      };
      if (!payload.name) throw new Error("Укажите название товара.");

      var saved;
      if (state.editingProductId) {
        var update = await state.client.from("catalog_products").update(payload).eq("id", state.editingProductId).select().single();
        if (update.error) throw update.error;
        saved = update.data;
      } else {
        var insert = await state.client.from("catalog_products").insert(payload).select().single();
        if (insert.error) throw insert.error;
        saved = insert.data;
      }

      var enteredPaths = $("productGallery").value.split(/\r?\n/);
      var uploadedPaths = await uploadSelectedFiles(saved.id);
      var paths = uniquePaths([payload.main_image].concat(enteredPaths, uploadedPaths));
      var mainImage = payload.main_image || paths[0] || null;

      if (mainImage !== saved.main_image) {
        var imageUpdate = await state.client.from("catalog_products").update({ main_image: mainImage }).eq("id", saved.id);
        if (imageUpdate.error) throw imageUpdate.error;
      }

      var deleted = await state.client.from("catalog_product_images").delete().eq("product_id", saved.id);
      if (deleted.error) throw deleted.error;
      if (paths.length) {
        var rows = paths.map(function (path, index) {
          return {
            product_id: saved.id,
            storage_path: path,
            alt_text: payload.name,
            sort_order: index,
            is_primary: path === mainImage
          };
        });
        var insertedImages = await state.client.from("catalog_product_images").insert(rows);
        if (insertedImages.error) throw insertedImages.error;
      }

      closeModal();
      await loadData();
      showToast("Товар сохранен.");
    } catch (error) {
      setFormError("productError", errorText(error));
    } finally {
      button.disabled = false;
      button.textContent = "Сохранить товар";
    }
  }

  async function deleteProduct(id) {
    var product = state.products.find(function (item) { return item.id === id; });
    if (!product) return;
    if (!window.confirm("Удалить товар «" + product.name + "»? Это действие удалит запись и галерею из базы.")) return;
    var result = await state.client.from("catalog_products").delete().eq("id", id);
    if (result.error) {
      showToast(errorText(result.error), true);
      return;
    }
    await loadData();
    showToast("Товар удален.");
  }

  function transliterate(value) {
    var map = {
      "а":"a","б":"b","в":"v","г":"g","д":"d","е":"e","ё":"e","ж":"zh","з":"z","и":"i","й":"j","к":"k","л":"l","м":"m","н":"n","о":"o","п":"p","р":"r","с":"s","т":"t","у":"u","ф":"f","х":"h","ц":"c","ч":"ch","ш":"sh","щ":"shch","ъ":"","ы":"y","ь":"","э":"e","ю":"yu","я":"ya"
    };
    return String(value || "").toLocaleLowerCase("ru-RU").split("").map(function (char) {
      return Object.prototype.hasOwnProperty.call(map, char) ? map[char] : char;
    }).join("").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 150);
  }

  function resetCategoryForm() {
    state.categoryEditId = null;
    $("categoryForm").reset();
    $("categoryActive").checked = true;
    $("categorySaveButton").textContent = "Добавить категорию";
    $("categoryCancelButton").classList.add("hidden");
    renderCategoryOptions();
  }

  function editCategory(id) {
    var category = categoryById(id);
    if (!category) return;
    state.categoryEditId = id;
    $("categoryEditId").value = id;
    $("categoryName").value = category.name;
    $("categorySlug").value = category.slug;
    $("categoryParent").value = category.parent_id || "";
    $("categoryActive").checked = Boolean(category.is_active);
    $("categorySaveButton").textContent = "Сохранить категорию";
    $("categoryCancelButton").classList.remove("hidden");
    renderCategoryOptions();
    $("categoryName").focus();
  }

  async function saveCategory(event) {
    event.preventDefault();
    var name = $("categoryName").value.trim();
    var slug = $("categorySlug").value.trim().toLowerCase();
    if (!name || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) {
      showToast("Укажите название и корректный slug латинскими буквами.", true);
      return;
    }
    var payload = {
      name: name,
      slug: slug,
      parent_id: $("categoryParent").value || null,
      is_active: $("categoryActive").checked
    };
    if (payload.parent_id === state.categoryEditId) {
      showToast("Категория не может быть родителем самой себе.", true);
      return;
    }
    var result;
    if (state.categoryEditId) {
      result = await state.client.from("catalog_categories").update(payload).eq("id", state.categoryEditId);
    } else {
      result = await state.client.from("catalog_categories").insert(payload);
    }
    if (result.error) {
      showToast(errorText(result.error), true);
      return;
    }
    resetCategoryForm();
    await loadData();
    showToast("Категория сохранена.");
  }

  async function deleteCategory(id) {
    var category = categoryById(id);
    if (!category || !window.confirm("Удалить категорию «" + category.name + "»?")) return;
    var result = await state.client.from("catalog_categories").delete().eq("id", id);
    if (result.error) {
      showToast("Категория не удалена: " + errorText(result.error), true);
      return;
    }
    await loadData();
    showToast("Категория удалена.");
  }

  async function login(event) {
    event.preventDefault();
    setFormError("loginError", "");
    var button = $("loginButton");
    button.disabled = true;
    button.textContent = "Вход…";
    var result = await state.client.auth.signInWithPassword({
      email: $("loginEmail").value.trim(),
      password: $("loginPassword").value
    });
    button.disabled = false;
    button.textContent = "Войти";
    if (result.error) setFormError("loginError", errorText(result.error));
  }

  async function init() {
    if (!configReady) {
      toggle("connectionNotice", true);
      renderAuth();
      return;
    }
    toggle("connectionNotice", false);
    state.client = window.supabase.createClient(config.url, config.anonKey);
    state.client.auth.onAuthStateChange(function (_event, session) {
      state.session = session;
      renderAuth();
      if (session) {
        window.setTimeout(function () {
          loadData().catch(function (error) {
            showToast("Данные не загружены: " + errorText(error), true);
          });
        }, 0);
      }
    });
    var sessionResult = await state.client.auth.getSession();
    if (sessionResult.error) {
      showToast(errorText(sessionResult.error), true);
      return;
    }
    state.session = sessionResult.data.session;
    renderAuth();
    if (state.session) {
      try { await loadData(); } catch (error) { showToast("Данные не загружены: " + errorText(error), true); }
    }
  }

  $("loginForm").addEventListener("submit", login);
  $("productForm").addEventListener("submit", saveProduct);
  $("categoryForm").addEventListener("submit", saveCategory);
  $("categoryName").addEventListener("input", function () {
    if (!state.categoryEditId && !$("categorySlug").value.trim()) $("categorySlug").value = transliterate($("categoryName").value);
  });
  $("searchInput").addEventListener("input", renderProducts);
  $("categoryFilter").addEventListener("change", renderProducts);
  $("statusFilter").addEventListener("change", renderProducts);
  $("importCatalogButton").addEventListener("click", importExistingCatalog);
  $("refreshButton").addEventListener("click", function () {
    loadData().then(function () { showToast("Данные обновлены."); }).catch(function (error) { showToast(errorText(error), true); });
  });
  $("newProductButton").addEventListener("click", function () { openModal(null); });
  $("signOutButton").addEventListener("click", function () {
    state.client.auth.signOut().then(function () { showToast("Вы вышли из админки."); });
  });
  $("categoryCancelButton").addEventListener("click", resetCategoryForm);

  document.addEventListener("click", function (event) {
    var editProduct = event.target.closest("[data-edit-product]");
    if (editProduct) {
      var product = state.products.find(function (item) { return item.id === editProduct.dataset.editProduct; });
      if (product) openModal(product);
      return;
    }
    var deleteProductButton = event.target.closest("[data-delete-product]");
    if (deleteProductButton) {
      deleteProduct(deleteProductButton.dataset.deleteProduct);
      return;
    }
    var editCategoryButton = event.target.closest("[data-edit-category]");
    if (editCategoryButton) {
      editCategory(editCategoryButton.dataset.editCategory);
      return;
    }
    var deleteCategoryButton = event.target.closest("[data-delete-category]");
    if (deleteCategoryButton) {
      deleteCategory(deleteCategoryButton.dataset.deleteCategory);
      return;
    }
    if (event.target.matches("[data-close-modal]") || event.target === $("productModal")) closeModal();
  });

  init().catch(function (error) {
    showToast("Админка не запустилась: " + errorText(error), true);
  });
}());

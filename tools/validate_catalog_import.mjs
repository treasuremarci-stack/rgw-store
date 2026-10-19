#!/usr/bin/env node
import { access, mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const positional = [];
let strict = false;
let baselinePath = null;

const argumentsList = process.argv.slice(2);
for (let index = 0; index < argumentsList.length; index += 1) {
  const argument = argumentsList[index];
  if (argument === "--strict") {
    strict = true;
  } else if (argument.startsWith("--baseline-products=")) {
    baselinePath = argument.slice("--baseline-products=".length);
  } else if (argument === "--baseline-products") {
    baselinePath = argumentsList[index + 1] || null;
    index += 1;
  } else {
    positional.push(argument);
  }
}

const root = path.resolve(positional[0] || ".");
const outputPath = path.resolve(positional[1] || "catalog-import-report.json");
const errors = [];
const warnings = [];
const info = [];

function problem(list, code, message, details) {
  list.push({ code, message, ...(details ? { details } : {}) });
}

async function readText(relativePath) {
  return readFile(path.join(root, relativePath), "utf8");
}

async function exists(relativePath) {
  try {
    await access(path.join(root, relativePath));
    return true;
  } catch {
    return false;
  }
}

function parseCsvLine(line, separator = ";") {
  const cells = [];
  let cell = "";
  let quoted = false;
  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];
    if (char === '"') {
      if (quoted && line[index + 1] === '"') {
        cell += '"';
        index += 1;
      } else {
        quoted = !quoted;
      }
    } else if (char === separator && !quoted) {
      cells.push(cell);
      cell = "";
    } else {
      cell += char;
    }
  }
  cells.push(cell);
  return cells;
}

function normalized(value) {
  return String(value || "")
    .toLocaleLowerCase("ru-RU")
    .replace(/ё/g, "е")
    .replace(/[^a-zа-я0-9]+/gi, "");
}

function parsePrice(value) {
  const raw = String(value || "").trim();
  if (!raw) return null;
  const normalizedValue = raw.replace(/[\s\u00a0]/g, "").replace(",", ".");
  if (!/^[+-]?(?:\d+(?:\.\d+)?|\.\d+)$/.test(normalizedValue)) return Number.NaN;
  return Number(normalizedValue);
}

function duplicates(values) {
  const seen = new Set();
  const repeated = new Set();
  for (const value of values) {
    if (!value) continue;
    if (seen.has(value)) repeated.add(value);
    seen.add(value);
  }
  return [...repeated];
}

function limited(values, limit = 100) {
  return { count: values.length, items: values.slice(0, limit) };
}

function unique(values) {
  return [...new Set(values)];
}

async function main() {
  const productsText = await readText("products.json");
  let products;
  try {
    products = JSON.parse(productsText);
  } catch (error) {
    problem(errors, "products-json-invalid", "products.json содержит некорректный JSON.", String(error.message));
    products = [];
  }
  if (!Array.isArray(products)) {
    problem(errors, "products-root-not-array", "Корневое значение products.json должно быть массивом.");
    products = [];
  }

  let priceText = "";
  try {
    priceText = await readText("price.csv");
  } catch (error) {
    problem(errors, "price-csv-missing", "Не удалось прочитать price.csv.", String(error.message));
  }

  const productIds = products.map((product) => String(product?.id || "").trim());
  const productSkus = products.map((product) => String(product?.sku || "").trim().toLocaleLowerCase("ru-RU"));
  const duplicateIds = duplicates(productIds);
  const duplicateSkus = duplicates(productSkus);

  if (duplicateIds.length) {
    problem(errors, "duplicate-product-ids", "Найдены дублирующиеся ID товаров.", duplicateIds);
  }
  if (duplicateSkus.length) {
    problem(errors, "duplicate-product-skus", "Найдены дублирующиеся SKU.", duplicateSkus);
  }

  const missingIds = [];
  const missingNames = [];
  const missingCategories = [];
  const missingCharacteristics = [];
  const missingCategoryUrls = [];
  const emptyVerifiedSpecs = [];
  const invalidIdFormat = [];
  const imagePaths = [];
  const productsWithImages = [];
  const productsWithoutImages = [];

  for (const product of products) {
    const id = String(product?.id || "").trim();
    if (!id) missingIds.push(id || "(empty)");
    if (!String(product?.name || "").trim()) missingNames.push(id);
    if (!String(product?.category || "").trim()) missingCategories.push(id);
    if (!/^[A-Za-z0-9][A-Za-z0-9._-]{1,127}$/.test(id)) invalidIdFormat.push(id || "(empty)");
    if (!Array.isArray(product?.catalogFacts) || product.catalogFacts.length === 0) {
      missingCharacteristics.push(id);
    }
    if (!Array.isArray(product?.verifiedSpecs) || product.verifiedSpecs.length === 0) {
      emptyVerifiedSpecs.push(id);
    }
    if (!String(product?.categoryUrl || "").trim()) missingCategoryUrls.push(id);

    const candidateImages = [];
    if (typeof product?.image === "string" && product.image.trim()) candidateImages.push(product.image.trim());
    if (Array.isArray(product?.images)) {
      for (const image of product.images) {
        if (typeof image === "string" && image.trim()) candidateImages.push(image.trim());
      }
    }
    const paths = unique(candidateImages);
    if (paths.length) {
      productsWithImages.push(id);
      imagePaths.push(...paths);
    } else {
      productsWithoutImages.push(id);
    }
  }

  if (missingIds.length) problem(errors, "missing-product-id", "У товаров отсутствует ID.", limited(missingIds));
  if (missingNames.length) problem(errors, "missing-product-name", "У товаров отсутствует название.", limited(missingNames));
  if (missingCategories.length) problem(errors, "missing-product-category", "У товаров отсутствует категория.", limited(missingCategories));
  if (invalidIdFormat.length) problem(errors, "invalid-product-id", "ID не соответствует безопасному формату.", limited(invalidIdFormat));
  if (missingCharacteristics.length) {
    problem(warnings, "missing-characteristics", "У товаров отсутствуют catalogFacts.", limited(missingCharacteristics));
  }
  if (missingCategoryUrls.length) {
    problem(warnings, "missing-category-url", "У товаров отсутствует categoryUrl.", limited(missingCategoryUrls));
  }
  if (emptyVerifiedSpecs.length) {
    problem(warnings, "missing-verified-specs", "У товаров отсутствуют дополнительные verifiedSpecs.", limited(emptyVerifiedSpecs));
  }

  const imageChecks = [];
  for (const image of unique(imagePaths)) {
    const remote = /^https?:\/\//i.test(image);
    const present = remote ? null : await exists(image);
    imageChecks.push({ path: image, remote, present });
    if (!remote && !present) {
      problem(errors, "missing-image-file", "Путь изображения указан, но файл не найден.", image);
    }
  }

  const rows = priceText
    .split(/\r?\n/)
    .filter((line) => line.trim())
    .map((line) => parseCsvLine(line));
  const header = rows[0] || [];
  const priceRows = rows.slice(1);
  const pricedRows = [];
  const sectionRows = [];
  const invalidPriceRows = [];
  const zeroPriceRows = [];

  for (const row of priceRows) {
    const name = String(row[0] || "").trim();
    const value = String(row[1] || "").trim();
    if (!name && !value) continue;
    if (!value) {
      sectionRows.push(name);
      continue;
    }
    const number = parsePrice(value);
    if (!Number.isFinite(number) || number < 0) {
      invalidPriceRows.push({ name, value });
      continue;
    }
    if (number === 0) zeroPriceRows.push(name);
    pricedRows.push({ name, value, number });
  }

  if (header[0] !== "Наименование" || header[1] !== "Цена") {
    problem(warnings, "price-header", "Заголовок price.csv отличается от ожидаемого.", header);
  }
  if (invalidPriceRows.length) problem(errors, "invalid-price-values", "В price.csv найдены некорректные или отрицательные цены.", limited(invalidPriceRows));
  if (zeroPriceRows.length) problem(warnings, "zero-prices", "В price.csv есть нулевые цены.", limited(zeroPriceRows));

  const priceNameIndex = new Map();
  for (const row of pricedRows) {
    const key = normalized(row.name);
    if (key && !priceNameIndex.has(key)) priceNameIndex.set(key, row);
  }
  const duplicatePriceNames = duplicates(pricedRows.map((row) => normalized(row.name)));
  if (duplicatePriceNames.length) problem(warnings, "duplicate-price-names", "В price.csv повторяются названия товаров.", limited(duplicatePriceNames));

  const productsWithoutPriceRows = [];
  const productPriceMatches = [];
  for (const product of products) {
    const productName = normalized(product.name);
    const sku = normalized(product.sku);
    let match = productName ? priceNameIndex.get(productName) : null;
    if (!match) {
      match = pricedRows.find((row) => {
        const priceName = normalized(row.name);
        return (priceName.length > 8 && (productName.includes(priceName) || priceName.includes(productName))) ||
          (sku.length > 6 && priceName.includes(sku));
      }) || null;
    }
    if (match) {
      productPriceMatches.push({ id: product.id, priceName: match.name, price: match.number });
    } else {
      productsWithoutPriceRows.push({ id: product.id, name: product.name });
    }
  }
  if (productsWithoutPriceRows.length) {
    problem(warnings, "product-without-price-row", "Для части товаров не найдено уверенное совпадение в price.csv.", limited(productsWithoutPriceRows));
  }

  const pageFiles = (await readdir(root))
    .filter((file) => /^rgw_page_.*\.html$/i.test(file))
    .sort();
  const pageReports = [];
  const allPageIds = [];
  const pageIdsByFile = new Map();

  for (const file of pageFiles) {
    const html = await readText(file);
    const links = [...html.matchAll(/product\.html\?id=([^"'&<\s]+)/g)]
      .map((match) => decodeURIComponent(match[1]));
    const ids = unique(links);
    pageIdsByFile.set(file, ids);
    allPageIds.push(...ids);
    pageReports.push({
      file,
      bytes: html.length,
      linkCount: links.length,
      cardCount: ids.length,
      duplicateLinkCount: links.length - ids.length,
      ids
    });
  }

  const pageIdSet = new Set(allPageIds);
  const productIdSet = new Set(productIds);
  const linksToMissingProducts = unique(allPageIds.filter((id) => !productIdSet.has(id)));
  const productsWithoutCategoryPageLink = productIds.filter((id) => !pageIdSet.has(id));
  if (linksToMissingProducts.length) {
    problem(errors, "page-link-missing-product", "Страницы категорий ссылаются на отсутствующие товары.", limited(linksToMissingProducts));
  }
  if (productsWithoutCategoryPageLink.length) {
    problem(warnings, "product-not-linked", "Часть товаров не найдена по ссылкам на страницах категорий.", limited(productsWithoutCategoryPageLink));
  }

  const missingCategoryPages = [];
  const productCategoryLinkMismatch = [];
  for (const product of products) {
    const categoryUrl = String(product?.categoryUrl || "").trim();
    if (!categoryUrl) continue;
    if (!pageIdsByFile.has(categoryUrl)) {
      missingCategoryPages.push({ id: product.id, categoryUrl });
      continue;
    }
    if (!pageIdsByFile.get(categoryUrl).includes(product.id)) {
      productCategoryLinkMismatch.push({ id: product.id, categoryUrl });
    }
  }
  if (missingCategoryPages.length) problem(errors, "category-page-missing", "categoryUrl указывает на отсутствующую страницу.", limited(missingCategoryPages));
  if (productCategoryLinkMismatch.length) problem(warnings, "category-page-link-mismatch", "Товар не найден на странице, указанной в categoryUrl.", limited(productCategoryLinkMismatch));

  const categories = {};
  for (const product of products) {
    const name = String(product?.category || "(missing)");
    categories[name] = (categories[name] || 0) + 1;
  }

  let baseline = null;
  if (baselinePath) {
    try {
      const baselineProducts = JSON.parse(await readFile(path.resolve(baselinePath), "utf8"));
      const baselineArray = Array.isArray(baselineProducts) ? baselineProducts : [];
      const baselineIds = unique(baselineArray.map((product) => String(product?.id || "").trim()).filter(Boolean));
      const currentIdSet = new Set(productIds);
      const baselineIdSet = new Set(baselineIds);
      const removed = baselineIds.filter((id) => !currentIdSet.has(id));
      const added = productIds.filter((id) => !baselineIdSet.has(id));
      baseline = { path: path.resolve(baselinePath), baselineCount: baselineIds.length, removedIds: removed, addedIds: added };
      if (removed.length) problem(errors, "product-ids-removed", "Из baseline исчезли существующие ID товаров.", limited(removed));
      info.push({ code: "baseline-compared", message: "ID товаров сравнены с baseline.", details: baseline });
    } catch (error) {
      problem(errors, "baseline-read-failed", "Не удалось прочитать baseline-файл товаров.", String(error.message));
    }
  } else {
    info.push({ code: "baseline-not-provided", message: "Проверка сохранности ID с предыдущей версией не выполнялась: baseline не передан." });
  }

  const report = {
    generatedAt: new Date().toISOString(),
    root,
    strict,
    summary: {
      productCount: products.length,
      uniqueProductIdCount: productIdSet.size,
      categoryCount: Object.keys(categories).length,
      categoryPageCount: pageFiles.length,
      nonEmptyCategoryPageCount: pageReports.filter((page) => page.cardCount > 0).length,
      categoryCardCount: pageReports.reduce((sum, page) => sum + page.cardCount, 0),
      priceCsvRows: priceRows.length,
      priceRowsWithValues: pricedRows.length,
      priceSectionRows: sectionRows.length,
      productsWithPriceMatch: productPriceMatches.length,
      productsWithoutPriceMatch: productsWithoutPriceRows.length,
      productsWithImages: unique(productsWithImages).length,
      productsWithoutImages: productsWithoutImages.length,
      imagePathCount: unique(imagePaths).length,
      missingImageFileCount: imageChecks.filter((image) => image.present === false).length,
      productsWithCatalogFacts: products.length - missingCharacteristics.length,
      productsWithVerifiedSpecs: products.length - emptyVerifiedSpecs.length
    },
    categories,
    duplicateIds,
    duplicateSkus,
    baseline,
    products: {
      missingIds: limited(missingIds),
      missingNames: limited(missingNames),
      missingCategories: limited(missingCategories),
      missingCharacteristics: limited(missingCharacteristics),
      missingCategoryUrls: limited(missingCategoryUrls),
      productsWithoutImages: limited(productsWithoutImages),
      productsWithoutPriceRows: limited(productsWithoutPriceRows)
    },
    priceCsv: {
      header,
      invalidPriceRows: limited(invalidPriceRows),
      zeroPriceRows: limited(zeroPriceRows),
      duplicatePriceNames: limited(duplicatePriceNames),
      sectionRows: limited(sectionRows),
      matchedProducts: limited(productPriceMatches)
    },
    images: { paths: imageChecks },
    categoryPages: pageReports,
    problems: { errors, warnings, info }
  };

  await mkdir(path.dirname(outputPath), { recursive: true });
  await writeFile(outputPath, JSON.stringify(report, null, 2) + "\n", "utf8");

  console.log("АКС: проверка каталога завершена");
  console.log("Товаров: " + report.summary.productCount);
  console.log("Страниц категорий: " + report.summary.categoryPageCount + " (непустых: " + report.summary.nonEmptyCategoryPageCount + ")");
  console.log("Карточек на страницах: " + report.summary.categoryCardCount);
  console.log("Совпадений с price.csv: " + report.summary.productsWithPriceMatch);
  console.log("Товаров с изображениями: " + report.summary.productsWithImages);
  console.log("Ошибок: " + errors.length + "; предупреждений: " + warnings.length);
  console.log("Отчет: " + outputPath);

  if (strict && errors.length) process.exitCode = 1;
}

main().catch((error) => {
  console.error("Ошибка проверки: " + (error.stack || error.message || error));
  process.exitCode = 2;
});

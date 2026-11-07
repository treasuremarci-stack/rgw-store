Warning: truncated output (original token count: 29241)
Total output lines: 921

# PROJECT_STATUS.md — АКС current state

Last updated: 2026-11-04

## Обработка фотографий мониторов Redmi (2026-11-04)

- Проверены все 10 записей Redmi: `monitors-14`–`monitors-23`, включая физические WebP-файлы, карточки `rgw_page_monitors.html`, записи `products.json` и работу универсальной галереи.
- Обработаны все 10 основных фотографий. Файлы сохранены локально как оптимизированные WebP 800×800 на чистом белом фоне; мониторы, подставки, рамки и содержимое экранов сохранены целиком.
- Для `monitors-15` добавлен отсутствовавший `images/products/monitors-15/main.webp`; placeholder удалён из каталога, в `products.json` добавлены `image` и `images`.
- `monitors-15`, `monitors-16`, `monitors-17`, `monitors-18`, `monitors-19` и `monitors-20` получили точные модельные изображения с чистым фоном из найденных карточек товаров. Уже чистые изображения `monitors-14`, `monitors-21` и `monitors-22` пересохранены/нормализованы; `monitors-23` очищен ручной маской по точному исходному G24Q с сохранением изображения на экране.
- Для проверки моделей использованы официальные страницы Xiaomi и страницы/изображения точных моделей X27A, G34WQ, G27U, G25, G27Q 320Hz и G27Q 240Hz; для G24Q использован официальный reference и точный локальный исходник каталога. Внешние URL в HTML и `products.json` не добавлялись.
- Цены, названия, характеристики, ID, SKU, фильтры, сортировка, дизайн, другие категории и фотографии других производителей не изменялись. `product.html` и `product.js` не изменялись: существующая галерея автоматически использует новый локальный `images` для `monitors-15`.

### Проверки этапа

- Проверены 10 физических `main.webp`: формат WebP, размер 800×800, непустое содержимое, белые углы холста и отсутствие дубликатов между моделями.
- Визуально проверены все 10 изображений: чёрные рекламные фоны и внешние надписи удалены; края мониторов и подставок не обрезаны.

## Добавление фотографий GameMax Vista Pro и Aigo C285M (2026-11-04)

- Полностью заменены изображения ровно двух товаров: `cases-003` — GameMax Vista Pro ATX BK WH и `cases-009` — Aigo C285M Black White.
- Для `cases-003` сохранены 6 локальных WebP-файлов: 1 основная фотография из прикреплённого пользователем снимка и 5 дополнительных ракурсов (`front.webp`, `angle.webp`, `side.webp`, `interior.webp`, `back.webp`).
- Для `cases-009` сохранены 4 локальных WebP-файла: 1 основная фотография из прикреплённого пользователем снимка и 3 дополнительных ракурса (`front.webp`, `angle.webp`, `interior.webp`).
- Основные фотографии оставлены именно из вложений пользователя; корпуса полностью помещены в кадр, выровнены по центру и сохранены на чистом белом фоне с равномерными полями.
- Дополнительные изображения GameMax взяты из официальной галереи GameMax Vista A/AW и сверены с чёрно-белой ATX-модификацией по форме корпуса; дополнительные изображения Aigo взяты из галереи AIGO/DARKFLASH C285 Black/White. Рекламные плашки, логотипы магазинов и водяные знаки в подключённые файлы не попали.
- Все физические изображения пересохранены в оптимизированный WebP 800×800. В `products.json` подключены локальные массивы `images`, а в `rgw_page_cases.html` заменены две заглушки на локальные `main.webp`.
- Цены, характеристики, названия, ID, SKU, фильтры, сортировка, дизайн карточек, другие товары и другие категории не изменялись. `product.html` и `product.js` оставлены без изменений: существующая галерея автоматически использует новые массивы фотографий.

### Проверки этапа

- Проверены 10 физических WebP-файлов: формат, размеры, непустое содержимое и отсутствие дубликатов внутри каждой новой галереи.
- Проверены локальные пути `cases-003` и `cases-009` в каталоге и в `products.json`; старые placeholder-иконки для этих двух товаров больше не подключаются.
- Проверены основные изображения и дополнительные ракурсы визуально; все корпуса соответствуют переданным пользователем моделям и цветовым вариантам.

## Полная замена фотографий блоков питания DeepCool, Segotep и GALAX (2026-11-04)

- Обработаны все 4 модели DeepCool в категории «Блоки питания»: `psu-014` PL800D, `psu-015` PN1000D, `psu-016` PF750 и `psu-017` PF600X.
- Для DeepCool обновлены/добавлены 22 локальных WebP-файла: для каждой модели подключены основная фотография и 4–5 дополнительных ракурсов. Использованы точные изображения соответствующих моделей; фотографии других мощностей и серий не подставлялись.
- Для `psu-015` PN1000D основным выбрано точное фото блока вместе с коробкой. Для PL800D и PF750 добавлены точные фото фирменной упаковки отдельными дополнительными кадрами. Для PF600X подходящее фото с реальным блоком и коробкой одновременно не найдено, поэтому оставлены качественные студийные ракурсы самого блока и прозрачный кадр внутреннего устройства.
- Фото пользователя подключены как новые основные изображения без изменения записей товаров: `IMG_4205.png` → `psu-001` GALAX OMEGA GL650S и `IMG_4204.jpeg` → `psu-002` Segotep AN650W.
- Всего обновлено/добавлено 24 физических изображения: 22 для DeepCool и 2 основные фотографии пользователя для GALAX/Segotep. Старые файлы этих товаров больше не подключаются как основные или галерейные изображения.
- `products.json` расширен до 5–6 локальных изображений для каждой модели DeepCool. `product.html` и `product.js` не переписывались: существующая универсальная галерея уже использует массивы `images`.
- В `rgw_page_power_supplies.html` фон области изображения заменён на однотонный `#fff`, а stacking/z-index карточки усилен: плашка категории остаётся поверх изображения при hover. Фильтры, сортировка, количество товаров, карточки и мобильная сетка не менялись.

### Проверки этапа

- Проверены точные ID, SKU, названия и модели `psu-001`, `psu-002`, `psu-014`–`psu-017`; цены, характеристики, ID и SKU не изменялись.
- Проверены все подключённые пути из `products.json`: 29 WebP-файлов непустые, читаются декодерами ImageMagick/FFmpeg, имеют корректный формат и одинаковый рабочий холст 1000×1000 после оптимизации.
- Визуально проверены основные и дополнительные изображения: белый фон, отсутствие обрезанных блоков/коробок, сохранение пропорций и отсутствие повторного использования одного кадра под разными именами.
- Проверена разметка категории: для всех 17 карточек сохранены исходные ID и ссылки `product.html?id=...`; изображения DeepCool, GALAX и Segotep ведут на существующие локальные файлы.
- Остальные товары, категории, `price.csv`, цены, характеристики, фильтры, сортировка и универсальная логика товара не изменялись.

## Замена фотографий корпусов DeepCool CH370 и CG530 4F (2026-11-04)

- Полностью заменены локальные изображения ровно трёх товаров: `cases-010` — DeepCool CH370 WHITE, `cases-011` — DeepCool CH370 BLACK и `cases-012` — DeepCool CG530 4F.
- Для каждого товара сохранены 5 локальных WebP-фотографий: 1 основная и 4 дополнительные (`main.webp`, `01.webp`–`04.webp`). Всего заменено 15 изображений; старые одинаковые логотипные заглушки больше не подключаются.
- Использованы официальные галереи DeepCool: CH370 WH, CH370 и CG530 4F. Для `cases-012` выбран именно чёрный CG530 4F без суффикса WH; CG530 4F WH и CG580 не использовались.
- Фотографии сохранены в исходном чистом белом оформлении производителя, без водяных знаков и рекламных надписей, с полным корпусом в кадре и одинаковым холстом 608×760; пересохранены и оптимизированы в WebP.
- Массивы `images` в `products.json` расширены до пяти файлов для каждой галереи. `rgw_page_cases.html` уже ссылался на правильные локальные `main.webp` этих трёх товаров; пути проверены, а содержимое файлов заменено без изменения разметки, фильтров и дизайна.
- Цены, названия, характеристики, ID, SKU, `price.csv`, другие товары/категории, `product.html` и `product.js` не изменялись. Универсальная галерея `product.html?id=...` использует обновлённые массивы `images` через существующую логику.

### Проверки этапа

- Проверены 15 физических WebP-файлов: непустые, формат WebP, 608×760, уникальные ракурсы внутри каждой модели.
- Проверены записи `cases-010`, `cases-011`, `cases-012` в `products.json`, локальные пути каталога и все 5 ссылок галереи для каждого товара.
- Визуально сверены белый CH370, чёрный CH370 и чёрный CG530 4F; похожие модели и белый CG530 4F WH не подставлялись.
- CSS карточек, внутренние поля 28 px, hover-анимация, фильтры, сортировка и адаптивная разметка не менялись.

## Повторный аудит фотографий материнских плат (2026-11-02)

- Проверены все 16 записей категории «Материнские платы», карточки rgw_page_motherboards.html, поля image/images и физические пути в дереве main.
- 11 товаров уже имеют существующие рабочие локальные изображения; они не изменялись.
- 5 товаров остаются заглушками: mb-005, mb-007, mb-008, mb-009, mb-012. У каждой записи по-прежнему image: null, пустой images[] и нет битого подключённого пути.
- Повторно проверены официальные источники и варианты написания моделей. Для Gigabyte H610 DDR4 найден официальный вариант H610M H DDR4, но название в каталоге не содержит точной модификации; для Gigabyte B760 D5 существует несколько разных DDR5-плат без указанного в каталоге артикула. Для Esonic официальные страницы показывают несколько вариантов H61, а найденные H610DA V41 и H81JEL имеют конкретные SKU, которых нет в записях каталога.
- Новых фотографий добавлено: 0. Похожие платы не подставлялись; пять заглушек сохранены до получения точных заводских обозначений/артикулов.
- Названия, характеристики, ID, SKU, цены, price.csv, каталог, фильтры, JavaScript и существующие фотографии не изменялись.

## Фотографии оперативной памяти (2026-11-02)

- Проверены все 11 товаров категории «Оперативная память»: 3 ранее готовых галереи сохранены, 8 записей были заглушками.
- Добавлены 3 точных локальных WebP-фотографии: ram-002 (Lexar DDR4-3200 SO-DIMM 16 ГБ), ram-003 (Lexar DDR4-3200 SO-DIMM 8 ГБ) и ram-006 (Lexar DDR4-3200 UDIMM 16 ГБ).
- Фото очищены от белого фона с сохранением формы и маркировки модулей; подключены к карточкам каталога и массивам images в products.json.
- Заглушки сохранены для ram-001, ram-004, ram-007, ram-009 и ram-010: у них нет точной серии/артикула или производителя, а Kingston DDR4 и безымянные DDR3 имеют несколько возможных вариантов.
- Цены, характеристики, названия, ID, SKU, price.csv, фильтры, JavaScript, дизайн и другие категории не изменялись.

## Mode
AUTONOMOUS-BY-STAGE.

The agent may decide how to execute the current approved stage, but MUST stop before beginning the next stage.

## Current checkpoint

Universal product-page integration stage completed for all remaining non-empty catalog categories.

The existing `product.html?id=PRODUCT_ID` flow now supports the 12 laptop cards and all 7 current monoblock cards. Product records keep stable identifiers and only confirmed model-specific characteristics; unsupported fields remain omitted. Product pages keep prices as placeholders; photo stage 1 connected the first 10 laptop records to verified local assets where an exact or explicitly documented family match was available.

## Photo stage 1 — first 10 laptops (2026-10-20)

- Audited `laptop-001` through `laptop-010` and recorded every result in `PHOTO_PROGRESS.json`.
- Connected 8 laptop records to 16 optimized local WebP files under `assets/products/PRODUCT_ID/`.
- `laptop-001`, `laptop-002`, `laptop-004`, `laptop-006` and `laptop-010` use exact model/configuration evidence; `laptop-003`, `laptop-005` and `laptop-007` use official family/chassis evidence documented in the progress file.
- `laptop-008` and `laptop-009` intentionally remain placeholders because a downloadable exact-SKU image with a confirmed reuse basis was not established. No similar-model or retailer image was copied.
- Updated only the image fields for these laptop records and the corresponding static catalog image slots. The existing `product.html`/`product.js` gallery logic already supports `images[]`, so it was not rewritten.
- All source files came from official manufacturer product/specification/media pages. `PHOTO_PROGRESS.json` marks the assets for manual rights review; an official page alone is not treated as a reuse licence.
- Prices, product names, IDs, characteristics, `price.csv`, filters, sorting, other categories and the existing product-page architecture were not changed.

## Known project facts
- Repository: `treasuremarci-stack/rgw-store`.
- Default working branch requested by the user: `main`.
- `price.csv` is the assortment source of truth.
- `rgw_multipage_home.html` / current global catalog assets provide the existing catalog/navigation implementation.
- `rgw_page_monoblocks.html` is the current primary visual reference for checkbox/checkmark/row-hover behavior.
- A recent headphones change caused a product-image sizing regression; subsequent work targeted restoring the card/image constraints. Because of that history, image/card regression checks are mandatory when editing category CSS.
- The repository currently contains many `rgw_page_*.html` category pages plus shared catalog/brand assets.
















## Completed in this checkpoint

- Used `rgw_page_access_points.html` as the representative card/image pilot.
- Compared its current card HTML and CSS against `rgw_page_monoblocks.html`.
- Confirmed the same:
  - `.product-card` flex/grid-compatible structure and overflow protection;
  - `.product-image` centered 205px desktop image area with clipped overflow;
  - `.product-image img` 100% constraints, `object-fit:contain`, padding and hover transition;
  - responsive two-column mobile grid and mobile image-height rule.
- Cross-checked `rgw_page_laptops.html` as the existing visual/card reference and confirmed the same effective baseline.
- Kept `rgw_page_headphones.html` avatar handling outside the product-card pilot.
- No category page, product data, prices, catalog, JavaScript, filters, `price.csv` or monoblocks reference was changed.

## Verification

- Re-fetched the pilot page and current `rgw_page_monoblocks.html`, `rgw_page_laptops.html` and `rgw_page_headphones.html` references from `main`.
- Confirmed the pilot card/image selector signatures match the approved baseline.
- Confirmed product-card and product-image wrapper counts remain paired on the pilot.
- Confirmed desktop and mobile-sensitive grid/image rules are present.
- Confirmed the range diff from the previous checkpoint contains only this `PROJECT_STATUS.md` update.
- No propagation batch was necessary because the inventory already showed the baseline on all 54 card-based category pages.

## Completed in the laptop product-page stage

- Added one universal product template: `product.html`.
- Added separate dynamic rendering logic: `product.js`.
- Added `products.json` with all 12 current laptop products, existing project identifiers, placeholder-only price/image state.
- Linked each current laptop card from `rgw_page_laptops.html` to its product page without changing filter values, card data attributes or product assortment.
- Used only confirmed model-specific technical data; unsupported or conflicting fields were omitted.

## Laptop-stage verification

- Confirmed 12 product IDs in the current laptop page are represented once in `products.json`.
- Confirmed each product has a stable ID and a matching model record.
- Confirmed `product.js` parses successfully and handles missing/invalid IDs.
- Confirmed all 12 image fields remain `null`; no foreign image was downloaded.
- Confirmed the laptop card filter/sort script and existing `data-*` attributes were not rewritten.

- Refined the product layout to match the approved brief: wide desktop image area, compact main specifications, grouped full specifications, tabs, and a visual-only «Добавить товар в сборку» block.
- Kept real prices out of `product.html` and `products.json`; the purchase area shows a prepared placeholder.
- Kept real laptop images out of the product page; the image component remains ready for future `object-fit: contain` assets.

- Updated the first-screen composition using the supplied reference: a single white product card now contains vertical thumbnails, a large left gallery, compact right-side specifications, action controls, price placeholder and purchase area.
- Replaced the large emoji placeholder with a lightweight inline SVG laptop icon; the image slot remains compatible with future `img` elements using `object-fit: contain`.
- Kept the build panel directly below the main card and retained the grouped specification tabs.

- Performed a 1440px-style visual check after publication and added the existing site header/container constraints to the product page so the main card is centered instead of touching the viewport edges.
- Enlarged the CSS/SVG placeholder proportionally inside the gallery while keeping it a lightweight placeholder rather than a large emoji.

## Completed in the monoblock universal-product stage

- Validated 7 real cards from `rgw_page_monoblocks.html` and matching `mono-001` through `mono-007` records in `products.json`.
- Kept the current monoblock filter HTML, checkbox animation, row hover, sorting and product-card layout unchanged.
- Made the universal product template category-aware: the category breadcrumb returns to the correct page, the copy uses the current category, and monoblocks receive a dedicated lightweight SVG placeholder.
- Kept monoblock prices and images out of `product.html`; all 7 records remain placeholder-only.
- Confirmed the new monoblock records contain no source URLs, source labels, verification blocks or service messages.


## Completed in the component product-page stage

- Connected 8 video cards, 17 processors and 22 SSD products to the shared `product.html?id=PRODUCT_ID` flow: 47 new records with stable `gpu-XXX`, `cpu-XXX` and `ssd-XXX` identifiers.
- Preserved the existing category pages, filters, sorting, catalog cards, product images and price/availability placeholders; only image and title links were added.
- Extended the shared renderer with component-aware breadcrumbs, SVG placeholders and compact main specifications while keeping the laptop and monoblock paths intact.
- Added only model-level facts tied to the exact catalog configuration; ambiguous component variants keep their catalog facts without guessed details.

## Completed in the motherboard, memory and HDD product-page stage

- Connected 16 motherboard, 11 RAM and 8 HDD catalog cards to the shared `product.html?id=PRODUCT_ID` flow: 35 new records with stable `mb-XXX`, `ram-XXX` and `hdd-XXX` identifiers.
- Preserved filters, sorting, card data attributes, existing images, prices and assortment; added only image/title links on the three category pages.
- Extended the shared renderer with category-aware copy, conservative component facts and lightweight SVG placeholders.
- Kept ambiguous motherboard/RAM/HDD variants conservative: no guessed part numbers or external image/price data were added.

## Completed in the cases, power-supply and cooling product-page stage

- Connected 17 case, 17 power-supply and 21 cooling cards to the shared `product.html?id=PRODUCT_ID` flow: 55 new records with stable `cases-XXX`, `psu-XXX` and `cooling-XXX` identifiers.
- Preserved filters, sorting, card data attributes, existing images, prices and assortment; added only image/title links on the three category pages.
- Extended the shared renderer with category-aware copy, conservative component facts and lightweight SVG placeholders.
- Kept generic/OEM entries conservative and did not invent missing model numbers or external image/price data.

## Completed in the laptop product-page cleanup stage (2026-10-01)

- Removed the unused «В избранное», «Сравнить» and «Поделиться» controls from `product.html`; their unused CSS was removed as well.
- Added one centralized laptop-only user-value normalizer in `product.js` for ordinary color/appearance values. It translates `Pure Silver`, `Cool Silver`, `Silver` to «Серебристый», `Black`, `Midnight Black`, `Carbo Black`, `Mixed Black` to «Чёрный», `White` to «Белый», `Gray`/`Grey`/`Luna Grey` to «Серый», `Blue` to «Синий» and `Gold` to «Золотистый».
- Extended that normalizer for the `Экран` characteristic: `TN`, `ComfyView` and `без сенсора` are removed from the displayed value, while `Touchscreen`, `Touch screen` and `Touch` become «Сенсорный экран» and an empty characteristic is omitted.
- Preserved product names, model numbers, brands, CPU/GPU standards, technical interfaces, prices, images, IDs and the `product.html?id=PRODUCT_ID` architecture.

### Laptop product-page verification

- Checked all 12 laptop IDs from `rgw_page_laptops.html` against `products.json`.
- Confirmed each ID resolves to one product record and each laptop retains its existing category and SKU.
- Confirmed the three action labels are absent from the product template and no dedicated action handlers remain in `product.js`.
- Confirmed the normalization is applied during shared specification rendering, so both main and full specs use the same display value without changing stored product data.
- Checked all 12 laptop screen values: the non-touch terms are removed, while the Dell touch-screen value remains visible as «сенсорный»; no empty screen rows or dangling comma separators are rendered.
- Confirmed `products.json` remains valid and no product records outside the display normalization path were edited.

## Completed in monitor product-page stage (2026-10-12)

- Linked 26 monitor cards to `product.html?id=PRODUCT_ID` via their image and title.
- Added 26 monitor records to `products.json`, preserving existing IDs, catalog titles and available brand/diagonal data.
- Prices and images remain placeholders; no filtering, sorting or price data was changed.
- Checked unique IDs, card link count and valid JSON before commit.

## Completed in the all-remaining-categories product-page stage (2026-10-12)

- Connected all 396 remaining catalog cards from 42 non-empty `rgw_page_*.html` category pages to the shared `product.html?id=PRODUCT_ID` flow.
- Added 396 product records to `products.json` with the existing card IDs/SKUs, category names, exact category return paths, catalog titles, available manufacturers and only facts present in the source cards.
- Extended `product.js` with category-aware breadcrumbs/copy for every remaining category, a conservative fallback for compact main specifications and category-specific emoji placeholders when a real image is absent.
- Preserved the existing design, prices as «Цена уточняется», image placeholders, card filters, sorting, data attributes, and the existing universal product architecture.
- Left `rgw_page_components.html` unchanged because it contains no product cards.

### All-remaining-stage verification

- Confirmed the 396 new IDs are unique and do not overlap the 182 existing product IDs.
- Confirmed each new record has a category, a matching category URL, a stable SKU, a catalog title, a placeholder image state and valid JSON.
- Confirmed each remaining card receives exactly one image link and one title link to its own `product.html?id=PRODUCT_ID`.
- Confirmed no price fields were added and no real images were introduced.


## Laptop photo background correction (2026-10-20)

- Reviewed all 16 existing WebP files linked to the first 10 laptop records. laptop-008 and laptop-009 remain placeholders and have no photo files to process.
- The light-gray catalog/product containers come from existing CSS; the visible white rectangles were embedded in source images.
- Removed only border-connected near-white pixels from affected images. Enclosed white laptop areas were not flood-filled. Dimensions, aspect ratios and visual scale were preserved; no cropping or stretching was introduced.
- Approved non-white/transparent images were left unchanged.

### Files checked

- assets/products/laptop-001/main.webp: transparent exterior (610402 pixels), size 1000x1000
- assets/products/laptop-002/main.webp: unchanged
- assets/products/laptop-003/main.webp: unchanged
- assets/products/laptop-003/side.webp: unchanged
- assets/products/laptop-003/detail.webp: unchanged
- assets/products/laptop-003/angle.webp: unchanged
- assets/products/laptop-004/main.webp: transparent exterior (657559 pixels), size 1000x1000
- assets/products/laptop-004/back.webp: transparent exterior (191558 pixels), size 800x602
- assets/products/laptop-005/main.webp: transparent exterior (747810 pixels), size 1000x1000
- assets/products/laptop-006/main.webp: unchanged
- assets/products/laptop-007/main.webp: unchanged
- assets/products/laptop-007/angle.webp: unchanged
- assets/products/laptop-007/back.webp: unchanged
- assets/products/laptop-010/main.webp: transparent exterior (658638 pixels), size 1000x1000
- assets/products/laptop-010/angle.webp: transparent exterior (659400 pixels), size 1000x1000
- assets/products/laptop-010/back.webp: transparent exterior (964275 pixels), size 1000x1000
- Product names, IDs, SKUs, characteristics, prices, price.csv, catalog markup, product-page logic and card design were not changed in this photo-only stage.

## Next proposed stage

Perform a final repository-wide visual/manual QA pass for the newly connected categories, then handle future real images/prices only when explicitly approved.

## User approval gate

READY FOR FINAL QA.

## Image harvesting checkpoint

Updated: 2026-10-12

The user explicitly authorized processing all categories in this run, overriding the normal stop-after-one-stage rule for this image task.

- Audited all 578 product records across 54 non-empty categories.
- Connected 56 exact-model products to 76 local WebP files under `images/products/PRODUCT_ID/`.
- Added `image` and `images` fields for the connected records and replaced catalog placeholders on 17 category pages.
- Extended `product.html?id=PRODUCT_ID` so thumbnails switch the main image and empty thumbnail slots are hidden when no gallery exists.
- 522 products remain with placeholders because the automated pass could not confirm both the exact model and a safe official image source. They are listed individually in `PRODUCT_IMAGES_REPORT.md`; no similar-model substitutions were made.
- Image integration commit: [d8b9ec815c10ccb141f9249ac499330aeee0eeb5](https://github.com/treasuremarci-stack/rgw-store/commit/d8b9ec815c10ccb141f9249ac499330aeee0eeb5).
- Full per-product audit: `PRODUCT_IMAGES_REPORT.md`.

## Image pilot legal/QA follow-up

Updated: 2026-10-12

- Re-checked the required five-category pilot: laptop, monitor, GPU, router and keyboard.
- Confirmed the exact Lenovo Legion R27fc-30 and MSI GeForce RTX 5060 8G VENTUS 2X (non-OC) models on official manufacturer pages.
- Kept placeholders for the monitor and GPU because no explicit public permission for commercial image reuse was found.
- Clarified that all 56 currently connected products are technically integrated from official manufacturer assets, but still require manual rights clearance; none has an explicit reuse licence documented in the report.
- Verified all 578 unique product records, 76 local WebP paths, gallery switching and catalog rendering on the published GitHub Pages site.
- No product data, prices, characteristics, filters, sorting, homepage or working images were changed in this follow-up.



## Stage 1 — база данных Supabase и основа админки (2026-10-19)

- Подготовлена воспроизводимая миграция `supabase/migrations/202610190001_admin_catalog.sql`.
- Добавлены таблицы категорий, товаров, изображений и белого списка администраторов Supabase Auth.
- Для товаров сохранен строковый ID, совместимый с `product.html?id=PRODUCT_ID`; отдельный триггер блокирует изменение ID после создания.
- Цена хранится как числовое поле `price_tjs numeric(12,2)`; отрицательные и чрезмерные значения отклоняются ограничением базы.
- Добавлены индексы, updated_at-триггеры, ограничение уникальности SKU и один primary-файл на товар.
- RLS-политики разрешают публичное чтение только активных категорий и опубликованных товаров; INSERT/UPDATE/DELETE разрешены только аутентифицированному пользователю из `catalog_admins`.
- Подготовлен bucket `catalog-images` и политики Storage для чтения фотографий и операций администратора.
- Создана статическая русскоязычная админка `/admin/`: вход без публичной регистрации, поиск, фильтры, добавление/редактирование/удаление товаров, цена, JSONB-характеристики, публикация, галерея изображений и управление категориями.
- Секретные ключи не добавлялись. Публичная конфигурация подключения вынесена в `admin/config.js`; пример без ключей остается в `admin/config.example.js`.
- Создан `tools/validate_catalog_import.mjs` и инструкция `tools/README.md`. Инструмент формирует отдельный JSON-отчет и не меняет исходные данные.
- Добавлена инструкция `supabase/README.md` с порядком применения миграции, созданием администратора и проверкой RLS.

### Фактическая проверка исходного каталога перед подготовкой импорта

- В `products.json`: 578 товаров, 578 уникальных ID, дубликатов ID нет.
- В `rgw_page_*.html`: 55 файлов, 54 непустые страницы, 578 уникальных карточек; повторные ссылки внутри карточки не считаются дополнительными товарами.
- В `price.csv`: 649 строк с числовыми ценами и 53 строки-раздела; 565 из 578 названий/SKU имеют уверенное прямое/частичное сопоставление.
- Поле `catalogFacts` присутствует у всех 578 записей, но заполнено у 572; поле `verifiedSpecs` присутствует у 415, из них непустое у 8.
- У 56 товаров есть локальные поля изображений, у 522 остается placeholder-состояние.
- 12 ноутбуков не имеют `categoryUrl`; это сохранено как предупреждение для отдельного решения, исходные файлы не изменены.
- Синтаксис нового Node-инструмента проверен через `node --check`; на тестовом наборе он корректно сформировал отчет и строгий режим не выявил ошибок.
- На момент первоначальной подготовки SQL не выполнялся: подключенного проекта Supabase и его URL/ключей в задаче не предоставлено. После выполнения миграции владельцем публичная конфигурация админки подключена, но авторизация, RLS, Storage и операции админки с реальной базой пока не заявляются полностью проверенными.
- Публичный сайт, `products.json`, `price.csv`, страницы категорий, фильтры, сортировка и `product.html/product.js` в этом этапе не переключались и не изменялись.

## Следующий этап

После отдельного решения владельца: применить миграцию в собственном проекте Supabase, создать первого администратора, выполнить проверку RLS и только затем подготовить контролируемую проверку сопоставления данных перед импортом. Массовый импорт и переключение публичного каталога в Stage 1 не выполнялись.

## Статус этапа

READY FOR SUPABASE OWNER SETUP. Публичная конфигурация подключена; массовый импорт данных не выполнялся.


## Подключение Supabase после выполнения миграции (2026-10-19)

- В `admin/config.js` добавлены URL проекта и публичный publishable key Supabase; секретные и `service_role` ключи не добавлялись.
- Коммит подключения: `d5017d25121347c909ebce1ad0d0b9c8aefd1440`.
- Проверено на опубликованной странице `/admin/`: конфигурация загружается, вместо сообщения «Supabase еще не настроен» отображается защищенная форма входа.
- Импорт товаров и переключение публи…9241 tokens truncated…нялись.
- После коммита и успешной публикации GitHub Pages выполнена браузерная проверка: все семь страниц категорий открылись, карточки и подключённые изображения загрузились; на роутерах проверены выбор и снятие фильтра, на `wifi-5` и `mesh-12` проверено переключение галереи. Прямой тест отдельного мобильного viewport недоступен в текущем CUA; структура и существующий mobile CSS не изменялись.

Детальный список 95 товаров, статусы, пути, источники и итоговые причины пропусков сохранён в `NETWORK_PHOTO_PROGRESS.json`. На текущем проходе точных пропусков не осталось.

## Этап: фотографии раздела «Электропитание» (2026-10-25)

Фактически проверены все пять подкатегорий и все 29 товаров раздела:

| Подкатегория | Страница | Всего | Получили фото сейчас | Заглушки | Новых WebP |
|---|---|---:|---:|---:|---:|
| UPS | `rgw_page_ups.html` | 13 | 7 | 6 | 8 |
| Батареи для UPS | `rgw_page_ups_batteries.html` | 3 | 0 | 3 | 0 |
| Стабилизаторы | `rgw_page_stabilizers.html` | 7 | 4 | 3 | 4 |
| Инверторы | `rgw_page_inverters.html` | 2 | 0 | 2 | 0 |
| Сетевые фильтры / пилоты | `rgw_page_power_strips.html` | 4 | 2 | 2 | 2 |
| **Итого** | **5 страниц** | **29** | **13** | **16** | **14** |

Подключены точные локальные WebP Mercury для Maverick 750/850/1050, Elite 1200/1500/2200/3200, стабилизаторов AVR 1000/2000/3000/5000 и фильтров Mercury 6240U/8240U. Для Maverick 750 добавлен второй ракурс. Пути записаны в `products.json`, а placeholder-слоты соответствующих карточек заменены на `img`. Универсальная страница продолжает использовать существующие `product.html`, `product.js` и `images[]`.

Заглушки сохранены для `ups-1`, `ups-4`, `ups-8`, `ups-9`, `ups-10`, `ups-13`, всех трёх батарей, `stabilizers-4`, `stabilizers-5`, `stabilizers-6`, обоих инверторов и `strips-3`, `strips-4`: для них в текущем проходе не найдено безопасное точное изображение модели без риска подмены другой модификацией, ёмкостью или мощностью. Причины записаны поштучно в `POWER_PHOTO_PROGRESS.json`.

### Проверки этапа

- Все 29 записей электропитания сопоставлены с пятью страницами каталога.
- Все 14 новых файлов физически существуют, открываются Pillow и являются валидными WebP; нулевых файлов и битых путей нет.
- Проверены JSON, локальные пути, наличие `img` в карточках готовых товаров и подключение `images[]` для универсальной галереи.
- `product.html`, `product.js`, цены, характеристики, названия, ID, SKU, `price.csv`, фильтры, сортировка, дизайн и другие категории не изменялись.
- После публикации выполнена браузерная desktop-проверка GitHub Pages: на `rgw_page_ups.html`, `rgw_page_stabilizers.html` и `rgw_page_power_strips.html` реальные изображения загружаются в карточках; `product.html?id=ups-2` открывается и показывает галерею с двумя ракурсами, переключение второго изображения проверено. Для всех 29 товаров дополнительно выполнена программная проверка путей и HTML-связей. Отдельный mobile viewport в текущем CUA недоступен; мобильный CSS и структура не изменялись. Перед коммерческим использованием внешних исходников требуется отдельная проверка прав.

## Этап: фотографии раздела «Видеонаблюдение» (2026-10-25)

Фактически проверены все существующие подкатегории раздела и весь ассортимент: 4 подкатегории и 9 товаров. В исходном состоянии у этих товаров не было подключённых локальных фотографий; теперь для всех 9 товаров добавлены точные изображения, а placeholder-слоты карточек заменены на реальные локальные `img`.

| Подкатегория | Страница | Всего | Получили фото | Файлов WebP |
|---|---|---:|---:|---:|
| IP-камеры | `rgw_page_ip_cameras.html` | 4 | 4 | 6 |
| Аналоговые камеры | `rgw_page_analog_cameras.html` | 2 | 2 | 4 |
| Домофоны | `rgw_page_intercoms.html` | 2 | 2 | 3 |
| Видеорегистраторы | `rgw_page_video_recorders.html` | 1 | 1 | 2 |
| **Итого** | **4 страницы** | **9** | **9** | **15** |

Для каждого товара подключены `image` и `images[]` в `products.json`, а основные изображения подключены в соответствующих карточках каталога. Добавлены следующие локальные галереи: `ip_cameras-1`, `ip_cameras-2`, `ip_cameras-3`, `ip_cameras-4`, `analog_cameras-1`, `analog_cameras-2`, `intercoms-1`, `intercoms-2`, `video_recorders-1`. Точные модели подтверждались официальными материалами Dahua/Imou; для отдельных вариантов использованы страницы точной модели у надёжных дистрибьюторов. Поштучные пути и источники сохранены в `SURVEILLANCE_PHOTO_PROGRESS.json`.

### Проверки этапа

- Все 4 реально существующие страницы раздела и все 9 ID сопоставлены с `products.json`; дополнительных surveillance-подкатегорий в каталоге не обнаружено.
- Все 15 новых файлов физически существуют, являются непустыми валидными WebP и проверены через Pillow; пути основных и дополнительных изображений проверены программно.
- В карточках всех четырёх страниц placeholder-слоты заменены на локальные изображения с правильными `alt` и путями `images/products/<ID>/main.webp`.
- Проверены JSON-файлы, `node --check product.js`, `git diff --check`, связи `image`/`images[]`, структура универсальной галереи и локальная загрузка страниц через HTTP-сервер.
- `product.html`, `product.js`, цены, характеристики, названия, ID, SKU, `price.csv`, фильтры, сортировка, дизайн и фотографии других категорий не изменялись.
- После публикации выполнена браузерная desktop-проверка страниц раздела и нескольких универсальных карточек с переключением дополнительных изображений; отдельный мобильный viewport в текущем CUA недоступен, существующие mobile-правила не изменялись.

Детальный список 9 товаров, статусы, источники, пути и результаты проверки сохранён в `SURVEILLANCE_PHOTO_PROGRESS.json`. Перед коммерческим использованием внешних исходников требуется отдельная проверка прав.

## Этап: фотографии раздела «Серверное и сетевая инфраструктура» (2026-10-25)

Фактически проверены все 7 существующих подкатегорий и все 43 товара раздела. Подкатегории определены по `rgw_global_catalog.js` и актуальным полям `category`/`categoryUrl` в `products.json`.

| Подкатегория | Страница | Всего | Уже было готово | Добавлено сейчас | Готово после запуска | Новых WebP |
|---|---|---:|---:|---:|---:|---:|
| Серверные шкафы | `rgw_page_server_racks.html` | 14 | 0 | 0 | 0 | 0 |
| Патч-панели | `rgw_page_patch_panels.html` | 2 | 0 | 0 | 0 | 0 |
| Коннекторы и розетки | `rgw_page_connectors_outlets.html` | 3 | 0 | 0 | 0 | 0 |
| Сетевые кабели | `rgw_page_network_cables.html` | 8 | 0 | 2 | 2 | 2 |
| IP-телефония | `rgw_page_ip_telephony.html` | 10 | 1 | 9 | 10 | 9 |
| Мини-АТС | `rgw_page_mini_pbx.html` | 1 | 0 | 1 | 1 | 1 |
| Сетевые аксессуары | `rgw_page_network_accessories.html` | 5 | 0 | 0 | 0 | 0 |
| **Итого** | **7 страниц** | **43** | **1** | **12** | **13** | **12** |

Для точных моделей Grandstream подключены официальные изображения GRP2602, GRP2601, UCM6302, DP755, GRP2604P, GXP2170, GXP2200EXT, DP750 и GXP1615. Для `Плата KX-TE82480` использована точная карточка платы Panasonic, а для двух явно брендированных кабелей MERCURY — точные карточки Mercury CAT6 SFTP/UTP 305 м. Все новые изображения сохранены локально как `images/products/<ID>/main.webp`, подключены в `products.json` и в карточки соответствующих страниц каталога. Существующий `ip_telephony-6` оставлен без изменений.

Заглушки сохранены для 30 товаров: всех 14 безымянных серверных шкафов, двух generic-патч-панелей, трёх generic-коннекторов, шести кабелей без однозначного производителя/доступного точного ассета и пяти generic-сетевых аксессуаров. По этим товарам точную модель нельзя подтвердить по текущим данным, поэтому похожие изображения не подставлялись. Поштучные причины и источники сохранены в `SERVER_INFRA_PHOTO_PROGRESS.json`.

### Проверки этапа

- Все 43 ID сопоставлены с семью фактическими страницами раздела и `products.json`.
- Все 12 новых WebP-файлов физически существуют, непустые и открываются как изображения; основные пути проверены программно.
- Новые изображения подключены в `products.json`, карточках `rgw_page_network_cables.html`, `rgw_page_ip_telephony.html` и `rgw_page_mini_pbx.html`; универсальная галерея продолжает использовать существующие `product.html`, `product.js` и `images[]`.
- Цены, характеристики, названия, ID, SKU, `price.csv`, фильтры, сортировка, дизайн, универсальный шаблон и фотографии завершённых категорий не изменялись.
- Для точных совпадений сохранены URL страниц/ассетов источников; перед коммерческим использованием внешних исходников требуется отдельная проверка прав.
- После публикации выполнена браузерная проверка опубликованных GitHub Pages: все 7 страниц категорий и все 43 страницы `product.html?id=...` открылись; у 13 товаров с подключёнными изображениями основные WebP загрузились без битых изображений, а у остальных 30 сохранены ожидаемые заглушки. Отдельный мобильный viewport в текущем CUA недоступен; мобильная разметка и CSS не изменялись.

## Этап: фотографии раздела «Аксессуары и хранение» (2026-10-25)

Фактическая инвентаризация по `products.json`, `rgw_global_catalog.js` и страницам каталога выявила 10 подкатегорий и 89 товаров:

| Подкатегория | Страница | Всего | Уже готово | Добавлено сейчас | Готово после запуска | Без точного фото |
|---|---|---:|---:|---:|---:|---:|
| Внешние HDD/SSD | `rgw_page_external_storage.html` | 16 | 1 | 14 | 15 | 1 |
| Флешки | `rgw_page_flash_drives.html` | 8 | 0 | 8 | 8 | 0 |
| Карты памяти | `rgw_page_memory_cards.html` | 4 | 0 | 4 | 4 | 0 |
| Кабели | `rgw_page_cables.html` | 1 | 0 | 1 | 1 | 0 |
| Переходники | `rgw_page_adapters.html` | 5 | 3 | 2 | 5 | 0 |
| USB-хабы | `rgw_page_usb_hubs.html` | 8 | 4 | 4 | 8 | 0 |
| Сумки и рюкзаки | `rgw_page_bags.html` | 20 | 0 | 6 | 6 | 14 |
| DVD-приводы | `rgw_page_dvd_drives.html` | 2 | 0 | 0 | 0 | 2 |
| Проекторы и экраны | `rgw_page_projectors_screens.html` | 19 | 0 | 3 | 3 | 16 |
| Прочие аксессуары | `rgw_page_other_accessories.html` | 6 | 0 | 0 | 0 | 6 |
| **Итого** | **10 страниц** | **89** | **8** | **42** | **50** | **39** |

Для 42 точных моделей добавлен 1 основной локальный WebP-файл на товар; подтверждённых дополнительных ракурсов в доступных источниках не найдено, поэтому массив `images[]` не заполнялся непроверенными дублями. Подключены внешние HDD/SSD Toshiba, WD, Seagate и Lexar; флешки SanDisk, Lexar, ADATA и Samsung; карты Lexar; кабель Baseus; адаптеры Baseus/Cudy; USB-хабы Baseus/Cudy; рюкзаки 90fen/Xiaomi/NINETYGO; проекторы Optoma W371 и Epson CO-WX02/EF-12.

Заглушки сохранены без подмены похожими товарами для:

- `acc-external_storage-16` — Transcend HDD 2TB без серии/артикула;
- `acc-bags-1..5`, `acc-bags-11..17`, `acc-bags-19..20` — нет однозначной модели или артикула;
- `acc-dvd_drives-1..2` — generic DVD-приводы без производителя/модели;
- `acc-projectors_screens-1..9`, `acc-projectors_screens-12..13`, `acc-projectors_screens-15..19` — экраны, стойки, электронная доска и generic-проектор без подтверждаемого точного ассета;
- `acc-other_accessories-1..6` — generic-бокс, DVD-планка и коврики без точной модели.

Источники и поштучные пути сохранены в `ACCESSORIES_STORAGE_PHOTO_PROGRESS.json`; для сторонних каталогов и официальных ассетов перед коммерческим использованием требуется отдельная проверка прав. В карточках восьми страниц каталога заменены только placeholder-слоты на соответствующие `images/products/<ID>/main.webp`; фильтры, карточки, цены, характеристики, названия, ID, SKU, `price.csv`, универсальные `product.html`/ `product.js` и остальные категории не менялись.

Выполнены локальные проверки JSON, путей и WebP. После публикации GitHub Pages через CUA проверены все 10 страниц подкатегорий: 50 подключённых изображений загрузились после прокрутки lazy-load без ошибок; проверены все 50 соответствующих `product.html?id=...`, имя товара и основной `main.webp` определились корректно. Отдельный мобильный viewport в текущем браузере недоступен; мобильные CSS и разметка не менялись.

## Laptop photo correction — Lenovo IdeaPad Slim 3 15IRH10 and MSI Crosshair 16 AI (2026-11-01)

- `laptop-005` (`LENOVO IP SLIM3 15IRH10`): removed only the lower-right Intel badge with a narrow right-edge crop. The laptop body, original angle, colors and product link remain unchanged.
- `laptop-011` (`MSI CROSSHAIR 16 AI`): replaced the main image and all three additional images that carried CompuMarts branding with four clean assets from MSI's official Crosshair 16 HX AI D2XW product page. The main asset is transparent; gallery assets contain no third-party branding.
- Audited the laptop records for MSI branding: `laptop-011` is the only MSI laptop in the current catalog, so no other MSI laptop image required replacement.
- Kept product records, characteristics, prices, IDs, SKUs, `price.csv`, `product.html`, `product.js` and all non-laptop categories unchanged; changed only the five local image path strings and corresponding catalog image references to clean filenames so GitHub Pages cannot serve the old cached assets.
- QA: inspected all five changed WebP assets, verified non-empty valid WebP files, checked the unchanged catalog paths, and verified the laptop data/progress JSON. Official-source reuse still requires the project's existing manual rights review.

## Publication cache follow-up (2026-11-01)

- GitHub Pages was still serving the old same-name image URLs from its CDN cache after the successful deployment. To make the correction visible immediately, only the five affected local image filenames/references were changed to clean filenames with a -clean suffix.
- The old Lenovo and four old MSI files were removed from the repository; the new files are the same inspected clean assets from the preceding correction commit.
- No product characteristic, title, price, ID, SKU, filter, layout, product-page logic or other-category file was changed.


## Laptop missing-photo recheck — HP 15-fd0183wm and Dell LDC15250 (2026-11-01)

- Catalog verification found the exact existing records laptop-008 (HP 15-FD0183WM, model 15-FD0183WM) and laptop-009 (DELL LDC15250-5434BLK-PUS, model LDC15250-5434BLK-PUS); no products were created and no titles, specifications or prices were changed.
- HP: added the official product image for HP 15-fd0183wm (B4GZ5UA) as assets/products/laptop-008/main-official.webp.
- Dell: mapped the exact catalog part to the official Dell 15 / DC15250 family and added the clean official Carbon Black chassis image as assets/products/laptop-009/main-official.webp; the exact SKU mapping was used only for verification, not as an image source.
- Updated only the two existing records' image/images fields and the two corresponding laptop catalog image slots. price.csv, prices, characteristics, IDs, SKUs, filters, card design and all other categories remain unchanged.
- Local QA: both files are non-empty WebP with transparency, preserve aspect ratio and include padding; JSON paths and the two catalog references were checked. Official-source reuse remains subject to the project's existing manual rights review.


## MSI Crosshair 16 AI — main screen image correction (2026-11-01)

- For existing catalog item laptop-011 (MSI CROSSHAIR 16 AI; platform Crosshair 16 HX AI D2XWX), replaced only the main image with the official MSI hero asset main-screen.webp.
- The new 1000×800 transparent WebP contains the official red/orange promotional display image and MSI dragon shield on the laptop screen; the laptop is not distorted or stretched.
- The three additional gallery files and their paths remain unchanged. Product name, characteristics, price, ID, SKU, price.csv, card layout and all other categories remain unchanged.
- The exact official source and new path are recorded in PHOTO_PROGRESS.json.


## Этап: фотографии видеокарт в заводских коробках (2026-11-01)

Фактически проверены все 8 товаров страницы `rgw_page_gpus.html`. Четыре корректных основных фото с заводской упаковкой сохранены без замены: `gpu-001`, `gpu-002`, `gpu-007` и `gpu-008`. Для `gpu-003`, `gpu-004`, `gpu-005` и `gpu-006` добавлены новые локальные WebP-фото точных коробок на белом фоне; старые изображения карт без упаковки больше не используются как основные фото. Для `gpu-003`, `gpu-004` и `gpu-008` дополнительные ссылки на снимки карт без коробки отключены, чтобы галерея также не нарушала новый стандарт.

Подтверждение моделей: официальные страницы GALAX указывают точные варианты RTX 5060 1-Click OC V2 (код 56NSN8MDDXBO), RTX 5050 1-Click OC, RTX 5080 1-Click OC и RTX 3060 1-Click OC; для фото упаковки использованы чистые изображения без водяных знаков и стороннего брендинга с точных карточек моделей. Пути сохранены в `COMPONENTS_PHOTO_PROGRESS.json`.

### Проверки этапа

- Проверены все 8 карточек видеокарт, основные пути в `products.json` и ссылки `rgw_page_gpus.html`.
- Добавлены 4 новых WebP-файла 1000×1000 с белым фоном, пропорции сохранены, коробки полностью помещаются с полями.
- Проверены локальные файлы, формат WebP, непустое содержимое и отсутствие битых путей.
- Цены, характеристики, названия, ID, SKU, `price.csv`, фильтры, сортировка, дизайн карточек и другие категории не изменялись.
- Мобильная проверка выполнялась по неизменённой адаптивной разметке; отдельный мобильный viewport в текущем браузере недоступен.

## Нормализация фона фотографий видеокарт (2026-11-01)

Обработаны только 8 товаров страницы «Видеокарты», у которых уже использовались фотографии заводских коробок (в отдельных снимках коробка показана вместе с видеокартой). Все 8 локальных WebP пересохранены с ровным белым фоном: прозрачные исходники также аккуратно сведены на белый, без обрезки упаковки, растягивания или изменения элементов её дизайна. Размеры исходников сохранены.

Водяные знаки не удалялись; на проверенных изображениях посторонних водяных знаков не обнаружено. Названия, цены, характеристики, ID, SKU, products.json, фильтры, карточки, другие категории и price.csv не изменялись.

### Проверки этапа

- Обработано и заменено: 8 изображений (gpu-001–gpu-008).
- Проверены визуальный результат, формат WebP, размеры, белые углы и отсутствие обрезанных коробок.
- Проверены загрузка восьми изображений в каталоге и страницы товаров с галереями; активные пути остались рабочими.
- Отдельный мобильный viewport в текущем браузере недоступен; CSS, размеры карточек и адаптивная разметка не менялись.

## Прозрачный фон фотографий видеокарт (2026-11-02)

Повторно обработаны только 8 активных фотографий категории «Видеокарты» (`gpu-001`–`gpu-008`). Ровные белые подложки удалены flood-fill обработкой по внешнему фону; файлы сохранены в WebP с настоящим альфа-каналом. Коробки и видеокарты сохранены полностью, без обрезки, растягивания и изменения надписей или дизайна упаковки. Пути товаров и данные каталога не менялись.

### Проверки этапа

- Проверены и обработаны: 8 изображений.
- Проверены прозрачные углы, отсутствие прямоугольной подложки, пропорции и размеры исходных файлов.
- Визуально проверены превью на контрастном фоне; активные изображения каталога и галерей загружаются.
- Названия, цены, характеристики, ID, SKU, фильтры, сортировка, карточки, другие категории и price.csv не изменялись.
- Отдельный мобильный viewport в текущем браузере недоступен; CSS и адаптивная разметка не менялись.

## Единый стандарт прозрачных фотографий процессоров (2026-11-02)

Проверены все 17 товаров категории «Процессоры» на `rgw_page_processors.html` и их активные изображения `images/products/cpu-*/main.webp`. 16 существующих изображений пересохранены в WebP с настоящим альфа-каналом: удалён внешний белый/серый фон, сохранены маркировка, пропорции, исходный холст и поля вокруг процессора. Прямоугольные подложки, растягивание и обрезка не добавлялись.

Для `cpu-008` (Core Ultra 5 245KF), `cpu-009` (Core Ultra 7 265K) и `cpu-017` (Core Ultra 5 225F) коробочные композиции заменены на точные снимки самих процессоров. Для `cpu-010` (Core Ultra 9 285K) и `cpu-011` (Core i3-9100F) использованы чистые снимки точных моделей без посторонней отметки. `cpu-005` (каталожное название «I3-3260») оставлен с заглушкой: подтверждённого изображения именно этой модели не найдено, а найденный Intel Pentium G3260 не является допустимой заменой.

### Проверки этапа

- Проверены 17/17 товаров и пути изображений в `products.json`, `rgw_page_processors.html` и `product.html?id=...`.
- Визуально проверены все 16 WebP на белом, сером и тёмном фоне: углы прозрачны, коробок и цветных прямоугольных фонов нет.
- Файлы проверены на непустое содержимое, формат WebP и альфа-канал; пути сохранены без изменений.
- Названия, цены, характеристики, ID, SKU, наличие, фильтры, сортировка, JavaScript, карточки, другие категории и `price.csv` не изменялись.
- Отдельный мобильный viewport в текущем браузере недоступен; адаптивная разметка и размеры карточек не менялись.


## Повторное заполнение фотографий оперативной памяти (2026-11-02)

- Повторно проверены все 11 товаров категории «Оперативная память» и фактические заглушки/пути в каталоге.
- Без рабочей фотографии были `ram-001`, `ram-004`, `ram-007`, `ram-009`, `ram-010`; для каждого добавлена одна локальная фотография WebP с прозрачным фоном.
- Не изменялись корректные фотографии `ram-002`, `ram-003`, `ram-005`, `ram-006`, `ram-008`, `ram-011`.
- Для `ram-001` использована официальная фотография семейства Lexar THOR DDR4 UDIMM (16 ГБ, DDR4-3200, радиатор); артикул в каталоге отсутствует.
- Для безымянных `ram-004` и `ram-007` использованы чистые фотографии обычных DDR3-модулей с соответствующими объёмами 8 ГБ и 4 ГБ; брендовые модули не подставлялись.
- Для `ram-009` и `ram-010` использованы изображения Kingston с публично подтверждёнными артикулами KVR32N22D8/16 (16 ГБ DDR4-3200) и KVR26N19S8/8 (8 ГБ DDR4-2666); эти артикулы отсутствуют в исходных данных каталога.
- Фотографии подключены в `products.json`, карточки `rgw_page_ram.html` и универсальную галерею через существующую логику `product.html?id=...`.
- Проверены локальные WebP-файлы: они непустые, с альфа-каналом, без прямоугольного фона; `price.csv`, цены, характеристики, ID, SKU, фильтры и другие категории не изменялись.

## SSD — дополнение фотографий (2026-11-02)

Проверены все 22 товара категории «SSD». У 10 товаров уже были рабочие локальные изображения — они сохранены без замены. Для 12 товаров с заглушками добавлены реальные предметные фотографии в формате WebP и подключены к каталогу и универсальной галерее: ssd-001, ssd-002, ssd-003, ssd-008, ssd-009, ssd-013, ssd-014, ssd-017, ssd-018, ssd-019, ssd-020, ssd-022.

Для записей без серии/артикула в названии каталога использованы официальные семейства, совпадающие по бренду, форм-фактору, интерфейсу и ёмкости: Lexar NS100 (2,5\" SATA), Lexar NM620 (M.2 2280 NVMe) и Samsung PM9C1b (M.2 2280 NVMe 256 ГБ). Названия, характеристики, ID, SKU, цены и price.csv не изменялись. Для Kingston 1 ТБ и 480 ГБ использованы точные варианты NV2 SNV2S/1000G и A400 SA400S37/480G.

Обновлены `products.json`, `rgw_page_ssd.html`, `COMPONENTS_PHOTO_PROGRESS.json` и этот статус. Визуально файлы проверены локально: WebP, альфа-канал, пропорции сохранены, товар полностью помещается в изображение.


## Блоки питания — дополнение фотографий (2026-11-02)

Проверены все 17 товаров категории «Блоки питания» и фактические файлы/заглушки. Десять корректных локальных наборов сохранены без изменений. Для трёх товаров добавлены реальные локальные WebP: `psu-006`, `psu-008`, `psu-013`; каждый подключён к каталогу и универсальной галерее.

- `psu-006` — Vision 550 W: предметное изображение подтверждено по бренду и мощности; в каталоге нет серии/артикула, ограничение зафиксировано.
- `psu-008` — Vision 750 W OEM: предметное изображение Master Vision ATX-750W подтверждено по бренду и мощности; точный артикул в каталоге отсутствует.
- `psu-013` — Cooler Master 600 W: использовано предметное изображение модели с совпадающими брендом и мощностью.
- `psu-007`, `psu-009`, `psu-010`, `psu-012` оставлены заглушками: точное совпадение серии/артикула не подтверждено, поэтому похожие блоки питания не подставлялись.

Новые файлы: `images/products/psu-006/main.webp`, `images/products/psu-008/main.webp`, `images/products/psu-013/main.webp`, `POWER_SUPPLIES_PHOTO_PROGRESS.json`. Обновлены `products.json`, `rgw_page_power_supplies.html`, `COMPONENTS_PHOTO_PROGRESS.json` и этот статус. Цены, `price.csv`, характеристики, ID, SKU, логика каталога, фотографии других категорий и дизайн не изменялись.


## Нормализация фотографий мышек (2026-11-07)

- Обработаны основные фотографии 11 товаров категории «Мыши»: `mice-3` (Logitech M196), `mice-4` (Logitech M330), `mice-5` (Logitech M650), `mice-7` (Logitech M705), `mice-8` (Logitech M187), `mice-10` (GALAX Slider-03), `mice-11` (Logitech M280), `mice-12` (Logitech Pebble), `mice-13` (Logitech M170), `mice-14` (Logitech M235), `mice-15` (Logitech M650L).
- Каждый `main.webp` пересохранён с уменьшением объекта примерно на 25% внутри исходного холста: мышь полностью помещается в кадр и получает равномерные поля.
- Фоны приведены к однотонному белому `#FFFFFF`; сохранены оригинальные цвета, логотипы, пропорции и комплектные USB-приёмники там, где они были частью исходной предметной фотографии.
- `products.json`, названия, цены, характеристики, ID, SKU, фильтры, JavaScript и фотографии остальных товаров не изменялись.

### Проверки этапа

- Проверены 11 локальных WebP: файлы непустые, декодируются ImageMagick, имеют исходные размеры холста и непрозрачный белый фон.
- Проверены пути изображений в опубликованном `rgw_page_mice.html`; все 11 целевых WebP загружаются с корректными натуральными размерами.
- Визуально проверены каталог и `product.html?id=mice-15`; фотографии не обрезаются и не выходят за область изображения.


## Нормализация фотографий веб-камер (2026-11-07)

- Обработаны ровно две модели категории «Веб-камеры»: `webcams-1` — Вебка Logitech C922 и `webcams-2` — Вебка Logitech C920 Pro.
- Для обеих фотографий фон заменён на непрозрачный однотонный белый `#FFFFFF`; сохранены оригинальные корпуса, объективы, крепления, маркировка, пропорции и ориентация.
- Визуальный масштаб уменьшен непосредственно внутри изображений: примерно на 29% для C922 и на 20% для C920 Pro. Холсты сохранены исходными: 700×601 и 1000×1000 соответственно; устройства полностью помещаются в кадр и имеют равномерные поля.
- Изменены только `images/products/webcams-1/main.webp` и `images/products/webcams-2/main.webp`, а также эта запись статуса. `products.json`, `rgw_page_webcams.html`, `product.html`, `product.js`, цены, характеристики, фильтры, карточки и остальные товары не изменялись.

### Проверки этапа

- Проверены оба файла: непустые WebP, корректные размеры холста, непрозрачный белый фон и отсутствие обрезанных частей устройств.
- Проверены существующие локальные пути в карточках категории и в `products.json`; подключение галереи `product.html?id=webcams-1` / `webcams-2` осталось без изменений.
- Визуально проверены оба результата: устройства центрированы, масштаб согласован, белые отступы добавлены; CSS, размеры карточек и адаптивная разметка не менялись.

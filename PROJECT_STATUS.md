# PROJECT_STATUS.md — АКС current state

Last updated: 2026-10-20

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
- Импорт товаров и переключение публичного каталога на Supabase не выполнялись.
- Для завершения проверки владелец должен создать пользователя Supabase Auth и добавить его UUID в `public.catalog_admins`; после этого можно проверить реальный вход, RLS, загрузку товаров и Storage.


## Подготовка импорта существующего каталога без цен (2026-10-19)

- В админку добавлена защищенная кнопка «Импорт каталога без цен».
- Импорт читает текущий `products.json`, создает 54 категории и добавляет 578 товаров с сохранением исходных ID.
- Для всех новых записей `price_tjs` остается `NULL`; повторный запуск пропускает существующие ID и не стирает будущие цены.
- Существующие изображения и характеристики сохраняются в полях товара и галерее.
- Код проверен на синтаксис; фактический импорт еще не запускался, пока владелец не войдет в админку и не подтвердит действие.
- Изменения: `admin/index.html` — `86a54711cd9161241b64aea3f865a77581bad54e`; `admin/admin.js` — `c857b402b304f2939921f37919ea439ea404aa9c`.

## Laptop photo stage 2 — remaining non-placeholder laptops (2026-10-20)

- Обработаны только laptop-011 и laptop-012.
- Файлы и записи laptop-001…laptop-010 не изменялись.
- laptop-008 и laptop-009 оставлены заглушками по заданному ограничению.
- Фильтры, карточки кроме image-slot, характеристики, цены, SKU, price.csv и архитектура product.html?id=PRODUCT_ID не изменялись.
- laptop-011: exact product-page source; добавлено 4 уникальных WebP: assets/products/laptop-011/main.webp, assets/products/laptop-011/angle.webp, assets/products/laptop-011/back.webp, assets/products/laptop-011/detail.webp.
- laptop-012: exact configuration fallback; добавлено 2 WebP: assets/products/laptop-012/main.webp, assets/products/laptop-012/angle.webp.
- Для laptop-011 использована точная страница MSI Crosshair 16 HX AI D2XWGKG-271NG; для laptop-012 — точная карточка Lenovo IdeaPad Slim 3 15IRU8, 82X700EDUS.
- Изображения скачаны в репозиторий, приведены к WebP до 1000 px для основного кадра и до 1400 px для дополнительных; краевой белый фон удаляется только из связной области фона, чтобы не затрагивать детали корпуса.
- Техническая готовность следующего этапа: каталог ноутбуков и универсальная страница уже используют локальные image/images; для остальных категорий отдельные фото пока не подключались.
- Права на повторное коммерческое размещение внешних assets требуют отдельной ручной проверки.


## Monoblock photo stage (2026-10-20)

Base stage commit: 9ec8a39d671655307017538c35ad6e2e3dda73bc. Final photo correction replaced rejected non-product assets. Laptop files and PHOTO_PROGRESS.json remain untouched.
All 7 monoblock records were checked. Only exact model/configuration sources were retained; similar models, generic banners and logos were excluded.

### Results

- mono-001 — Моноблок HP 200 G4 AIO: complete, 6 WebP; main photo assets/products/mono-001/main.webp.
- mono-002 — Моноблок HP 290: placeholder; reason: В каталоге указано только «HP 290» без поколения, артикула и точного форм-фактора; подтверждённое фото именно этой AIO-модификации не найдено.
- mono-003 — Моноблок HP AIO 27-CR0008L: complete, 3 WebP; main photo assets/products/mono-003/main.webp.
- mono-004 — Моноблок Lenovo IdeaCentre 27IRH9, Core i7: complete, 4 WebP; main photo assets/products/mono-004/main.webp.
- mono-005 — Моноблок Lenovo IdeaCentre 27IRH9, Core i5: complete, 5 WebP; main photo assets/products/mono-005/main.webp.
- mono-006 — Моноблок MSI Pro AP272P AIO 27: complete, 5 WebP; main photo assets/products/mono-006/main.webp.
- mono-007 — Моноблок HP AIO 27-CR0156NH: complete, 3 WebP; main photo assets/products/mono-007/main.webp.

### Checks

Changed product image links only for monoblock records with verified images; product names, IDs, SKUs, characteristics, prices and filters were preserved.
The monoblock catalog card paths remain the same main.webp slots, and the existing product.html?id=mono-XXX gallery architecture remains unchanged.
All replacement assets are WebP, are not artificially enlarged, and use border-connected white-background removal only.
External-image reuse rights still require manual review; source pages and direct image URLs are recorded in MONOBLOCK_PHOTO_PROGRESS.json.

### Next proposed stage

After owner review, continue with photos for other categories. Laptops after commit 9ec8a39 remain outside this stage.

## Monoblock card/photo corrections (2026-10-20)

- Fixed the existing monoblock card image layering in rgw_page_monoblocks.html: the image keeps its hover transform, while the brand badge now has a higher stacking level and remains above the transformed image.
- Kept the card dimensions, brand badge appearance, filter markup, product data attributes and filter script unchanged.
- Reduced only the existing image hover scale from 1.06 to 1.03 and retained the existing .25s transition; the image wrapper keeps object-fit: contain, adds internal box sizing, and uses a small consistent inset.
- Reframed the main images for mono-001, mono-003 and mono-007 on a transparent square canvas so the complete HP device remains visible with margins. Additional gallery files were not replaced.
- Replaced only assets/products/mono-006/main.webp with a single-unit exact PRO AP272P 14M frame from the official MSI Gallery. products.json image paths and the four additional gallery files were preserved.
- Updated MONOBLOCK_PHOTO_PROGRESS.json with the corrected MSI source and resulting asset metadata.

### Scope and checks

- Confirmed the seven monoblock card IDs remain present; mono-002 remains the existing placeholder.
- Hash-guarded products.json, price.csv, product.html, product.js, all laptop files, and every non-monoblock category page; the correction script aborts if any of them changes.
- Confirmed the catalog markup outside the monoblock page CSS block is byte-for-byte unchanged.
- Confirmed the page still points to the same main.webp paths and the universal product.html?id=mono-XXX gallery continues to receive the existing images[] arrays.
- GitHub Pages publication and interactive browser hover checks are performed after the commit; if the environment cannot provide an interactive browser, that limitation will be reported explicitly.


## Published verification — monoblock card correction (2026-10-20)

- GitHub Pages build/deployment for the correction commit e6e80a8647a9eb64d841a38d4a919aac85c1db71 completed successfully (run 39471990812).
- Static verification confirmed all seven monoblock cards, 26 existing monoblock WebP gallery files, unchanged product-page gallery logic, unchanged protected files, and the responsive image rules.
- An interactive browser/screenshot runtime was not available in this environment, so live hover/touch interaction and pixel-level visual comparison could not be performed here. The CSS and asset checks were completed from the published source tree and deployment result.

## Lenovo monoblock photo scale correction (2026-10-20)

- Reframed only the main images for mono-004 (Lenovo IdeaCentre 27IRH9 Core i7) and mono-005 (Lenovo IdeaCentre 27IRH9 Core i5) on a 1000x1000 transparent canvas with a 0.74 visible-image ratio, preserving proportions and adding margins around the complete device.
- Kept the existing monoblock CSS unchanged: the Lenovo badge remains above the image and the existing smooth hover animation, transition and card dimensions are preserved.
- Did not modify HP mono-001, mono-003 or mono-007, MSI mono-006, the mono-002 placeholder, or any additional gallery image.
- Product IDs, SKUs, titles, characteristics, prices, products.json, product.html, product.js, price.csv, filters, laptops and other categories remain protected.

### Scope checks

- Checked all seven monoblock card IDs and retained the existing main.webp links and product gallery arrays.
- Protected every other asset under assets/products, every category page, product-page files, product data and price.csv; the correction script aborts on an unexpected change.
- GitHub Pages and interactive visual checks are completed after the final commit; an unavailable browser runtime will be recorded explicitly.


## Published verification — Lenovo monoblock scale correction (2026-10-20)

- GitHub Pages build/deployment for the Lenovo correction commit 81b422429dbfd330aedeff6b5e09b9e23b15cb16 completed successfully (run 39472893741).
- Static verification confirmed that all seven monoblock cards remain linked, all 26 monoblock WebP assets remain present, and the current badge layering, hover scale, transition, mobile rule and product gallery paths are unchanged.
- An interactive browser/screenshot runtime was not available in this environment, so live hover/touch and pixel-level visual comparison could not be performed here; this limitation is recorded explicitly.


## System-unit photo stage (2026-10-20)

- Обработаны все 8 карточек категории «Системные блоки» (case-001—case-008).
- Для каждой модели использованы точные официальные страницы/файлы DeepCool; похожие модели и чужие изображения не подставлялись.
- Главные и дополнительные кадры скачаны, приведены к WebP без искусственного увеличения; белый фон удалён только из связной краевой области, если он был встроен.
- Каталог и product.html?id=... используют существующую архитектуру: изменены только image-слоты системных блоков и поля image/images для этих восьми записей.
- CSS, анимация карточек, цены, характеристики, названия, SKU, ID, price.csv, ноутбуки, моноблоки и остальные категории не изменялись.

### Результаты

- case-001 — DeepCool CASE CH 370 WHITE: 5 WebP, главное фото images/products/case-001/main.webp.
- case-002 — DeepCool CASE CH 370 BLACK: 5 WebP, главное фото images/products/case-002/main.webp.
- case-003 — DeepCool CASE CG530 4F: 5 WebP, главное фото images/products/case-003/main.webp.
- case-004 — DeepCool CASE CG580 4F V2: 5 WebP, главное фото images/products/case-004/main.webp.
- case-005 — DeepCool CASE MATREXX 50: 5 WebP, главное фото images/products/case-005/main.webp.
- case-006 — DeepCool CASE CH 160 WHITE: 5 WebP, главное фото images/products/case-006/main.webp.
- case-007 — DeepCool CASE CC560 LIMITED V2: 5 WebP, главное фото images/products/case-007/main.webp.
- case-008 — DeepCool CASE CG380 3F: 5 WebP, главное фото images/products/case-008/main.webp.

### Источники

- Официальные страницы DeepCool и соответствующие CDN-пути указаны в SYSTEM_UNIT_PHOTO_PROGRESS.json.
- Права на повторное коммерческое размещение внешних изображений требуют отдельной ручной проверки.

### Проверки

- Сверены все 8 ID, SKU и названия с текущим каталогом.
- Галерея использует существующий product.js и массив images[]; filter/sort/card layout не переписывались.
- Перед коммитом проверяется, что изменены только системные image-слоты, новые локальные WebP, progress-файл и этот статус.
\n\n## Published verification — system-unit photo stage (2026-10-20)\n\n- GitHub Pages build/deployment for the system-unit photo commit f5c765fa959248760d03759530d01373a292cf53 completed successfully (run 39474394312).\n- Static verification confirmed all 8 system-unit IDs, 40 local WebP files, catalog image slots, existing product.html?id=... gallery wiring, unchanged prices and unchanged non-image product data.\n- The final diff contains no laptop, monoblock or other-category page/assets; the temporary processing workflow/script were removed from the final tree.\n- An interactive browser/screenshot runtime is not available in this environment, so live visual inspection of the published pages could not be performed here; the source-tree and Pages deployment checks were completed.\n

## Исправление дублирования чекбоксов системных блоков (2026-10-20)

- В соответствующем файле категории `rgw_page_system_units.html` устранено двойное отображение: настоящий `input[type="checkbox"]` сохранён для работы фильтра, а его нативная отрисовка визуально скрыта тем же правилом, что используется в `rgw_page_monoblocks.html`.
- Кастомные `.checkmark`, RGW-цвет, hover строки, checked-галочка, переходы, focus и reduced-motion не менялись.
- Проверены все группы с checkbox: «Производитель» (1 значение) и «Цвет» (2 значения); у каждого input остался ровно один `.checkmark`.
- JS фильтрации не переписывался: сохранён существующий обработчик `change`, а выбор/снятие checkbox по-прежнему обновляет карточки и счётчики.
- Карточки, фотографии, цены, характеристики, SKU, ID, данные товаров и другие категории не изменялись.
- Выполнена статическая проверка HTML/CSS/JS. Интерактивный браузерный runtime для live-проверки hover/tap в окружении недоступен; публикация GitHub Pages проверяется отдельно.


## Этап: фотографии комплектующих (2026-10-20)

Обработаны все 9 подкатегорий раздела «Комплектующие» и все 137 товарных записей:

- Видеокарты — 8
- Процессоры — 17
- Материнские платы — 16
- Оперативная память — 11
- SSD — 22
- HDD — 8
- Корпуса — 17
- Блоки питания — 17
- Охлаждение — 21

Итог по фото:

- 22 товара имеют подключённые фотографии;
- 14 наборов фотографий добавлены в рамках этого этапа;
- добавлено 41 новых WebP-файлов;
- 115 товаров оставлены с заглушками, потому что точный официальный ассет не удалось подтвердить;
- сохранены 8 ранее подтверждённых наборов компонентных фото;
- подробный перечень по каждому ID, путям, источникам и причинам пропуска находится в `COMPONENTS_PHOTO_PROGRESS.json`.

Добавленные источники точных моделей: ASUS, GIGABYTE, Samsung, Western Digital, DeepCool и GamerStorm/DeepCool. Для корпусов, блоков питания и охлаждения DeepCool использованы прямые product-gallery ассеты производителя; фоновые изображения сайта не использовались. Неподтверждённые изображения похожих моделей не добавлялись. В частности, изображения WD Purple 6 ТБ и 8 ТБ удалены после проверки: официальные страницы отдавали один и тот же URL изображения 1 ТБ.

Подключение проверено статически:

- JSON товаров корректен;
- все 22 подключённых пути существуют;
- карточки 9 страниц категорий ссылаются на соответствующие `images/products/<ID>/main.webp`;
- дополнительные галерейные файлы подключены в `products.json`;
- WebP-файлы прошли загрузку и преобразование через Pillow в GitHub Actions.

В рамках этапа не изменялись ноутбуки, моноблоки и системные блоки, цены, `price.csv`, характеристики, названия, ID, SKU, `product.html`, `product.js`, фильтры, карточки и дизайн сайта. Временные инструменты сбора после завершения удалены из репозитория.

Браузерная визуальная проверка из текущего окружения недоступна; проверка GitHub Pages выполнена по статусу публикации Actions.

<!-- COMPONENTS PHOTO STAGE V2 START -->
## Повторный полный проход фотографий комплектующих (2026-10-21)

Проверены все 137 товаров девяти подкатегорий раздела «Комплектующие»: Видеокарты, Процессоры, Материнские платы, Оперативная память, SSD, HDD, Корпуса, Блоки питания и Охлаждение.

- новые точные наборы добавлены для **46** товаров; существующие подтверждённые наборы сохранены для **22** товаров; заглушки оставлены для **69** товаров;
- в компонентные записи подключено **207** локальных WebP-файлов;
- карточки категорий переведены с placeholder-icon на соответствующий `images/products/<ID>/main.webp`; универсальная галерея продолжает использовать существующие `product.js` и `images[]`;
- цены, характеристики, названия, ID, SKU, `price.csv`, фильтры и товары других категорий не изменялись; существующие фотографии ноутбуков, моноблоков и системных блоков сохранены;
- источники новых изображений: официальные страницы/ассеты GALAX, MSI, ASUS, GIGABYTE, Kingston, Lexar, Samsung, Western Digital, GameMax, Segotep и DeepCool.

Товары, которые остались с заглушками, перечислены в `COMPONENTS_PHOTO_PROGRESS.json` с причиной по каждому ID. Причина в основном — отсутствует точная модель/артикул в каталоге или официальный ассет не позволяет подтвердить конкретную модификацию; похожие изображения не использовались.

Автоматическая проверка: 2026-10-21T17:27:55.540836+00:00; все скачанные изображения открыты Pillow и сохранены как WebP, без искусственного увеличения; обновление выполнялось только в рамках девяти компонентных страниц.
<!-- COMPONENTS PHOTO STAGE V2 END -->

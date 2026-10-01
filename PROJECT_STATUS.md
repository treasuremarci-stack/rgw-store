# PROJECT_STATUS.md — АКС current state

Last updated: 2026-10-01

## Mode
AUTONOMOUS-BY-STAGE.

The agent may decide how to execute the current approved stage, but MUST stop before beginning the next stage.

## Current checkpoint

Universal product-page integration stage extended.

The existing `product.html?id=PRODUCT_ID` flow now supports the 12 laptop cards and all 7 current monoblock cards. Product records keep stable identifiers and only confirmed model-specific characteristics; unsupported fields remain omitted. Product pages keep prices and real images as placeholders until later stages.

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

## Next proposed stage

**Phase 5A — monitors, keyboards and mice product pages.**

The next approved batch should connect the current «Мониторы», «Клавиатуры» and «Мыши» cards to the same universal product-page flow, preserving their current catalog data and visual behavior.

## User approval gate

WAITING FOR USER.

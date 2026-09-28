# PROJECT_STATUS.md — RGW current state

Last updated: 2026-09-28

## Mode
AUTONOMOUS-BY-STAGE.

The agent may decide how to execute the current approved stage, but MUST stop before beginning the next stage.

## Current checkpoint
Phase 2A — checkbox/filter UI reference audit completed.

The current `rgw_page_monoblocks.html` implementation is now documented as the primary checkbox/filter visual reference. No storefront implementation was changed in this stage.

## Known project facts
- Repository: `treasuremarci-stack/rgw-store`.
- Default working branch requested by the user: `main`.
- `price.csv` is the assortment source of truth.
- `rgw_multipage_home.html` / current global catalog assets provide the existing catalog/navigation implementation.
- `rgw_page_monoblocks.html` is the current primary visual reference for checkbox/checkmark/row-hover behavior.
- A recent headphones change caused a product-image sizing regression; subsequent work targeted restoring the card/image constraints. Because of that history, image/card regression checks are mandatory when editing category CSS.
- The repository currently contains many `rgw_page_*.html` category pages plus shared catalog/brand assets.

## Completed in this checkpoint
- Re-audited the current `rgw_page_monoblocks.html` on `main`.
- Confirmed that the page uses only `rgw_global_catalog.css` and `rgw_brand.css` as external stylesheets; the checkbox interaction is implemented in the page's inline `<style>`.
- Confirmed the reference markup pattern:
  `<label class="check"><input type="checkbox" data-filter="..."><span class="checkmark" aria-hidden="true"></span>...</label>`.
- Confirmed the current reference contains 16 checkbox inputs and 16 matching `.checkmark` elements.
- Documented the effective reference selectors:
  - `.check`: flex row, expanded horizontal hover area, no text selection, 170 ms color/background transition;
  - `.check:hover`: RGW-accent translucent row highlight;
  - `.check input`: visually hidden native control that remains the state/accessibility source;
  - `.checkmark`: 18×18 custom checkbox box with border, rounded corners and transition;
  - `.check:hover .checkmark`: accent border and soft focus ring;
  - `.check input:checked + .checkmark`: accent background/border and small scale animation;
  - `.checkmark::after`: centered white checkmark with opacity/transform animation;
  - focus and disabled selectors: `.check input:focus-visible + .checkmark` and `.check input:disabled + .checkmark`.
- Confirmed the current filter behavior remains JavaScript-driven by the existing page script; the visual reference does not require a new filtering implementation.
- Confirmed `rgw_global_catalog.css` contains no checkbox/checkmark rules, and no `rgw_checkbox.css` file exists on `main`.
- Identified a legacy cascade inside the same inline style: an earlier base `.check` / `.check input` definition uses the native checkbox sizing/accent color, while the later reference layer overrides the input to a visually hidden control and renders the visible state through `.checkmark`. The later reference layer is authoritative by source order.
- No products, prices, `price.csv`, category pages, links, JavaScript behavior or shared CSS files were changed.

## Verification
- Re-fetched `rgw_page_monoblocks.html`, `rgw_global_catalog.css` and `rgw_global_catalog.js` from `main`.
- Confirmed all 16 checkbox inputs have matching adjacent `.checkmark` spans.
- Confirmed the checked selector uses the required adjacent-sibling relationship: `.check input:checked + .checkmark`.
- Confirmed the row-hover selector and centered checkmark pseudo-element are present.
- Confirmed the mobile filter drawer selectors and existing filtering handlers remain present.
- Confirmed this stage changed only `PROJECT_STATUS.md`.

## Next proposed stage
**Phase 3A — inventory and group category filter implementations.**

On user command `продолжай`:
1. inventory all `rgw_page_*.html` pages that contain filters;
2. group them by checkbox/row-hover implementation pattern;
3. identify one safe pilot page for the approved visual implementation;
4. do not propagate changes yet;
5. update this status file;
6. commit the stage;
7. STOP again for approval.

## User approval gate
WAITING FOR USER.

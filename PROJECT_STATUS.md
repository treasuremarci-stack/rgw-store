# PROJECT_STATUS.md — RGW current state

Last updated: 2026-09-28

## Mode
AUTONOMOUS-BY-STAGE.

The agent may decide how to execute the current approved stage, but MUST stop before beginning the next stage.

## Current checkpoint
Phase 3A — category filter inventory and grouping completed.

The current repository-wide filter inventory is documented below. No storefront implementation was changed in this stage.

## Known project facts
- Repository: `treasuremarci-stack/rgw-store`.
- Default working branch requested by the user: `main`.
- `price.csv` is the assortment source of truth.
- `rgw_multipage_home.html` / current global catalog assets provide the existing catalog/navigation implementation.
- `rgw_page_monoblocks.html` is the current primary visual reference for checkbox/checkmark/row-hover behavior.
- A recent headphones change caused a product-image sizing regression; subsequent work targeted restoring the card/image constraints. Because of that history, image/card regression checks are mandatory when editing category CSS.
- The repository currently contains many `rgw_page_*.html` category pages plus shared catalog/brand assets.

## Completed in this checkpoint
- Inventoried all 55 root `rgw_page_*.html` category pages on `main`.
- Confirmed that all 55 pages reference the shared `rgw_global_catalog.js`.
- Grouped the pages by their actual filter controls and checkbox implementation:
  - **Group A — approved custom checkbox family: 50 pages.** Every page except the named exceptions below has `.checkmark`, a custom checked adjacent-sibling selector, and `.check:hover` row-hover behavior. This is the broad existing implementation family.
  - **Group B — native checkbox pilot candidate: `rgw_page_headphones.html`.** It has 6 real checkbox inputs and matching `.checkmark` spans in the markup, but its current inline CSS exposes the native checkbox and lacks the approved custom checkmark/row-hover rules.
  - **Group C — non-checkbox filter controls: `rgw_page_connectors_outlets.html`, `rgw_page_network_accessories.html`, and `rgw_page_mini_pbx.html`.** These pages contain filter UI but currently have no checkbox inputs or matching `.checkmark` implementation, so they are not part of the checkbox propagation batch.
  - **Group D — no-filter category shell: `rgw_page_components.html`.** It contains no checkbox/data-filter implementation and was excluded from the filter inventory.
- Confirmed that the 50-page custom family is not completely uniform internally:
  - `rgw_page_monoblocks.html` remains the clean visual reference for the effective custom layer.
  - `rgw_page_cases.html` is a clean custom-only example.
  - Pages such as `rgw_page_access_points.html` and `rgw_page_laptops.html` retain older native/`.check.is-checked` rules before a later custom layer; the later custom layer is visually authoritative, but those legacy rules must be preserved unless a future stage explicitly addresses the cascade.
- Selected `rgw_page_headphones.html` as the single safe pilot for the next stage because it is small (6 filters, 7 products), already had a dedicated image/card audit, and has the required filter markup without requiring product, price, catalog, or JavaScript data changes.
- No products, prices, `price.csv`, category pages, links, JavaScript behavior, or shared CSS files were changed in this stage.

## Verification
- Re-fetched and inspected all 55 category pages from `main`.
- Counted checkbox inputs, `.checkmark` markup, custom checked selectors, and row-hover selectors per page.
- Confirmed the headphones pilot has 6 checkbox inputs, while the three non-checkbox filter pages have zero checkbox inputs.
- Confirmed `rgw_page_components.html` has no filter controls.
- Confirmed the shared catalog script is present across the inventory.
- Confirmed the only intended change for this stage is this status file.

## Next proposed stage
**Phase 3B — apply the approved custom checkbox interaction to one pilot: `rgw_page_headphones.html`.**

On user command `продолжай`:
1. re-inspect the current headphones page and the monoblocks reference;
2. apply only the required checkbox/row-hover presentation rules to the pilot;
3. preserve product data, prices, cards, images, filtering, sorting, mobile filter behavior and catalog links;
4. verify the page and its related functions;
5. update this status file;
6. commit the stage;
7. STOP for visual approval before propagating anything further.

## User approval gate
WAITING FOR USER.

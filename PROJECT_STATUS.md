# PROJECT_STATUS.md — RGW current state

Last updated: 2026-09-28

## Mode
AUTONOMOUS-BY-STAGE.

The agent may decide how to execute the current approved stage, but MUST stop before beginning the next stage.

## Current checkpoint
Phase 0 — workflow setup.

This checkpoint creates project-control files only. No storefront HTML/CSS/JS/product data should be changed as part of this phase.

## Known project facts
- Repository: `treasuremarci-stack/rgw-store`.
- Default working branch requested by the user: `main`.
- `price.csv` is the assortment source of truth.
- `rgw_multipage_home.html` / current global catalog assets provide the existing catalog/navigation implementation.
- `rgw_page_monoblocks.html` is the current primary visual reference for checkbox/checkmark/row-hover behavior.
- A recent headphones change caused a product-image sizing regression; subsequent work targeted restoring the card/image constraints. Because of that history, image/card regression checks are mandatory when editing category CSS.
- The repository currently contains many `rgw_page_*.html` category pages plus shared catalog/brand assets.

## Completed in this checkpoint
- Added persistent agent operating rules.
- Added staged roadmap.
- Added this persistent status file.
- No storefront implementation changes are included in this setup stage.

## Next proposed stage
**Phase 1A — headphones audit only.**

On user command `продолжай`:
1. inspect the current `rgw_page_headphones.html`;
2. compare relevant recent history if needed;
3. verify card/image constraints, filters, sorting/reset, mobile-sensitive CSS and global catalog integration;
4. make a targeted fix only if a concrete defect is found;
5. update this status file;
6. commit the stage;
7. STOP again for approval.

## User approval gate
WAITING FOR USER.

# PROJECT_PLAN.md — RGW roadmap

Goal: finish and standardize the RGW store incrementally without large risky rewrites.

## Operating principle
Only one stage may be executed per user approval. A stage is not permission to continue into later stages.

## Phase 0 — Autonomous workflow setup
- [x] Add persistent agent rules.
- [x] Add project roadmap.
- [x] Add persistent project status.

## Phase 1 — Stabilize current pages
- [ ] Audit the current `rgw_page_headphones.html` after recent fixes.
- [ ] Verify product-card/image constraints and confirm no oversized-image regression.
- [ ] Verify headphones filters, sorting, reset, mobile behavior and global catalog.
- [ ] Make only targeted fixes found by the audit.

## Phase 2 — Establish UI references
- [ ] Re-audit `rgw_page_monoblocks.html` as the checkbox/filter interaction reference.
- [ ] Document the exact reference selectors/markup required for checkbox, checkmark and row hover.
- [ ] Confirm which shared CSS files are authoritative and identify conflicting legacy styles.

## Phase 3 — Standardize category filters safely
- [ ] Inventory all `rgw_page_*.html` pages that contain filters.
- [ ] Group pages by implementation pattern.
- [ ] Apply the approved filter interaction to ONE pilot page.
- [ ] Stop for visual approval.
- [ ] Propagate only after approval, in small category batches.
- [ ] Verify filtering after each batch.

## Phase 4 — Product-card consistency
- [ ] Inventory card/image implementations across category pages.
- [ ] Define a safe shared card/image baseline without changing assortment.
- [ ] Pilot on one page.
- [ ] After approval, propagate in small batches.
- [ ] Check desktop and mobile grids.

## Phase 5 — Catalog and navigation integrity
- [ ] Verify one global catalog implementation is used.
- [ ] Check category links and remove accidental duplicate navigation implementations only when safe.
- [ ] Check header consistency across pages.
- [ ] Check mobile catalog behavior.

## Phase 6 — Assortment/data audit
- [ ] Compare category pages against `price.csv`.
- [ ] Identify missing, duplicate or misclassified items without changing prices.
- [ ] Fix one category at a time after approval.
- [ ] Preserve future 1C pricing compatibility.

## Phase 7 — Responsive and functional QA
- [ ] Test representative widths: 375, 390, 430, 768 and 1366 px.
- [ ] Check overflow, cards, filters, catalog, typography and controls.
- [ ] Fix regressions in small batches with checkpoints.

## Phase 8 — Homepage polish
- [ ] Audit the current homepage without replacing the approved structure.
- [ ] Identify high-impact improvements.
- [ ] Implement one approved improvement at a time.

## Phase 9 — Final site audit
- [ ] Broken links.
- [ ] Missing assets.
- [ ] Duplicate IDs / malformed markup.
- [ ] Filter/sort regressions.
- [ ] Mobile regressions.
- [ ] Inconsistent category UI.
- [ ] Final status report.

## Definition of done
The site is considered ready when the final audit has no known critical regressions, category navigation works, product pages are consistent, filters/sorting work where present, and data remains compatible with `price.csv` and planned 1C integration.

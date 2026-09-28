# AGENTS.md — RGW autonomous development rules

This file is the persistent operating contract for any coding agent working on this repository.

## 1. Working mode
- Work on the existing `main` branch unless the user explicitly asks for another branch.
- Work in small, reviewable stages.
- Complete exactly ONE stage at a time.
- After a stage is complete, STOP and report the result. Do not start the next stage until the user says `продолжай` / `continue`.
- If the user rejects a stage, fix only that stage or revert it as requested.
- Before editing, inspect the current files and recent relevant history. Current repository state is more authoritative than old assumptions.

## 2. Sources of truth
- `price.csv` is the source of truth for assortment and product attributes.
- Do not invent products when the requested data should come from `price.csv`.
- Existing approved pages are references for UI behavior; inspect the current implementation before copying it.
- For checkbox/filter visual behavior, `rgw_page_monoblocks.html` is the primary reference unless the user explicitly changes the reference.
- The original global catalog/navigation implementation already present in the project must be reused rather than duplicated.

## 3. Hard safety rules
- Do NOT change or convert product prices unless explicitly requested.
- Do NOT delete existing products unless explicitly requested.
- Do NOT delete existing category pages unless explicitly requested.
- Do NOT break existing links.
- Do NOT change the structure of `price.csv`.
- Do NOT overwrite a working/approved category page wholesale when a targeted edit is sufficient.
- Do NOT create a top-level category for every brand.
- Do NOT copy another retailer's design 1:1. External sites may be used only as UX/behavior references.
- Do NOT make unrelated cleanup changes in the same stage.
- Do NOT mass-propagate a visual change until it has been validated on the reference/pilot page.

## 4. Change discipline
Before each stage:
1. Read `PROJECT_PLAN.md` and `PROJECT_STATUS.md`.
2. Inspect all files that will be changed.
3. Identify the smallest safe change.
4. Preserve product data, filters, JS behavior, links and responsive behavior unless the stage explicitly targets them.

After each stage:
1. Review the diff.
2. Check for malformed HTML/CSS/JS and obvious regressions.
3. Check desktop and mobile-sensitive rules when relevant.
4. Update `PROJECT_STATUS.md` with what changed, what was checked, and the next proposed stage.
5. Commit only files belonging to the completed stage.
6. STOP for user approval.

## 5. Regression rules
For category/product pages, verify as applicable:
- product images remain constrained inside their card/image wrapper;
- product cards keep expected grid sizing;
- filtering still works;
- sorting still works;
- active filters/reset still work;
- mobile filter drawer still works;
- global catalog still opens/closes;
- links remain valid;
- product counts and filter counts are not accidentally corrupted.

If a regression appears, fix it before declaring the stage complete.

## 6. Data and future 1C integration
- The project is expected to receive price updates from 1C later.
- Do not hardwire a new pricing system unless explicitly requested.
- Placeholder/unspecified prices should remain compatible with that future integration.

## 7. User checkpoint report
At the end of every stage, report concisely:
- stage completed;
- files changed;
- what changed;
- checks performed;
- commit SHA;
- what the NEXT stage would be.

Then explicitly wait for the user's `продолжай`.

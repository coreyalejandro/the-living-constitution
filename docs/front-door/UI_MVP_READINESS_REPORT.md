# UI MVP readiness report — TLC control plane

**Date:** 2026-03-31  
**Scope:** Wired MVP for `apps/tlc-control-plane` per C-RSP contract (TLC AI Governance System).

## What changed

- Added a **read-only adapter layer** under `apps/tlc-control-plane/lib/adapters/` for `STATUS.json`, system graph inventory, and verification path presence checks.
- Added **`lib/repo-root.ts`** to resolve the monorepo root via `STATUS.json` (optional `TLC_REPO_ROOT`).
- Wired **`app/page.tsx`** with `dynamic = "force-dynamic"` so status reads occur at request time, not only at static build time.
- Updated all four panels to show **truth-source** and **functional-status** badges (plus plain-language notes), semantic headings, keyboard-focusable regions (`tabIndex={0}`), and `sr-only` labels where helpful.
- Updated **shell copy** to state the UI is subordinate to `STATUS.json` and does not claim authority.
- Added **`prefers-reduced-motion`** rules in `app/globals.css`.
- Refreshed **`apps/tlc-control-plane/README.md`** to match actual behavior.

## What is working

- Home route renders **system graph**, **status/truth**, **execution**, and **verification** regions.
- **Status/truth panel** reads `STATUS.json` from the resolved repo root when `STATUS.json` is readable (live filesystem read).
- **System graph** reads `MASTER_PROJECT_INVENTORY.json` when present and lists `tlc_projects_overlay.expected_slugs`.
- **Verification stream** lists configured paths and reports **file present / not found / unknown** when repo root resolves.
- **Production build** completes (`npm run build` in `apps/tlc-control-plane`).

## What is partial

- **Execution pane:** Documentation-backed sequencing text; augments with read-only `STATUS.json` fields when available — not an execution engine.
- **System graph:** List-only, not interactive navigation.
- **Verification stream:** File presence checks only — not CI event streaming or ledger replay.

## What is not implemented

- Live CI or telemetry feeds.
- Graph interactivity (zoom, edge inspection, drill-down).
- Any write path to `STATUS.json` or other governance artifacts.

## Verification steps

1. From repo: `cd apps/tlc-control-plane && npm install && npm run build` — expect success.
2. `npm run dev` — open `/` and confirm four panels.
3. Confirm status panel shows **Live repo read** when `STATUS.json` resolves (typical when cwd is `apps/tlc-control-plane`).
4. Confirm badges and footers state truth source and **not** real-time telemetry.
5. Search codebase for `STATUS.json` writes from the app — expect none.

## V&T statement

- **Exists:** Verified present — adapter modules, updated panels, `page.tsx` with `force-dynamic`, README, this report, successful local `npm run build` in `apps/tlc-control-plane`.
- **Non-existent:** No mutation path to `STATUS.json`; no product rename; no live telemetry implementation.
- **Unverified:** Manual browser inspection of focus order and screenshots (not executed in this pass).
- **Functional status:** MVP wired for file-backed reads as described; partial/scaffold behaviors documented in README and UI labels.

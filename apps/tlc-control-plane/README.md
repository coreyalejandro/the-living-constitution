# TLC AI Governance System — control plane (MVP)

Next.js App Router UI for the **TLC AI Governance System** (The Living Constitution). This package is a **subordinate operational surface**: it reads approved repository artifacts and **does not** replace `STATUS.json` as the authoritative truth surface.

## Functional status

| Area | Status | Truth source |
| --- | --- | --- |
| Home route (`/`) | **Working** — four canonical panels render | N/A |
| Status / truth panel | **Working** when repo root resolves — reads root `STATUS.json` via read-only adapter | Live repo read → **Authoritative repo truth** |
| Status / truth panel | **Partial** if repo root cannot be resolved or JSON parse fails — embedded snapshot fallback | Static scaffold |
| System graph | **Partial** when `MASTER_PROJECT_INVENTORY.json` is readable — lists expected project slugs | Documentation-backed |
| System graph | **Scaffold-only** fallback — static node list from `lib/tlc-snapshot.ts` | Static scaffold |
| Execution pane | **Partial** — roadmap bullets + read-only fields from loaded `STATUS.json` | Documentation-backed |
| Verification stream | **Partial** — lists known paths; checks file presence when root resolves | File-backed evidence / static |
| Live CI telemetry | **Not implemented** — not presented as a real-time stream | N/A |

## Run locally

Prerequisites: Node.js 20.x, npm or pnpm 9.x.

```bash
cd apps/tlc-control-plane
npm install
npm run dev
```

Open `http://localhost:3000`. Run from `apps/tlc-control-plane` so the adapter can resolve the monorepo root (parent of `apps/`) and read `STATUS.json`.

Optional: set `TLC_REPO_ROOT` to an absolute path to the TLC repository if `process.cwd()` does not allow resolution.

## Build

```bash
npm run build
npm start
```

## Architecture

- **Read-only adapters:** `lib/adapters/*` — no writes to governance artifacts; typed load results include `SourceStatusMeta` (truth surface + functional status).
- **Fallback snapshot:** `lib/tlc-snapshot.ts` — used only when live read fails or root is unknown.
- **UI labeling:** Each panel shows truth-source badges and functional status (plain text, not color-only).

## Truth surface

Authoritative operational status remains **`STATUS.json`** at the repository root (human mirror: `STATUS.md`). This UI renders a read-only view; it never writes `STATUS.json`.

## Governance

Maintenance-mode governance applies. This app does not execute a new TLC governance pass.

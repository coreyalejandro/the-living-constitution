# TLC control plane (scaffold)

Minimal Next.js App Router shell for the TLC **governance control plane** UI. This package is **static scaffolding** with a **local snapshot** of status fields; it does **not** replace `STATUS.json` as the authoritative truth surface.

## Functional status

- **Renders:** Four panels — **system graph**, **status/truth panel**, **execution pane**, **verification stream** — on the home route.
- **Data:** Static snapshot in `lib/tlc-snapshot.ts` (aligned to repository status at scaffold creation). Not a live read of `STATUS.json`.
- **Non-wired:** All dynamic behavior, live verification streams, and graph interactivity are explicitly labeled in the UI as scaffold-only.

## Run locally

Prerequisites: Node.js 20.x, and npm or pnpm 9.x.

```bash
cd apps/tlc-control-plane
npm install
npm run dev
```

Use `pnpm install` / `pnpm dev` instead if you prefer pnpm in this directory.

Open `http://localhost:3000`.

## Build

```bash
pnpm build
pnpm start
```

## Truth surface

Authoritative operational status: **`STATUS.json`** at the repository root (human mirror: `STATUS.md`). Update the snapshot module manually if you need the UI to reflect a new committed status after intentional changes.

## Governance

Maintenance-mode governance applies. This app does not execute a new TLC governance pass.

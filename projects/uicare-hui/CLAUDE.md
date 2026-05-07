# CLAUDE.md — UICare-HUI (Behavioral Safety System)

## What This Is

Governance overlay for **uicare-hui** — a Hexagonal Architecture monorepo that implements
a Behavioral Safety System for High-Risk Neurodivergent Users.

Implementation lives at:
  `/Users/coreyalejandro/Projects/uicare-hui`
  GitHub: https://github.com/coreyalejandro/uicare-hui (to be created)

## Domain

Human Safety — behavioral-state tracking, restrictive action gates, local-first safety
logic, consent-aware monitoring, accessibility-first intervention design.

## TLC Alignment

This project is a **Satellite project** of The Living Constitution Commonwealth.
It is governed by TLC Articles I–V and by contract instance `CRSP-UICARE-HUI-001`.

Governing contract: `projects/c-rsp/instances/CRSP-UICARE-HUI-001.md`
Schema authority: `projects/c-rsp/contract-schema.json`
Canonical C-RSP master: `projects/c-rsp/BUILD_CONTRACT.md`

## Not Claimed

- Not a medical device.
- Not an emergency-response system.
- Not a clinical diagnostic tool.
- Does not replace professional mental-health services.
- TLC does not vouch for the clinical accuracy of any behavioral scoring.

## Rules

1. All Living Constitution Articles I–V apply.
2. INVARIANT_011 (zero-dependency `packages/safety-core`) is a structural invariant
   enforced by CI ESLint boundary lint — violations halt the build.
3. INVARIANT_001 (consent required before monitoring) is a runtime invariant enforced
   inside `packages/safety-core/src/consent/consent-enforcer.ts`.
4. No clinical language in any user-facing copy (INVARIANT_008).
5. `packages/safety-core` is the truth surface for all safety logic — never bypass it
   through an adapter.
6. Implementation repos are the source of truth for code; this overlay is governance only.
7. Do not duplicate implementation code here.

## Resume Claim

"UICare-HUI — Behavioral Safety System for High-Risk Neurodivergent Users |
Status: Phase 0-8 Build Contract Executed | Hexagonal Architecture monorepo |
TypeScript, Next.js 14 PWA, IndexedDB, AES-256-GCM | 72/72 tests passing |
Local-first, offline-capable safety gates | Consent-enforced behavioral monitoring"
